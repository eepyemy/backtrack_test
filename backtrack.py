from rich import print
import sys

def print_grid(grid):
	print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]))

def get_column(col, board):
	return [x[col] for x in board]

def get_row(row, board):
	return board[row]

def check_array(visible_amount, array, reverse):
	last_seen = 0
	counter_seen = 0
	for el in array[::1 if not reverse else -1]:
		if el > last_seen:
			last_seen = el
			counter_seen+=1
	return counter_seen == visible_amount

def can_place(row, col, board, borders, value):
	h = get_row(row, board)
	v = get_column(col, board)
	if value in h or value in v:
		return False
	h[col] = value
	v[row] = value
	if not all(h):
		return True
	checks = []
	checks.append(check_array(borders["left"][row], h, False))
	checks.append(check_array(borders["right"][row], h, True))
	if not all(v) or not all(checks):
		return all(checks)
	checks.append(check_array(borders["top"][col], v, False))
	checks.append(check_array(borders["bottom"][col], v, True))
	return all(checks)

def	found_solution(board):
	return all([all(board[x]) for x in range(N)])

def backtrack(row, col, board, borders):
	if (found_solution(board)):
		print_grid(board)
		return
	for choice in range(1, N+1):
		if (can_place(row, col, board, borders, choice)):
			board[row][col] = choice
		else:
			continue
		next_col = (col + 1) % N
		next_row = row
		if (next_col == 0):
			next_row = (row + 1) % N
		backtrack(next_row, next_col, board, borders)
	board[row][col] = 0

N = int(sys.argv[1])
positions = ["top", "bottom", "left", "right"]
borders = sys.argv[2].split(" ")
borders = {name:[int(borders[x*N + y]) for y in range(N)] for x, name in enumerate(positions)}
board = [[0 for x in range(N)] for x in range(N)]
print(board)

print(borders)
backtrack(0, 0, board, borders)