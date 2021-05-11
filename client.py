import socket,time
import errno
import select

class MySocket:


    def __init__(self, iptext, port=21701):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.setblocking(0)
        print('started')
        try:
            # r=self.check_socket()
            # if r:
            self.sock.connect((iptext,port))
            print('Connecting....')
        except:
            print('Cannot connect')
        try:
            # r = self.check_socket()
            # if r:
            self.sock.send('S'.encode())
            print('Connection SUCCESSFUL!!!!')
        except:
            print('failed to connect')

    def check_socket(self):
        r=[]
        while r == []:
            r,w,_ = select.select([self.sock],[self.sock],[],10)
        print('select YES: ',r,w,_)
        return r

    def get_data(self):
        # before = 0
        # after = 1

        # while before < after:
        #     data = self.sock.recv(16)
        #     after += len(data)
        #     before = after

            # print >> sys.stderr, 'received "%s"' % data
        r = self.check_socket()
        while True:

            try:

                # print(r)
                if r:
                    data = self.sock.recv(1024)
                    print(data.decode())
                    time.sleep(0.01)

            except:
                continue#print('get data error')

    def StrSend(self, s):
        try:
            self.sock.send(s.encode())
            while True:

                data_s = self.sock.recv(1024)
                data = data_s.decode()
                if data == 'USC':
                    continue
                #print('command = ',s,' response = ',data)
                return data
        except IOError as e:
            if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
                print("Reading error:{}".format(str(e)))
                self.clear_buffer()

        except socket.timeout:
            print("timeout")

    def StrSend1(self, s):
        buffer = ''

        try:
            data = ''
            self.sock.send(s.encode())
            while True:
                data_s = self.sock.recv(1024)

                if not data_s:
                    break
                buffer += data_s.decode()
                data = buffer
                print('command1 = ',s,' response1 = ',data)
            return data
        except socket.error:
            print("socket error")
            #self.clear_buffer()
        except socket.timeout:
            print("timeout")

    def clear_buffer(self):
        try:
            while self.sock.recv(1024): pass
        except:
            pass
        print('cleared buffer!')
#
# sock = MySocket('127.0.0.1')
# # for n in range(1,30):
# r =sock.check_socket()
# print(r)
# # #     #
# # # while True:
#
#     busy_matches = ['BUSY','BUSY.']
#     p_match = ['P']
#     d1 = sock.StrSend('GI')
#     if d1 != None:
#         l1 = d1.split(' ')
#         #print(l1)
#         if any(x in l1 for x in busy_matches):
#             pass#print('it\'s there!')
#         else:
#             if any(x in l1 for x in p_match):#print('not there my friend')
#                 d2 = sock.StrSend('S')
#                 d3 = sock.StrSend('G')
#
#                 print(d1,'  ',d2,'  ',d3)
#     time.sleep(0.2)