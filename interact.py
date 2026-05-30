import socket
import telnetlib
import sys

def interact():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('chals.cyberjousting.com', 1370))
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

if __name__ == '__main__':
    interact()
