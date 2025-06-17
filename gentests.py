from rich import print
import sys
import random

def print_grid(grid):
	print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]))

def get_column(col, board):
	return [x[col] for x in board]

def get_row(row, board):
	return board[row]

def prefill(board, frame):
	global FILLED_CELLS
	for i in range(N):
		if frame["top"][i] == 1:
				board[0][i] = N
		if frame["bottom"][i] == 1:
				board[N-1][i] = N
		if frame["left"][i] == 1:
				board[i][0] = N
		if frame["right"][i] == 1:
				board[i][N-1] = N
		for j in range(N):
			if frame["top"][i] == N:
				board[j][i] = j+1			
			if frame["bottom"][i] == N:
				board[N-1-j][i] = j+1
			if frame["left"][i] == N:
				board[i][j] = j+1
			if frame["right"][i] == N:
				board[i][N-1-j] = j+1

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
	global FOUND
	FOUND = FILLED_CELLS == N*N
	return FOUND

def get_frame(board):
	frame = {pos:[0 for x in range(N)] for pos in POSITIONS}
	frame["left"] = [check_array(get_row(x, board), False) for x in range(N)]
	frame["right"] = [check_array(get_row(x, board), True) for x in range(N)]
	frame["top"] = [check_array(get_column(x, board), False) for x in range(N)]
	frame["bottom"] = [check_array(get_column(x, board), True) for x in range(N)]
	return frame
	
	
def frame_to_str(frame):
	return "".join("".join(f"{y} " for y in x) for x in list(frame.values()))[:-1]

def gentests(row, col, board):
	global FILLED_CELLS
	prefilled = False
	if (found_solution(board)):
		#print(frame_to_str(get_frame(board)))
		frame = get_frame(board)
		# values = [v for ar in list(frame.values()) for v in ar]
		# if N in values:
		# print(frame)
		print(frame_to_str(frame))
		print_grid(board)
		return
	if (board[row][col] != 0):
		prefilled = True
		next_col = (col + 1) % N
		next_row = row
		if (next_col == 0):
			next_row = (row + 1) % N
		gentests(next_row, next_col, board)
	if not prefilled:	
		choices = list(range(1, N+1))
		random.shuffle(choices)
		for choice in choices:
			if (can_place(row, col, board, choice)):
				board[row][col] = choice
				FILLED_CELLS += 1
			else:
				continue
			next_col = (col + 1) % N
			next_row = row
			if (next_col == 0):
				next_row = (row + 1) % N
			gentests(next_row, next_col, board)
			board[row][col] = 0
			FILLED_CELLS -= 1

def count_filled(board):
	global FILLED_CELLS
	for row in board:
		for cell in row:
			if cell != 0:
				FILLED_CELLS += 1

FOUND = False
FILLED_CELLS = 0
N = int(sys.argv[1])
POSITIONS = ["top", "bottom", "left", "right"]
board = [[0 for x in range(N)] for x in range(N)]
frame = sys.argv[2].split(" ")
frame = {name:[int(frame[x*N + y]) for y in range(N)] for x, name in enumerate(POSITIONS)}

prefill(board, frame)
count_filled(board)
print_grid(board)
gentests(0, 0, board)