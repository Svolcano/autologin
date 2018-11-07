import socket
import time
import json

socket.setdefaulttimeout(1)

g_buf_len = 8092

def recv_all(sock):
    new_line_buf = []
    while 1:
        try:
            new_line = sock.recv(g_buf_len)
            if new_line:
                new_line_buf.append(new_line)
        except Exception as e:
            print(e)
            return (b''.join(new_line_buf))
    return (b''.join(new_line_buf))


def time_server(address):
    out = open("test.txt", 'w', encoding='utf-8')
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        buf_len = 20
        buf = []
        while buf_len:
            sock.send(b'go on')
            line = recv_all(sock)
            if not line:
                continue
            try:
                line = line.decode()
            except Exception as e:
                print(e)
            yield line
            buf_len -= 1
        sock.close()
    out.close()


if __name__ == '__main__':
    lines = time_server(('47.95.210.95', 9991))
    ln = 0
    for line in lines:
        print("line number : ", ln, line)
        ln += 1