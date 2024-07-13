import gfps, serial, time, json, os

print("Starting FP daemon")

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

queue = [{
	"type": "ring",
	"mode": "both"
},{
	"type": "ring",
	"mode": "stop"
}]

print("Connecting to earbuds")

gfps_serial = serial.Serial("/dev/rfcomm0",9600)
gfps_serial.timeout = 0.1

print("Connected to earbuds")

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


while True:
	try:
		msg = gfps.read_msg(gfps_serial)
		# Give chance to ^C the daemon
		time.sleep(0.01)
	except TypeError:
		msg = gfps.Message(512,0,0,b"")
		handleQueue()
	if msg.group == 0x03 and msg.code == 0x03:
		print("Got battery!")
		battery[0] = ord(msg.data[0:1])
		battery[1] = ord(msg.data[1:2])
		battery[2] = ord(msg.data[2:3])
		print(battery)
	elif msg.group == 512:
		pass
	else:
		print(f"TODO: Packet {hex(msg.group)} {hex(msg.code)} {hex(msg.datalength)} {msg.data}")

print("Stopping daemon")
gfps_serial.close()