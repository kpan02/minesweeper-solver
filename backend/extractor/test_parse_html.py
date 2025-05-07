from parse_html import parse_board

def print_grid(grid):
    for row in grid:
        print(' '.join(
            f"{cell.value if cell.state == 'number' else '.' if cell.state == 'closed' else cell.state[0].upper()}"  
            # N for number, _ for closed, F for flag, M for mine, U for unknown
            for cell in row
        ))

if __name__ == "__main__":
    with open("example_html.txt", "r", encoding="utf-8") as f:
        html = f.read()
    grid = parse_board(html)
    print_grid(grid)
