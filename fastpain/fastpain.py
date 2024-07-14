#!/usr/bin/env python3
import gfps, serial, time, json, os, socketserver, selectors, threading, sys

class EarbudsDisconnected(Exception):
    pass

print("Starting FastPain daemon")

# Parse jason's config
conf = {}
try:
	config = open(os.getenv("HOME")+"/.config/gfps.json")
	conf = json.loads(config.read())
	config.close()
except:
	print("No config file detected")

# Battery percentage
# 127 means unknown
# 0 = Left bud
# 1 = Right bud
# 2 = Case
battery = [127,127,127]

queue = []

gfps_serial = serial.Serial()

# FastPain protocol:
# 0x00 - Ring right/pair
# 0x01 - Ring left
# 0x02 - Ring both
# 0x03 - Ring stop
# 0x04 - Get battery percentage
class FastPain(socketserver.BaseRequestHandler):
	def handle(self):
		cmd_raw = self.request.recv(1)
		if len(cmd_raw) == 0:
			self.finish()
			return
		cmd = ord(cmd_raw)
		if cmd == 0x00:
			queue.append({"type": "ring", "mode": "right"})
		elif cmd == 0x01:
			queue.append({"type": "ring", "mode": "left"})
		elif cmd == 0x02:
			queue.append({"type": "ring", "mode": "both"})
		elif cmd == 0x03:
			queue.append({"type": "ring", "mode": "stop"})
		elif cmd == 0x04:
			self.request.send(f"{battery[0]}\n{battery[1]}\n{battery[2]}".encode("latin8"))
		self.request.close()
		self.finish()

def handleQueue():
	translation = {
		"left": gfps.ring_left,
		"right": gfps.ring_right,
		"both": gfps.ring_both,
		"pair": gfps.ring_mono,
		"stop": gfps.ring_stop,
	}
	try:
		msg = queue.pop()
	except IndexError:
		return
	if msg["type"] == "ring":
		mode = translation.get(msg["mode"])
		if mode == None:
			print(f"Got invalid ring mode: {msg['mode']}")
			return
		else:
			gfps.ring(gfps_serial,mode)
	else:
		print(f"Got invalid type: {msg['type']}")


tcp = socketserver.TCPServer(("127.0.0.1",8376),FastPain)
tcp.timeout = 0.1

def handleEarbuds():
	while True:
		try:
			msg = gfps.read_msg(gfps_serial)
			# Give chance to ^C the daemon
			time.sleep(0.01)
		except TypeError:
			msg = gfps.Message(512,0,0,b"")
			handleQueue()
		except serial.serialutil.SerialException:
			raise EarbudsDisconnected()
		tcp.handle_request()
		if msg.group == 0x03 and msg.code == 0x03:
			print("Got battery!")
			battery[0] = ord(msg.data[0:1])
			battery[1] = ord(msg.data[1:2])
			battery[2] = ord(msg.data[2:3])
			print(f"Left: {battery[0]}%")
			print(f"Right: {battery[1]}%")
			print(f"Case: {battery[2]}%")
		elif msg.group == 512:
			pass
		else:
			print(f"TODO: Packet {hex(msg.group)} {hex(msg.code)} {hex(msg.datalength)} {msg.data}")
try:
	if __name__ == "__main__":
		try:
			while True:
				try:
					gfps_serial = serial.Serial("/dev/rfcomm0",9600)
					gfps_serial.timeout = 0.1
					print("Connected to earbuds")
					try:
						handleEarbuds()
					except EarbudsDisconnected:
						print("Earbuds disconnected")
				except serial.serialutil.SerialException:
					pass
		except KeyboardInterrupt:
			print("Requested to exit")
finally:
	print("Stopping daemon")
	gfps_serial.close()
	tcp.server_close()