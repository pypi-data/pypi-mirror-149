from .wrapper import *
import requests as r
import websocket, json, rel, time, threading, sys

class Bot:
	URL = "://rmtrollbox.eu-gb.mybluemix.net/"
	events = {}
	sid = None
	HEARTBEAT = 0
	ws = None
	def __init__(self, name, color, bot=True):
		self.name = name
		self.color = color
		self.bot = bot
	def _ping(self, ws):
		while True:
			time.sleep(self.HEARTBEAT/1000)
			ws.send("2")
	def event(self, func):
		self.events[func.__name__] = func
	def _message(self, ws, msg):
		if msg == "3probe":
			ws.send("5")
		else:
			data = json.loads(msg[2:])
			if data[0] == "connectdata":
				try:
					connection = json.dumps([
						"user joined",
						self.name,
						self.color,
						self.bot
					])
					ws.send("42"+connection)
					try:
						self.events["connect"]()
					except:
						pass
				except Exception as e:
					# print(str(e))
					pass
			else:
				ev = converter.e2f[data[0]]
				self.events[ev](data[1])
	def _error(self, ws, err):
		pass
	def _close(self, ws, status, msg):
		print("Disconnected", status, msg)
		sys.exit()
	def _open(self, ws):
		ws.send("2probe")
		self.ws = ws
		self.pingt = threading.Thread(target=self._ping,args=(ws,),daemon=True)
		self.pingt.start()
	def run(self):
		stuff = json.loads(r.get("https"+self.URL+"socket.io/?EIO=3&transport=polling").text[4:-4])
		self.sid = stuff["sid"]
		self.HEARTBEAT = stuff["pingInterval"]
		ws = websocket.WebSocketApp("wss"+self.URL+"socket.io/?EIO=3&transport=websocket&sid="+self.sid,
                              on_open=self._open,
                              on_message=self._message,
                              on_error=self._error,
                              on_close=self._close)
		ws.run_forever(dispatcher=rel)
		rel.signal(2, rel.abort)
		rel.dispatch()
	############
	def rename(self, nick, col, bot=True):
		self.ws.send("42"+json.dumps([
			"user joined",
			nick,
			col,
			bot
		]))
		self.name = nick
		self.color = col
		self.bot = bot
	def send(self, content):
		self.ws.send("42"+json.dumps([
			"message",
			content
		]))
	def delete(self):
		self.ws.send("42"+json.dumps([
			"delet"
		]))
	def editlast(self, new):
		self.ws.send("42"+json.dumps([
			"edit",
			new
		]))
	def edit(self, id, new):
		self.ws_send("42"+json.dumps([
			"edit_ownid",
			id,
			new
		]))
	def start_typing(self):
		self.ws_send("42"+json.dumps([
			"type",
			True
		]))
	def stop_typing(self):
		self.ws_send("42"+json.dumps([
			"type",
			False
		]))
	def react(self, ID, img):
		self.ws_send("42"+json.dumps([
			"react",
			ID,
			img
		]))
	def unreact(self, ID, img):
		self.ws_send("42"+json.dumps([
			"unreact",
			ID,
			img
		]))
	def request_rooms(self):
		self.ws_send("42"+json.dumps([
			"room_list"
		]))
	def request_current_room(self):
		self.ws_send("42"+json.dumps([
			"room_current"
		]))
	def join_room(self, name, passwd=None):
		self.ws_send("42"+json.dumps([
			"room_join",
			name,
			passwd
		]))
	def create_room(self, name, passwd=None):
		self.ws_send("42"+json.dumps([
			"room_create",
			name,
			passwd
		]))