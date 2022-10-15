from .database import *
from .hand import *
from .game_server.server import start_server, stop_server
from .game_server.client import Client
import threading
from time import sleep

class CAH:
	def __init__(self, port):
		self.db = DB('cah/cah-cards-full-official.json')
		self.mode = 'player' # 'host'
		self.client = None
		self.player = None
		self.udp_server = None
		self.is_shut = False
		# default settings
		self.port = port
		self.udp_port = 1234
		self.tcp_port = 1234
		self.room_capacity = 8

	def set_player(self, player):
		self.player = Hand(player, self.db)


	def start_server(self):
		self.udp_server, self.tcp_server = start_server(
			self.tcp_port, self.udp_port, self.room_capacity)


	def _stop_server(self):
		self.is_shut = False
		while self.is_shut:
			sleep(0.1)
		if not self.udp_server:
			return
		self.udp_server.is_listening = False
		self.tcp_server.is_listening = False
		stop_server(self.udp_server, self.tcp_server)
		self.udp_server = self.tcp_server = None
		self.is_shut = True

	def stop_server(self):
		if self.udp_server:
			self.stop_thread = threading.Thread(target=self._stop_server)
			self.stop_thread.start()
		self.mode = None


	def _stop_client(self):
		while self.is_shut:
			sleep(0.1)
		if not self.client:
			return
		self.is_shut = False
		self.client.leave_room()
		self.client.stop()
		self.client = None
		self.player = None
		self.is_shut = True

	def stop_client(self):
		if self.client:
			self.stop_thread = threading.Thread(target=self._stop_client)
			self.stop_thread.start()
		self.mode = None


	def list_rooms(self):
		rooms = self.udp_server.rooms
		text = 'Rooms:\n'
		for room_id, room in rooms.rooms.items():
			text += ("%s - %s (%d/%d)" % (room.identifier,room.name,len(room.players),room.capacity))
		return text


	def _join(self, mode):
		while self.is_shut:
			sleep(0.1)
		if mode == 'host':
			self.start_server()
		if not self.client:
			self.client = Client('127.0.0.1', self.tcp_port,
				self.udp_port, self.port)
			self.set_player('test')
		if mode == 'host':
			self.client.create_room("Game Room")
		elif mode == 'player':
			self.client.autojoin()
		self.mode = mode

	def join(self, mode='player'):
		self.join_thread = threading.Thread(target=self._join, args=(mode,))
		self.join_thread.start()
	







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

