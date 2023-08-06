from enum import Enum
from subprocess import Popen, PIPE, STDOUT
from PythonChessLibrary.tools import *
import re, random, sys, berserk


class BasePlayer:
	def get_move(self, game):
		"""Method Documentation"""
		return

	def ask_draw(self, game):
		"""Method Documentation"""
		return

	def init(self):
		"""Method Documentation"""
		return

	def __init__(self, *args, **kwargs):
		self.debug = args[0]

		self.__dict__.update(kwargs)

		self.init()
		

class OnlinePlayer(BasePlayer):
	def get_move(self, game):
		print("getting move for online player")
		# wait for the online player to make a move and then report it
		for event in self.client.client.bots.stream_game_state(self.client.gameid):
			print(event)
			if event['type'] == 'gameState':
				return event['moves'].split(" ")[-1]

	def send_move(self, move):
		self.client.client.bots.make_move(self.client.gameid, move)

class UserPlayer(BasePlayer):
	def get_move(self, game):
		print("Input your move ---> ", end="")
		return input()

class RandomPlayer(BasePlayer):
	def get_move(self, chessnut):
		moves = chessnut.get_moves()
		if len(moves) == 0:
			print("Move History: " + str(chessnut.move_history), file=sys.stderr)
			print("fen string: " + str(chessnut.get_fen()), file=sys.stderr)
			print("_all_moves: " + str(chessnut._all_moves(player='b')), file=sys.stderr)
		dprint("Possible Moves: " + str(moves), self.debug)

		return moves[random.randint(0, len(moves)-1)]

class BotPlayer(BasePlayer):
	def get_move(self, game):
		# Choose a random starting move if we are testing with bots
		if hasattr(game, 'test_mode') and len(game.chessnut_game.move_history) == 0:
			valid_moves = game.chessnut_game.get_moves()
			return valid_moves[random.randint(0, len(valid_moves)-1)]

		# start a new game to be safe
		self.proc.stdin.write("ucinewgame\n")

		# give state
		self.proc.stdin.write("position fen " + game.chessnut_game.get_fen() + "\n")

		#tell it to search
		self.proc.stdin.write("go wtime 122000 btime 120000 winc 2000 binc 2000 depth 8\n")

		self.proc.stdin.flush()

		dprint("finding best move...", self.debug)

		#read in best move
		response = ""
		while not response.startswith("bestmove"):
			response = self.proc.stdout.readline()

		# Parse the response string
		move = response.split(" ")[1].strip()

		return move

	def init(self):
		engine_path = self.engine_path if self.engine_path else get_config_dict()['engine_path']
		self.proc = Popen([engine_path], stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding='UTF8')

		#read intro
		response = self.proc.stdout.readline()
		dprint(response, self.debug, end="")

		#tell it to use uci
		self.proc.stdin.write("uci\n")
		self.proc.stdin.flush()
		
		response = ""
		while response.strip() != "uciok":
			response = self.proc.stdout.readline()
			dprint(response, self.debug, end="")

		#setoptions if you want
		#setoption name Hash value 32
		#info string Hash table allocation: Windows large pages not used.

		#indicate ready
		self.proc.stdin.write("isready\n")
		self.proc.stdin.flush()
		response = self.proc.stdout.readline()
		if response.strip() != "readyok":
			#fucking panic or something idk
			print("Oh shit it aint ready coach. Engine said: ", response.strip())
			exit(0)

		#start new uci game
		self.proc.stdin.write("ucinewgame\n")