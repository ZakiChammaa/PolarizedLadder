from __future__ import print_function
import os, sys

class PolarizedLadder:
	board = []
	def __init__(self, player_id):
		self.player_id = player_id
	def populate_board(self, height, base):
		# Method to set up board
		for i in range(1,height+1):
			temp = []
			for j in range(0,(base - (2*(height-i)))):
				temp.append('-')
			self.board.append(temp)
		for i in range(0, len(self.board)):
			for j in range(1, (height-i)):
				self.board[i].insert(0, ' ')
			for j in range(1, (height-i)):
				self.board[i].append(' ')
		return self.board
	def print_board(self):
		# Method that prints the playing board
		my_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
		for i in range(0,len(self.board)):
			print(len(self.board) - i, end="")
			for j in range(0, len(self.board[i])):
				print(self.board[i][j], end="")
			print("")
		print(" ", end="")
		for i in range(0, len(my_alphabet)):
			print(my_alphabet[i], end="")
		print("")
	def place_move(self, move):
		# Method to let the player place a move
		# Move is also validated for size and position
		my_dict = {0: ['A', 'a'], 1: ['B', 'b'], 2: ['C', 'c'],
		           3: ['D', 'd'], 4: ['E', 'e'], 5: ['F', 'f'],
		           6: ['G', 'g'], 7: ['H', 'h'], 8: ['I', 'i'],
		           9: ['J', 'j'], 10: ['K', 'k'], 11: ['L', 'l'], 
		           12: ['M', 'm']}
		if len(move) == 2 and move[0].isdigit() == False and move[1].isdigit():
			row = len(self.board) - int(list(move)[1])
		else:
			print("Not a valid move")
			return False
		for key in my_dict:
			if list(move)[0] in my_dict[key]:
				col = key
		if self.board[row][col] != '-':
			print("Not a valid move")
			return False
		else:
			self.board[row][col] = 'o' if self.player_id == 1 else 'x'
		return True
	def remove_move(self, move):
		self.board[move[0]][move[1]] = '-'
	def convert_move(self, move):
		# Method that takes indices and converts them to original format
		my_dict = {0: ['A', 'a'], 1: ['B', 'b'], 2: ['C', 'c'],
		           3: ['D', 'd'], 4: ['E', 'e'], 5: ['F', 'f'],
		           6: ['G', 'g'], 7: ['H', 'h'], 8: ['I', 'i'],
		           9: ['J', 'j'], 10: ['K', 'k'], 11: ['L', 'l'], 
		           12: ['M', 'm']}
		for key in my_dict:
			if move[1] == key:
				new_move = my_dict[key][0]
		new_move = new_move + str(len(self.board) - move[0])
		return new_move
	def check_winner(self, child_board):
		# Method checks for the status of the game
		# return 0 => tie game
		# return 1 => player 1 wins
		# return 2 => player 2 wins
		# return 3 => keeps playing
		for i in range(0,len(child_board)):
			for j in range(0, len(child_board[i])):
				try:
					if child_board[i][j] != '-' and child_board[i][j] != ' ':
						# check for right and left side ladder
						if (child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i-1][j+1] and
						child_board[i][j] == child_board[i-1][j+2] and child_board[i][j] == child_board[i-2][j+2]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i-1][j] and
						child_board[i][j] == child_board[i-1][j-1] and child_board[i][j] == child_board[i-2][j-1]):
							if child_board[i][j] == 'o':
								# check if neutralized by opponent
								if (child_board[i][j-1] == 'x' and child_board[i-2][j+1] == 'x') or \
								(child_board[i][j+2] == 'x' and child_board[i-2][j] == 'x'):
									pass
								else:
									return 1
							else:
								# check if neutralized by opponent
								if (child_board[i][j-1] == 'o' and child_board[i-2][j+1] == 'o') or \
								(child_board[i][j+2] == 'o' and child_board[i-2][j] == 'o'):
									pass
								else:
									return 2
				except IndexError:
					pass
		current_token = 'o' if self.player_id == 1 else 'x'
		if (child_board[6][12] == current_token and child_board[6][11] == current_token and child_board[5][11] == current_token and
		child_board[5][10] == current_token and child_board[4][10] == current_token) or (child_board[5][11] == current_token and 
		child_board[5][10] == current_token and child_board[4][10] == current_token and child_board[4][9] == current_token and 
		child_board[3][9] == current_token) or (child_board[4][10] == current_token and child_board[4][9] == current_token and 
		child_board[3][9] == current_token and child_board[3][8] == current_token and child_board[2][8] == current_token) or \
		(child_board[3][9] == current_token and child_board[3][8] == current_token and child_board[2][8] == current_token and 
		child_board[2][7] == current_token and child_board[1][7] == current_token) or (child_board[2][8] == current_token and 
		child_board[2][7] == current_token and child_board[1][7] == current_token and child_board[1][6] == current_token and 
		child_board[0][6] == current_token) or (child_board[6][11] == current_token and child_board[6][10] == current_token and 
		child_board[5][10] == current_token and child_board[5][9] == current_token and child_board[4][9] == current_token):
			return self.player_id
		if self.is_board_full(child_board):
			return 0
		return 3
	def is_board_full(self, child_board):
		# Method to check if board is full
		for row in child_board:
			if '-' in row:
				return False
		return True
	def valid_moves(self, child_board):
		# Method that gets valid moves 
		valid_moves_list = []
		for i in range(0,len(child_board)):
			for j in range(0, len(child_board[i])):
				if child_board[i][j] == '-':
					valid_moves_list.append((i,j))
		return valid_moves_list
	def ai_best_move(self, depth, child_board, current_id):
		# Method that calls search to perform minimax and get the best move
		valid_moves_dict = {}
		best_score = -sys.maxint
		best_move = None
		opponent_id = 2 if current_id == 1 else 1
		for move in self.valid_moves(child_board):
			converted_move = self.convert_move(move)
			self.place_move(converted_move)
			temp_board = self.board
			valid_moves_dict[converted_move] = -self.search(depth-1, temp_board, opponent_id)
			self.remove_move(move)
		possible_moves = valid_moves_dict.items()
		for move, score in possible_moves:
			if score >= best_score:
				best_score = score
				best_move = move
		return best_move
	def search(self, depth, child_board, current_id):
		valid_moves = []
		best_score = -sys.maxint
		opponent_id = 2 if current_id == 1 else 1
		for move in self.valid_moves(child_board):
			converted_move = self.convert_move(move)
			self.place_move(converted_move)
			temp_board = self.board
			valid_moves.append(temp_board)
			self.remove_move(move)
		if depth == 0 or len(valid_moves) == 0 or self.check_winner(child_board) != 3:
			return self.get_score(child_board, current_id)
		for child in valid_moves:
			best_score = max(best_score, -self.search(depth-1, child, opponent_id))
		return best_score
	def get_score(self, child_board, current_id):
		opponent_id = 2 if current_id == 1 else 1

		current_two_patterns = self.find_two_pattern(child_board ,current_id)
		current_three_patterns = self.find_three_pattern(child_board ,current_id)
		current_four_patterns = self.find_four_pattern(child_board ,current_id)
		current_five_patterns = self.find_five_pattern(child_board ,current_id)

		opponent_five_patterns = self.find_five_pattern(child_board ,opponent_id)

		if opponent_five_patterns > 0:
			return -100000
		else:
			return current_five_patterns*100000 + current_four_patterns*10000 + current_three_patterns*100 + current_two_patterns
	def ai_place_move(self, depth):
		ai_move = self.ai_best_move(depth, self.board, self.player_id)
		self.place_move(ai_move)

	# The next four methods find two, three, four and five ladder patterns, respectively
	def find_two_pattern(self, child_board, player_id):
		num_of_two = 0
		for i in range(0,len(child_board)):
			for j in range(0, len(child_board[i])):
				try:
					if child_board[i][j] != '-' and child_board[i][j] != ' ' and ((self.player_id == 1 and child_board[i][j] == 'o') or (self.player_id == 2 and child_board[i][j] == 'x')):
						if (child_board[i][j] == child_board[i][j+1] or child_board[i][j] == child_board[i-1][j]):
							if ((j != 0 and j-1 != len(child_board[i])-1) and (i != 0 and i+1 != len(child_board)-1)):
								num_of_two += 1
						elif (child_board[i][j] == child_board[i][j-1] or child_board[i][j] == child_board[i+1][j]):
							if ((j != 0 and j-1 != len(child_board[i])-1) and (i != 0 and i+1 != len(child_board)-1)):
								num_of_two += 1
				except IndexError:
					pass
		return num_of_two
	def find_three_pattern(self, child_board, player_id):
		num_of_three = 0
		for i in range(0,len(child_board)):
			for j in range(0, len(child_board[i])):
				try:
					if child_board[i][j] != '-' and child_board[i][j] != ' ' and ((self.player_id == 1 and child_board[i][j] == 'o') or (self.player_id == 2 and child_board[i][j] == 'x')):
						if (child_board[i][j] == child_board[i][j+1] and child_board[i][j+1] == child_board[i-1][j+1]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i+1][j]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i-1][j]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j+1] == child_board[i+1][j+1]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j-1] == child_board[i+1][j-1]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j-1] == child_board[i-1][j-1]) or \
						(child_board[i][j] == child_board[i+1][j] and child_board[i][j] == child_board[i+1][j+1]):
							num_of_three += 1
				except IndexError:
					pass
		return num_of_three
	def find_four_pattern(self, child_board, player_id):
		num_of_four = 0
		for i in range(0,len(child_board)):
			for j in range(0, len(child_board[i])):
				try:
					if child_board[i][j] != '-' and child_board[i][j] != ' ' and ((self.player_id == 1 and child_board[i][j] == 'o') or (self.player_id == 2 and child_board[i][j] == 'x')):					
						if (child_board[i][j] == child_board[i][j+1] and child_board[i][j+1] == child_board[i-1][j+1] and
						child_board[i-1][j+1] == child_board[i-1][j+2]) or (child_board[i][j] == child_board[i][j+1] and 
						child_board[i][j] == child_board[i-1][j] and child_board[i][j] == child_board[i+1][j+1]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i+1][j+1] and
						child_board[i][j] == child_board[i+1][j+2]) or (child_board[i][j] == child_board[i][j+1] and 
						child_board[i][j] == child_board[i+1][j] and child_board[i][j] == child_board[i-1][j+1]):
							num_of_four += 1
				except IndexError:
					pass
		return num_of_four
	def find_five_pattern(self, child_board, player_id):
		num_of_fives = 0
		for i in range(0,len(self.board)):
			for j in range(0, len(self.board[i])):
				try:
					if self.board[i][j] != '-' and self.board[i][j] != ' ' and ((self.player_id == 1 and self.board[i][j] == 'o') or (self.player_id == 2 and self.board[i][j] == 'x')):					
						# check for right and left side ladder
						if (child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i-1][j+1] and
						child_board[i][j] == child_board[i-1][j+2] and child_board[i][j] == child_board[i-2][j+2]) or \
						(child_board[i][j] == child_board[i][j+1] and child_board[i][j] == child_board[i-1][j] and
						child_board[i][j] == child_board[i-1][j-1] and child_board[i][j] == child_board[i-2][j-1]):
							if child_board[i][j] == 'o':
								# check if neutralized by opponent
								if (child_board[i][j-1] == 'x' and child_board[i-2][j+1] == 'x') or \
								(child_board[i][j+2] == 'x' and child_board[i-2][j] == 'x'):
									pass
								else:
									num_of_fives += 1
							else:
								# check if neutralized by opponent
								if (child_board[i][j-1] == 'o' and child_board[i-2][j+1] == 'o') or \
								(child_board[i][j+2] == 'o' and child_board[i-2][j] == 'o'):
									pass
								else:
									num_of_fives += 1
				except IndexError:
					pass
		current_token = 'o' if self.player_id == 1 else 'x'
		if (child_board[6][12] == current_token and child_board[6][11] == current_token and child_board[5][11] == current_token and
		child_board[5][10] == current_token and child_board[4][10] == current_token) or (child_board[5][11] == current_token and 
		child_board[5][10] == current_token and child_board[4][10] == current_token and child_board[4][9] == current_token and 
		child_board[3][9] == current_token) or (child_board[4][10] == current_token and child_board[4][9] == current_token and 
		child_board[3][9] == current_token and child_board[3][8] == current_token and child_board[2][8] == current_token) or \
		(child_board[3][9] == current_token and child_board[3][8] == current_token and child_board[2][8] == current_token and 
		child_board[2][7] == current_token and child_board[1][7] == current_token) or (child_board[2][8] == current_token and 
		child_board[2][7] == current_token and child_board[1][7] == current_token and child_board[1][6] == current_token and 
		child_board[0][6] == current_token) or (child_board[6][11] == current_token and child_board[6][10] == current_token and 
		child_board[5][10] == current_token and child_board[5][9] == current_token and child_board[4][9] == current_token):
			num_of_fives += 1
		return num_of_fives
