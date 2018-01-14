import socket
port=8081
host='localhost'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)





s.sendto(b'55 aa 00 60 7b 22 63 6c 73 22 3a 22 74 61 67 22 2c 22 69 64 22 3a 32 33 2c 22 6c 61 79 65 72 5f 6e 61 6d 65 22 3a 22 65 67 6d 73 5f 31 31 30 22 2c 22 74 69 6d 65 22 3a 31 34 39 39 37 35 31 31 36 31 2c 22 6b 65 79 22 3a 22 63 6f 6f 72 64 69 6e 61 74 65 22 2c 22 76 61 6c 22 3a 22 31 2c 2d 35 30 22 7d',(host,port));

