from rich import print
import sys
import random

def print_grid(grid):
	print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]))

def get_column(col, board):
	return [x[col] for x in board]

def get_row(row, board):
	return board[row]

def check_array(array, reverse):
	last_seen = 0
	counter_seen = 0
	for el in array[::1 if not reverse else -1]:
		if el > last_seen:
			last_seen = el
			counter_seen+=1
	return counter_seen

def can_place(row, col, board, value):
	h = get_row(row, board)
	v = get_column(col, board)
	if value in h or value in v:
		return False
	return True

def	found_solution(board):
	return all([all(board[x]) for x in range(N)])

def get_borders(board):
	borders = {pos:[0 for x in range(N)] for pos in POSITIONS}
	borders["left"] = [check_array(get_row(x, board), False) for x in range(N)]
	borders["right"] = [check_array(get_row(x, board), True) for x in range(N)]
	borders["top"] = [check_array(get_column(x, board), False) for x in range(N)]
	borders["bottom"] = [check_array(get_column(x, board), True) for x in range(N)]
	return borders
	
	
def borders_to_str(borders):
	return "".join("".join(f"{y} " for y in x) for x in list(borders.values()))[:-1]

def gentests(row, col, board):
	if (found_solution(board)):
		print(borders_to_str(get_borders(board)))
		print_grid(board)
		return
	choices = list(range(1, N+1))
	random.shuffle(choices)
	for choice in choices:
		if (can_place(row, col, board, choice)):
			board[row][col] = choice
		else:
			continue
		next_col = (col + 1) % N
		next_row = row
		if (next_col == 0):
			next_row = (row + 1) % N
		gentests(next_row, next_col, board)
	board[row][col] = 0

N = int(sys.argv[1])
POSITIONS = ["top", "bottom", "left", "right"]
board = [[0 for x in range(N)] for x in range(N)]
print(board)

gentests(0, 0, board)