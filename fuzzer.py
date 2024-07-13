import gfps, serial, time, random

print("GFPS fuzzer")

# Enable your dirtybud's fast pair serial for this
gfps_serial = serial.Serial("/dev/rfcomm0",9600)
gfps_serial.timeout = 0.1


try:
	while True:
		msg = gfps.Message(random.randint(0,255),random.randint(0,255),0,b"")
		print(f"Trying {msg.toPacket()}")
		try:
			print(gfps.send(gfps_serial,msg))
		except:
			print("No response from device")
			time.sleep(0.05)
finally:
	gfps_serial.close()