from bs4 import BeautifulSoup
import re
from typing import List, Optional

class Cell:
    def __init__(self, x: int, y: int, state: str, value: Optional[int] = None):
        self.x = x
        self.y = y
        self.state = state  # 'closed', 'flag', 'number', 'mine', 'unknown', 'error'
        self.value = value  # only for number cells

    def __repr__(self):
        return f"{self.state}:{self.value}" if self.value is not None else self.state

def parse_board(html: str) -> List[List[Cell]]:
    """
    Parse the Minesweeper board from the provided HTML string.
    Only cells inside the "AreaBlock" div are considered. 
    Coordinates are taken from data-x/data-y if available, otherwise from the id.
    Returns a 2D grid (list of rows, each a list of Cell objects).
    """
    soup = BeautifulSoup(html, 'html.parser')
    area_block = soup.find('div', id='AreaBlock')
    if not area_block:
        raise ValueError("AreaBlock not found in HTML")

    cells = area_block.find_all(id=re.compile(r'^cell_\d+_\d+$'))

    board = {}
    max_x = max_y = 0

    for cell in cells:
        try:
            x = int(cell.get('data-x')) if cell.has_attr('data-x') else int(cell['id'].split('_')[1])
            y = int(cell.get('data-y')) if cell.has_attr('data-y') else int(cell['id'].split('_')[2])
        except Exception:
            x, y = -1, -1  
        class_list = cell.get('class', [])

        if x not in board:
            board[x] = {}

        state = 'unknown'
        value = None

        if 'hd_flag' in class_list:
            state = 'flag'
        elif 'hd_opened' in class_list:
            if 'hd_mine' in class_list:
                state = 'mine'
            else:
                for cls in class_list:
                    if cls.startswith('hd_type'):
                        state = 'number'
                        try:
                            value = int(cls.replace('hd_type', ''))
                        except Exception:
                            value = None
                        break
                if state != 'number':
                    state = 'opened'  
        elif 'hd_closed' in class_list:
            state = 'closed'
        else:
            state = 'unknown'

        board[x][y] = Cell(x, y, state, value)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    # Build grid by rows (y) and columns (x)
    grid = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(board.get(x, {}).get(y, Cell(x, y, 'unknown')))
        grid.append(row)

    return grid