def main():
	Player1 = PolarizedLadder(1)
	Player2 = PolarizedLadder(2)
	Player1.populate_board(7,13)
	while True:
		game_type = raw_input("Select game type: 'CP', 'PC', 'PP', 'CC': ")
		if game_type == 'CP' or game_type == 'PC' or game_type == 'PP' or game_type == 'CC':
			break
	Player2.print_board()
	depth = 2
	while True:
		# Player 1 move
		if game_type == 'PC' or game_type == 'PP':
			while True:
				move = raw_input("Player 1 move: ")
				if Player1.place_move(move):
					break
		else:
			Player1.ai_place_move(depth)

		# Update board
		Player1.print_board()

		# Check game status
		if Player1.check_winner(Player1.board) == 1:
			print("Player 1 has won")
			break
		if Player1.check_winner(Player1.board) == 0:
			print("Game is a tie")
			break

		# Player 2 move
		if game_type == 'CP' or game_type == 'PP':
			while True:
				move = raw_input("Player 2 move: ")
				if Player2.place_move(move):
					break
		else:
			Player2.ai_place_move(depth)

		# Update board
		Player2.print_board()

		# Check game status
		if Player2.check_winner(Player2.board) == 2:
			print("Player 2 has won")
			break
		if Player1.check_winner(Player2.board) == 0:
			print("Game is a tie")
			break
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
