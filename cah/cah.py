from .database import *
from .hand import *
from .game_server.server import start_server, stop_server
from .game_server.client import Client

class CAH:
	def __init__(self):
		self.db = DB('cah/cah-cards-full-official.json')
		self.mode = 'player' # 'host'
		self.client = None
		self.udp_server = None
		# default settings
		self.udp_port = 1234
		self.tcp_port = 1234
		self.room_capacity = 8

	def set_player(self, player):
		self.player = Hand(player, self.db)

	def start_server(self):
		self.udp_server, self.tcp_server = start_server(
			self.tcp_port, self.udp_port, self.room_capacity)

	def stop_server(self):
		if self.udp_server:
			self.udp_server.is_listening = False
			self.tcp_server.is_listening = False
			stop_server(self.udp_server, self.tcp_server)
		self.mode = None
		self.udp_server = self.tcp_server = None

	def stop_client(self):
		if self.client:
			self.client.leave_room()
			self.client.stop()
		self.mode = None
		self.client = None


	def list_rooms(self):
		rooms = self.udp_server.rooms
		print("Rooms :")
		for room_id, room in rooms.rooms.items():
			print("%s - %s (%d/%d)" % (room.identifier,room.name,len(room.players),room.capacity))

	def host(self):
		self.start_server()



	def join(self, mode='player'):
		if mode == 'host':
			self.start_server()
		if not self.client:
			self.client = Client('127.0.0.1', self.tcp_port,
				self.udp_port, self.udp_port + 1)
			self.set_player('test')
		if mode == 'host':
			self.client.create_room("Game Room")
		elif mode == 'player':
			self.client.autojoin()
		self.mode = mode
	







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
	game = CAH()
	game.set_player(['test'])
	game.run()

