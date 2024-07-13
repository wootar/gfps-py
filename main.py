import gfps, serial, time

print("GFPS test")

# Enable your dirtybud's fast pair serial for this
gfps_serial = serial.Serial("/dev/rfcomm0",9600)

def ring_test(type):
	if type == gfps.ring_both:
		print("Now ringing both buds for 2 seconds")
	elif type == gfps.ring_left:
		print("Now ringing left bud")
	else:
		print("Now ringing right bud/pair for 2 seconds")
	print(gfps.ring(gfps_serial,type))
	time.sleep(2)
	print(gfps.ring(gfps_serial,gfps.ring_stop))

ring_test(gfps.ring_both)
ring_test(gfps.ring_left)
ring_test(gfps.ring_right)

gfps_serial.close()