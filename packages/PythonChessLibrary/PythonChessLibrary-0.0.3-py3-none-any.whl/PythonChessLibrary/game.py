from subprocess import Popen, PIPE, STDOUT
import sys
from PythonChessLibrary.tools import dprint
from PythonChessLibrary.player import *

# Dependencies to install
from Chessnut import Game

class BasicGame:
	def get_move_list(self):
		move_str = ''
		for m in self.chessnut_game.move_history:
			move_str += m + " "
		return move_str.strip()

	def make_move(self):
		# ask the player for the move
		m = self._get_move(self.turn)

		# update internal board
		moved_piece, taken_piece, castled = self._update_board(m)

		# Tell online opponent of move if necessary
		if self.turn == self.white_player and isinstance(self.black_player, OnlinePlayer):
			self.black_player.send_move(m)
		if self.turn == self.black_player and isinstance(self.white_player, OnlinePlayer):
			self.white_player.send_move(m)

		# Move to next turn if it didn't fail
		self.turn = self.black_player if self.turn == self.white_player else self.white_player

		return m

	def _get_move(self, player):
		# Get move from player
		global is_valid
		is_valid = False
		m = None
		while not is_valid:
			m = player.get_move(self)
			print("Suggested Move: " + str(m))

			# Put exceptions for user commands such as forfeit and exit
			if m == 'exit' or m == 'ff' or m == 'draw':
				return m

			if m in self.chessnut_game.get_moves():
				self.chessnut_game.apply_move(m)
				is_valid = True
			else:
				dprint("Proposed move: " + m, self.debug)
				dprint("Valid moves: " + str(self.chessnut_game.get_moves()), self.debug)
				dprint("Fen: " + str(self.chessnut_game.get_fen()), self.debug)
				print("Invalid move, try again.")

		return m

	def _update_board(self, m):
		# Update internal board
		moved_piece = None
		taken_piece = None

		## Calculate where the piece is coming and going
		col_from = ord(m[0]) - 97
		row_from = (int(m[1])-4)*-1 + 4
		index_from = row_from*8 + col_from

		col_to = ord(m[2]) - 97
		row_to = (int(m[3])-4)*-1 + 4
		index_to = row_to*8 + col_to

		## Move the piece
		moved_piece = (self.chess_board[index_from], index_from)
		taken_piece = (self.chess_board[index_to], index_to)
		self.chess_board[index_to] = self.chess_board[index_from]
		self.chess_board[index_from] = ""

		## In en_passant, the taken piece must be manually removed
		if self.chess_board[index_to].lower() == 'p' and not taken_piece[0]:
			if self.turn == self.white_player:
				taken_piece = (self.chess_board[index_to + 8], index_to+8)
				self.chess_board[index_to + 8] = ""
			else:
				taken_piece = (self.chess_board[index_to - 8], index_to-8)
				self.chess_board[index_to - 8] = ""

		## If castling, move the rook as well
		if self.chess_board[index_to].lower() == 'k' and abs(col_from - col_to) == 2:
			if col_to - col_from < 0:
				castled = 'a' + m[1] + 'd' + m[1]
			else:
				castled = 'h' + m[1] + 'f' + m[1]

			c_col_from = ord(castled[0]) - 97
			c_row_from = (int(castled[1])-4)*-1 + 4
			c_index_from = c_row_from*8 + c_col_from

			c_col_to = ord(castled[2]) - 97
			c_row_to = (int(castled[3])-4)*-1 + 4
			c_index_to = c_row_to*8 + c_col_to

			### Create something to the arm to process
			castled = (castled, (self.chess_board[c_index_from], c_index_from), (self.chess_board[c_index_to], c_index_to))

			### Move the rook
			self.chess_board[c_index_to] = self.chess_board[c_index_from]
			self.chess_board[c_index_from] = ""

		else:
			castled = None
			
		## If we have a promotion, promote it
		if len(m) == 5:
			self.chess_board[index_to] = m[4] if self.turn == self.black_player else m[4].upper()


		# ((b, 34), (Q, 42), None)
		# ((K, 59), ("", 61), (h1f1, (R, 63), ("", 60)))
		return moved_piece, taken_piece, castled

	def is_over(self):
		dprint("Game Status: " + str(self.chessnut_game.status), self.debug)
		return self.chessnut_game.status > 1

	def print_board(self):
		for row in range(8):
			print(((row-4)*-1 + 4), '', end='')
			for col in range(8):
				piece = self.chess_board[row*8 + col]
				print(piece if piece else '-', "", end="")
			print()
		print("  a b c d e f g h")


	def __init__(self, white_player, black_player, debug=False):
		# Ensure both players derive from BasePlayer
		if not isinstance(white_player, BasePlayer) or not isinstance(black_player, BasePlayer):
			print("Both player objects must derive from BasePlayer.")
			quit()

		self.white_player = white_player
		self.black_player = black_player
		self.turn = white_player

		self.chess_board =["r", "n", "b", "q", "k", "b", "n", "r", 
						   "p", "p", "p", "p", "p", "p", "p", "p", 
						   "",  "",  "",  "",  "",  "",  "",  "", 
						   "",  "",  "",  "",  "",  "",  "",  "", 
						   "",  "",  "",  "",  "",  "",  "",  "", 
						   "",  "",  "",  "",  "",  "",  "",  "", 
						   "P", "P", "P", "P", "P", "P", "P", "P", 
						   "R", "N", "B", "Q", "K", "B", "N", "R"]

		self.chessnut_game = Game()

		self.debug = debug


class ChessBuddyGame(BasicGame):
	def _get_move(self, player):
		# Get move from player
		global is_valid
		is_valid = False
		m = None
		while not is_valid:
			m = player.get_move(self)
			print("Player Move: " + str(m))

			# Put exceptions for user commands such as forfeit and exit
			if m == 'exit' or m == 'ff' or m == 'draw':
				return m

			if m in self.chessnut_game.get_moves():
				self.chessnut_game.apply_move(m)
				is_valid = True
			else:
				dprint("Proposed move: " + m, self.debug)
				dprint("Valid moves: " + str(self.chessnut_game.get_moves()), self.debug)
				dprint("Fen: " + str(self.chessnut_game.get_fen()), self.debug)
				print("Invalid move, try again.")

		return m

	def __init__(self, white_player, black_player, debug=False):
		BasicGame.__init__(white_player, black_player, debug=debug)

		# Ensure there is exactly one ChessBuddyPlayer and that both are a Base Player
		if not ((isinstance(white_player, ChessBuddyPlayer) and not isinstance(black_player, ChessBuddyPlayer)) or (not isinstance(white_player, ChessBuddyPlayer) and isinstance(black_player, ChessBuddyPlayer))):
			print("There must be exactly one ChessBuddyPlayer. Watch mode (two remote players) not supported yet.")




