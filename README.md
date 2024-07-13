# gfps.py

### An Python library for Google's Fast Pair Service

# Why?

I just want wanna see my buds battery on PC

# Usage
`main.py` should ring each bud for 2 seconds

`daemon.py` is a daemon that wraps gfps.py into a nice little TCP server

# FastPain protocol

The FastPain uses TCP

Commands:
* 0x00 - Ring right/pair (Returns nothing)
* 0x01 - Ring left (Returns nothing)
* 0x02 - Ring both (Returns nothing)
* 0x03 - Ring stop (Returns nothing)
* 0x04 - Get battery percentage (Returns `<leftbud battery percentage>\n<rightbud battery percentage>\n<case battery percentage>`)