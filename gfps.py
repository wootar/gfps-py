import uuid, struct, serial

# Google Fast Pair Service service UUID
serviceuuid = uuid.UUID("df21fe2c-2515-4fdb-8886-f12c4d67927c")

msg_struct = ">BBH"

class Message():
	group = 0x00
	code = 0x00
	datalength = 0
	data = b""
	def __init__(self, group: int, code: int, datalength: int, data: bytes):
		self.group = group
		self.code = code
		self.datalength = datalength
		self.data = data
	def toPacket(self):
		return struct.pack(msg_struct+str(self.datalength)+"s",self.group,self.code,self.datalength,self.data)

ring_stop = 0x00
ring_mono = 0x01
ring_right = 0x01
ring_left = 0x02
ring_both = 0x03

def send(sr: serial.Serial, msg: Message):
	sr.write(msg.toPacket())
	resp = sr.read(4)
	length = struct.unpack(">H",resp[-2:])[0]
	resp += sr.read(length)
	return resp

def ring(sr: serial.Serial, type: int):
	msg = Message(0x04,0x01,1,str(type).encode("latin8"))
	return send(sr,msg)