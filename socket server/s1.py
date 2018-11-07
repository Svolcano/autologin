from socket import socket, AF_INET, SOCK_STREAM
import re
import logging

no_conent = '0009900889900'


logging.basicConfig(filename="log.txt", format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger()


def get_content(line):
    if 'INSERT INTO' not in line:
        return no_conent
    conent = re.search(r'.*?[3|99],.*?,(.*)', line)
    if conent:
        c = conent.groups()[0]
        c = c.replace(');', '')
        return c
    return no_conent


def time_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    file_name = 'c.py'
    sock.listen(5)
    fh = open(file_name, 'r', encoding='utf-8')
    pos = 0
    done = False
    counter = 0
    while True:
        fh.seek(pos)
        peer, addr = sock.accept()
        while 1:
            try:
                line = fh.readline()
                pos = fh.tell()
                peer.send(line.encode('utf-8'))
                counter += 1
            except Exception as e:
                logger.info(e)
                break
            if done:
                break
        if done:
            break
    sock.close()
    fh.close()


if __name__ == '__main__':
    time_server(('', 9991))