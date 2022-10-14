from database import *
from hand import *
from game_server.server import start_server, stop_server
from game_server.client import Client

class Game:
	def __init__(self):
		self.db = DB('cah-cards-full-official.json')
		self.play_mode = 'player' # 'host'
		# default settings
		self.udp_port = 1234
		self.tcp_port = 1234
		self.room_capacity = 3

	def set_player(self, player):
		self.player = Hand(player, self.db)

	def start(self):
		self.udp_server, self.tcp_server = start_server(
			self.tcp_port, self.udp_port, self.room_capacity)

	def stop(self):
		stop_server(self.udp_server, self.tcp_server)

	def start_game(self):
		if self.play_mode == 'host':
			self.start()
		self.client = Client('127.0.0.1', self.tcp_port,
			self.udp_port, self.udp_port + 1)


	def run(self):
		while True:
			black_card = self.db.draw('black')['text']
			print(black_card)
			select = [False] * black_card.count('_')
			count = 0
			while not select[-1]:
				action = input('>> ')
				if action == 'draw':
					self.player.draw()
				elif action == 'pick':
					select[count] = self.player.pick(0)
					count += 1
				elif action == 'hand':
					print(self.player.get_hand())
				elif action == 'q':
					break
			if action == 'q':
				break
			for selection in select:
				black_card = black_card.replace('_', selection['text'], 1)
			print(black_card)
			self.player.draw()
			print()
	


if __name__ == '__main__':
	game = Game()
	game.set_player(['test'])
	game.run()

