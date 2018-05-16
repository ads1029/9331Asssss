import sys
from socket import *
# from threading import *
import time
import threading

# source = int(sys.argv[1])
# succ1 = int(sys.argv[2])
# succ2 = int(sys.argv[3])

source = 3
succ1 = 4
succ2 = 5
pre_peer = []

port = source + 50000


print('the number of arg:', len(sys.argv)-1, f'the three element is:{source},{succ1},{succ2}' )


def send_request(s, succ1, succ2, from_peer):
    word = str(from_peer)
    s.sendto((word+'First').encode('utf-8'), ('127.0.0.1', succ1+50000))
    s.sendto((word+'Second').encode('utf-8'), ('127.0.0.1', succ2+50000))


def respond_request(s):
    global pre_peer

    data, addr = s.recvfrom(1024)
    target_port = int(addr[1])
    pp = str(int(addr[1]) - 50000)
    print('Here is target_port:', target_port)
    print('Here is port:', port)
    print(f'A ping request message was received from Peer', pp)

    # Add per_peer into list

    if pp not in pre_peer:
        pre_peer.append(pp)
    print('\n\nHere is the pre_peer list for now:',pre_peer,'\n\n')
    data = data.decode('utf-8')
    print(f'The word is: {data}')

    # s.sendto('GOTCHA'.encode('utf-8'),('127.0.0.1', addr[1]))


def check_file_name(f):
    # f = input('输入文件名：')
    # digdic = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    # print(len(f),'aadassdadasdasda')
    if len(f) != 4:
        print('Wrong length')
        return 0

    for i in f:
        try:
            int(i)
        except ValueError:
            print('input is not digit')
            return 0
    print('File is requesting...')
    return 1


def peer_departure(): # TODO
    pass


# TODO bulid TCPClient to find hashfile
def request_file(current_port, target_port):

    filename = input()
    print('This is your request filename', filename)
    if check_file_name(filename):
        # hash_file = str(int(filename) % 256)  # TODO put the process to server after receiving the msg
        print(f'File request message for {filename} has been sent to my successor.')
        tcpClient = socket(AF_INET, SOCK_STREAM)
        # tcpClient.bind(('', current_port))
        tcpClient.connect(('', target_port))
        tcpClient.send(filename.encode('utf-8'))

    else:
        if filename == 'quit':
            peer_departure()
        return


def respond_file(s, start_peer):
    global port
    conn, addr = s.accept()
    file_name = int(conn.recv(100).decode('utf-8'))
    file_hs = file_name % 256
    last_peer = int(addr[1]-40000) # current peer #  fixme  THIS IS NOT CURRENT!!! THIS IS THE LAST PEER!!!! HOW TO GET CURRENT? GLOBAL?
    current_peer = port - 50000
    print(file_hs)
    print(addr)
    print(addr[0],':',addr[1])
    print('TCP MSG RECEIVED.')

    if file_hs == current_peer:  # find the file. Display and sent msg back to start peer.
        pass
    elif file_hs > current_peer:  # not find yet. send msg to next peer
        if current_peer > last_peer:  # keep going.
        # if 1:
            pass
        else:  # already a loop. Stop and put the file at current peer.
            print(f'File {file_hs * 256 }')






# UDP Server-Client build.
udpS = socket(AF_INET, SOCK_DGRAM)
udpS.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # avoid waiting time
udpS.bind(('127.0.0.1', port))

# TCP Server build.
tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # avoid waiting time
tcpServer.bind(('', port))
tcpServer.listen(5)
print('TCP server waiting...')




print(f"Peer {source} is ready to receive message")



while 1:

    # FIXME 无法在等待respone时同时send request. FIXED: multithreading.


    # print(filename)
    # print('TESTING....')
    send_request(udpS, succ1, succ2, source)

    thread2 = threading.Thread(target=request_file, args=(port, succ1+40000))
    # thread2 = threading.Thread(target=request_file, args=(port,source))

    thread3 = threading.Thread(target=respond_file, args=(tcpServer,source))
    thread2.start()
    thread3.start()

    try:
        respond_request(udpS)
    except:
        pass

    time.sleep(10)




# class peer(threading.Thread):
#     def __init__(self, source, succ1, succ2, target=None, args=()):
#         super().__init__(target=target, args=args)
#         self.source = source
#         self.succ1 = succ1
#         self.succ2 = succ2
