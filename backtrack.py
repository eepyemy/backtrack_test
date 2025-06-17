from rich import print
import curses
import sys

SCR = curses.initscr()
def print_grid(grid):
	print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]), end="\r\r\r\r", flush=True)

def print_in_place(grid):
	for ind, row in enumerate(grid):
		a = ' '.join([str(cell) for cell in row])
		SCR.addstr(ind, 0, a)
	SCR.refresh()

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

def can_place(row, col, board, frame, value):
	h = list(get_row(row, board))
	v = list(get_column(col, board))
	if value in h or value in v:
		return False
	h[col] = value
	v[row] = value
	if not check_array(frame["left"][row], h, False):
		return False
	if not check_array(frame["right"][row], h, True):
		return False
	if not check_array(frame["top"][col], v, False):
		return False
	if not check_array(frame["bottom"][col], v, True):
		return False
	return True

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

def	found_solution(board):
	global FOUND
	if not FOUND:
		FOUND = FILLED_CELLS == N*N
	return FOUND

def backtrack(row, col, board, frame):
	global FILLED_CELLS, ATTEMPTS
	prefilled = False
	#if ATTEMPTS % 200 == 0:
		#print(f"\n still solving, ... {ATTEMPTS} attempts")
		#print_grid(board)
	print_in_place(board)
	if (found_solution(board)):
		return
	if (board[row][col] != 0):
		prefilled = True
		next_col = (col + 1) % N
		next_row = row
		if (next_col == 0):
			next_row = (row + 1) % N
		backtrack(next_row, next_col, board, frame)
	if not prefilled:
		ATTEMPTS += 4
		for choice in range(1, N+1):
			if (can_place(row, col, board, frame, choice)):
				board[row][col] = choice
				FILLED_CELLS += 1
			else:
				continue
			if col == N-1 and row == N-1:
				break
			next_col = (col + 1) % N
			next_row = row
			if (next_col == 0):
				next_row = (row + 1) % N
			backtrack(next_row, next_col, board, frame)
			if not found_solution(board):
				board[row][col] = 0
				FILLED_CELLS -= 1
def count_filled(board):
	global FILLED_CELLS
	for row in board:
		for cell in row:
			if cell != 0:
				FILLED_CELLS += 1
FOUND = False
ATTEMPTS = 0
N = int(sys.argv[1])
positions = ["top", "bottom", "left", "right"]
frame = sys.argv[2].split(" ") #"1 2 2 4 4 2 2 1 1 2 2 4 4 2 2 1".split(" ") 
# 4 2 3 1
# 2 4 1 3
# 1 3 4 2
# 3 1 2 4

# recurions depth reached
# 1 2 2 4 4 2 2 1 1 2 2 4 4 2 2 1
# 4 3 2 1
# 3 1 4 2
# 2 4 1 3
# 1 2 3 4

# frame = "1 2 2 3 3 2 1 2 1 3 2 3 2 1 3 2".split(" ")

# 8 4 4 3 3 2 2 1 1 2 2 3 3 5 4 8 8 5 4 3 3 2 2 1 1 2 2 3 3 5 4 8
# 1 2 3 4 5 6 7 8
# 2 4 5 3 6 1 8 7
# 3 1 4 7 2 8 5 6
# 4 3 7 8 1 2 6 5
# 5 6 2 1 8 7 3 4
# 6 8 1 2 7 5 4 3
# 7 5 8 6 3 4 1 2
# 8 7 6 5 4 3 2 1

FILLED_CELLS = 0
frame = {name:[int(frame[x*N + y]) for y in range(N)] for x, name in enumerate(positions)}
board = [[0 for x in range(N)] for x in range(N)]
print_grid(board)
print(frame)
print("\nprefilling board:")
prefill(board, frame)
count_filled(board)
print_grid(board)
backtrack(0, 0, board, frame)
print("\nresult:")
print(f"\n attempts: {ATTEMPTS}")
print_grid(board)