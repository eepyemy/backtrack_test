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
	saw_zero = False
	for el in array[::1 if not reverse else -1]:
		if el == 0 and counter_seen == 0:
			return True
		if el > last_seen:
			last_seen = el
			counter_seen+=1
		if el == 0:
			saw_zero = True
	return counter_seen == visible_amount if not saw_zero else counter_seen <= visible_amount

def can_place(row, col, board, borders, value):
	h = list(get_row(row, board))
	v = list(get_column(col, board))
	if value in h or value in v:
		return False
	h[col] = value
	v[row] = value
	if not check_array(borders["left"][row], h, False):
		return False
	if not check_array(borders["right"][row], h, True):
		return False
	if not check_array(borders["top"][col], v, False):
		return False
	if not check_array(borders["bottom"][col], v, True):
		return False
	return True

def	found_solution(board):
	global FOUND
	if not FOUND:
		FOUND = board[N-1][N-1] != 0
	return FOUND

def backtrack(row, col, board, borders):
	if (found_solution(board)):
		return
	for choice in range(1, N+1):
		if (can_place(row, col, board, borders, choice)):
			board[row][col] = choice
		else:
			continue
		if col == N-1 and row == N-1:
			break
		next_col = (col + 1) % N
		next_row = row
		if (next_col == 0):
			next_row = (row + 1) % N
		backtrack(next_row, next_col, board, borders)
	if not found_solution(board):
		board[row][col] = 0

FOUND = False
N = 4
positions = ["top", "bottom", "left", "right"]
# borders = "1 2 2 3 2 3 2 1 1 2 3 2 3 2 2 1".split(" ")
# 4 2 3 1
# 2 4 1 3
# 1 3 4 2
# 3 1 2 4

borders = "1 2 2 3 3 2 1 2 1 3 2 3 2 1 3 2".split(" ")

borders = {name:[int(borders[x*N + y]) for y in range(N)] for x, name in enumerate(positions)}
board = [[0 for x in range(N)] for x in range(N)]
print(board)

print(borders)
backtrack(0, 0, board, borders)
print_grid(board)