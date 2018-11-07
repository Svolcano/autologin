from socket import socket, AF_INET, SOCK_STREAM
import re
import logging

no_conent = '0009900889900'


logging.basicConfig(filename="log.txt", format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger()

def send_line(sock, addr, line):
    total_len = len(line)
    buf_size = 8092
    while total_len:
        sock.send(line[:buf_size].encode('utf-8'))
        line = line[buf_size:]
        total_len = len(line)


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
    file_name = '../jmt_index_news_2.sql'
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
                line = get_content(line)
                if line == no_conent:
                    continue
                if not line:
                    logger.info("done")
                    done = True
                bytes = peer.recv(1024)
                logger.info(('G  :', bytes.decode('utf-8'), 'counter',  counter))
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