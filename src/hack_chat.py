import websocket
from time import sleep
from threading import Thread
from json import dumps, loads

class HackChat:
	def __init__(
			self,
			nickname: str,
			password: str = None,
			channel: str = "programming") -> None:
		self.channel = channel
		self.on_join = []
		self.on_leave = []
		self.on_message = []
		self.on_statistics = []
		self.online_users = []
		self.ws = websocket.create_connection("wss://hack.chat/chat-ws")
		self.nickname = f"{nickname}#{password}" if password else nickname
		self.send_packet(
			{
				"cmd": "join",
				"channel": self.channel,
				"nick": self.nickname
			}
		)
		Thread(target=self._ping_loop, daemon=True).start()

	def send_packet(self, packet: dict) -> None:
		self.ws.send(dumps(packet))

	def send_message(self, message: str) -> None:
		self.send_packet({"cmd": "chat", "text": message})

	def send_message_to(self, nickname: str, message: str) -> None:
		self.send_packet({"cmd": "whisper", "nick": nickname, "text": message})

	def change_nickname(self, nickname: str) -> None:
		self.nickname = nickname
		self.send_packet({"cmd": "changenick", "nick": nickname})

	def move_to_channel(self, channel: str) -> None:
		self.channel = channel
		self.send_packet({"cmd": "move", "channel": channel})

	def invite_user(self, nickname: str) -> None:
		self.send_packet({"cmd": "invite", "nick": nickname})

	def request_statistics(self) -> None:
		self.send_packet({"cmd": "stats"})

	def ban_user(self, nickname: str) -> None:
		"""REQUIRES: admin or moderator password"""
		self.send_packet({"cmd": "ban", "nick": nickname})

	def unban_user(self, user_ip: str) -> None:
		"""REQUIRES: admin or moderator password"""
		self.send_packet({"cmd": "unban", "ip": user_ip})

	def kick_user(self, nickname: str) -> None:
		"""REQUIRES: admin or moderator password"""
		self.send_packet({"cmd": "kick", "nick": nickname})

	def add_moderator(self, nickname: str) -> None:
		"""REQUIRES: admin or moderator password"""
		self.send_packet({"cmd": "addmod", "nick": nickname})

	def save_config(self) -> None:
		self.send_packet({"cmd": "saveconfig"})

	def listen(self) -> None:
		Thread(target=self._message_loop, daemon=True).start()

	def _message_loop(self) -> None:
		while True:
			response = loads(self.ws.recv())
			cmd = response["cmd"]
			if cmd == "chat":
				for handler in self.on_message:
					handler(self, response["text"], response["nick"])
			elif cmd == "onlineAdd":
				self.online_users.append(response["nick"])
				for handler in self.on_join:
					handler(self, response["nick"])
			elif cmd == "onlineRemove":
				self.online_users.remove(response["nick"])
				for handler in self.on_leave:
					handler(self, response["nick"])
			elif cmd == "onlineSet":
				self.online_users.extend(response["nicks"])
			elif cmd == "info" and response.get("type") == "whisper":
				for handler in self.on_message:
					handler(self, response["text"], response["from"], response)
			elif cmd == "info" and " IPs " in response["text"]:
				for handler in self.on_statistics:
					handler(self, response["text"])

	def _ping_loop(self) -> None:
		while self.ws.connected:
			self.send_packet({"cmd": "ping"})
			sleep(60)
