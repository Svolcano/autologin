import os
import gensim
import jieba
import logging
import socket


def recv_all(sock):
    g_buf_len = 8092
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


def time_server(stop_file=None, address=('www.jingmeiti.com', 9991)):
    socket.setdefaulttimeout(1)
    stopwords = get_stopwords(stop_file)
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(address)
            while 1:
                sock.send(b'g ')
                line = recv_all(sock)
                if not line:
                    continue
                try:
                    line = line.decode()
                except Exception as e:
                    print(e)
                line = sentence2word(line, stopwords=stopwords)
                yield line
        except Exception as e:
            print('time server: ', e)
        finally:
            sock.close()


def get_stopwords(file_name):
    stop_wrods_set = set()
    with open(file_name, 'r', encoding='utf-8') as f:
        for word in f:
            word = word.strip()
            if word:
                stop_wrods_set.add(word)
    return stop_wrods_set


def sentence2word(sentence, stopwords=None):
    '''
    用结巴分词
    '''
    words = jieba.cut(sentence, cut_all=False)
    if stopwords is not None:
        words = [w for w in words if w not in stopwords and w!=' ']
    else:
        words = list(words)
    return words


class MySentences(object):
    def __init__(self, dirname, stopwords_fn=None):
        if stopwords_fn is not None:
            self.stopwords = get_stopwords(stopwords_fn)
        else:
            self.stopwords = None
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            f_with_name = os.path.join(self.dirname, fname)
            with open(f_with_name, 'r', encoding='utf-8') as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        line = sentence2word(line, stopwords=self.stopwords)
                        if line:
                            yield line


def train(sentences):
    # set up logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    stopwords_fn = 'stop_words.txt'
    model_fn = 'edu_word2vec.model'
    buf_size = 2000
    counter = 0
    save_counter = 0
    while 1:
        try:
            sentences = time_server(stop_file=stopwords_fn)
            lines_buf = []

            for line in sentences:
                lines_buf.append(line)
                counter += 1
                if counter >= buf_size:
                    if os.path.exists(model_fn):
                        model = gensim.models.Word2Vec.load(model_fn)
                        model.train(lines_buf)
                    else:
                        model = gensim.models.Word2Vec(sentences,
                                                   size=100,
                                                   max_vocab_size=8000000,
                                                   workers=8,
                                                   min_count=2,
                                                   )
                    save_counter += 1
                    model.save(model_fn)
                    lines_buf = []
                    counter = 0
                    print("save couner: %d" % save_counter)
        except Exception as e:
            print(e)


def use():
    # set up logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = gensim.models.Word2Vec.load('xajh_word2vec_model')
    for w in model.most_similar(u'侯亮平', topn=20):
        print(w[0], w[1])

    # ##
    # pos = [u'令狐冲', u'任盈盈']
    # neg = [u'岳灵珊']
    # for w in model.most_similar(positive=pos, negative=neg, topn=20):
    #     print(w[0], w[1])


if __name__ == "__main__":
    train(time_server())
