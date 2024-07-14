#!/bin/sh
inst() {
	echo "$1 -> $2"
	install -m=755 "$1" "$2"	
}

inst fastpain/fastpain.py /usr/lib/python3/dist-packages/fastpain.py
inst gfps.py /usr/lib/python3/dist-packages/gfps.py
inst fastpain/fastpain.service /usr/lib/systemd/system