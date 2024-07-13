import gfps, serial, time, bluetooth, json, os

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

print("Connecting to earbuds")
try:
	gfps_serial = serial.Serial("/dev/rfcomm0",9600)
	gfps_serial.timeout = 0.1
except:
	if conf.get("earbuds") == None:
		print("No earbuds address provided")
		exit(1)
	matches = bluetooth.find_service(uuid=str(gfps.serviceuuid),address=conf["earbuds"])
	if len(matches) == 0:
		print("No fast pair service detected, exiting...")
		exit(1)
	fps = matches[0]
	print("Got", fps["name"], "(",fps["host"],")", fps["port"])
	gfps_serial = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	gfps_serial.connect((fps["host"],fps["port"]))

print("Connected to earbuds")

while True:
	try:
		msg = gfps.read_msg(gfps_serial)
		# Give chance to ^C the daemon
		time.sleep(0.01)
	except:
		msg = gfps.Message(512,0,0,b"")
	if msg.group == 0x03 and msg.code == 0x03:
		print("Got battery!")
		battery[0] = ord(msg.data[0:1])
		battery[1] = ord(msg.data[1:2])
		battery[2] = ord(msg.data[2:3])
		print(battery)
	elif msg.group == 512:
		# Ignore
		pass
	else:
		print(f"TODO: Packet {hex(msg.group)} {hex(msg.code)} {hex(msg.datalength)} {hex(msg.data)}")

print("Stopping daemon")
gfps_serial.close()