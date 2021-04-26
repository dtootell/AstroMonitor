import socket

class MySocket:


    # def __init__(self, host = '127.0.0.1',port = 21701):
    def __init__(self, iptext, port=21701):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((iptext,port))
        except:
            print('Cannot connect')
        try:
            self.sock.send('0'.encode())
            print('Connection SUCCESSFUL!!!!')
        except:
            print('failed to connect')

    def get_data(self):
        data = self.sock.recv(1024)
        return data.decode()

    def StrSend(self, s):
        self.sock.send(s.encode())
        data_s = self.sock.recv(1024)
        data = data_s.decode()
        return data

