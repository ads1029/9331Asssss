import sys
from socket import *
from threading import *
import time

# source = int(sys.argv[1])
# succ1 = int(sys.argv[2])
# succ2 = int(sys.argv[3])

source = 5
succ1 = 1
succ2 = 3

port = source + 50000


print('the number of arg:', len(sys.argv)-1, f'the three element is:{source},{succ1},{succ2}' )


def send_request(s, succ1, succ2, from_peer):
    word = str(from_peer)
    s.sendto(word.encode('utf-8'), ('127.0.0.1', succ1+50000))
    s.sendto(word.encode('utf-8'), ('127.0.0.1', succ2+50000))


def respones_request(s):
    data, addr = s.recvfrom(1024)
    target_port = int(addr[1])
    print('Here is target_port:', target_port)
    print('Here is port:', port)
    print(f'A ping request message was received from Peer', int(addr[1]) - 50000)
    print(f'The word is: {data}')


s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # avoid waiting time
s.bind(('127.0.0.1', port))
print(f"Peer {source} is ready to receive message")

while 1:
    send_request(s, succ1, succ2, source) #跑不到

    try:
        respones_request(s)  #只会跑到这里 接收到request才会跑下面的
    except:
        pass
    # Timer(10, send_request(s, succ1, succ2).start())
    # print('TYRYAOIEJAS')
    time.sleep(5)  #跑不到
    '''
    无法在等待respone时同时send request
    '''

