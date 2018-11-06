# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 18:08:17 2017
读取语料库
转化词向量，保存为h5文件

@author: liang
"""
import sys
import os
import codecs
import multiprocessing
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from gensim.models.word2vec import LineSentence
from keras.preprocessing import sequence
np.random.seed(1337)
import jieba
#import pandas as pd
import logging
#jieba.load_userdict("newdict.txt")

sys.setrecursionlimit(1000000)
vocab_dim = 100   #训练完毕后词向量的维数
maxlen = 100
n_iterations = 1  #对每个输入词向量训练函数的句子迭代的次数，可以更大，会更慢...
                  #这可以理解为用来向训练函数中输入数据的迭代器的迭代次数
                  #通常情况下，训练函数第一次接收数据用来收集单词并计算词频
                  #第二次及以后，用来做神经网络训练。因为会迭代iterations+1次，
                  #所以至少为1。也可以更大，用以增加对每个输入的训练次数，但会更慢
                  #我在训练函数中，指明了build_vocab和train操作，所以就是训练一次
                  #这样做，而不是直接用gensim.models.Word2Vec(corpus)是为了
                  #可以处理输入数据不能重复的情况，扩展性更好
n_exposures=10
window_size=7
batch_size=32
n_epoch=4
input_length=100
cpu_count=multiprocessing.cpu_count()
#pool = multiprocessing.Pool(cpu_count)
#还可定义两个学习速率参数alpha和mini_alpha，会从alpha线性衰减到mini_alpha
#max_vocab_size 词典创建过程中，词汇量的最大值，每一千万词汇大概需要1G内存。默认值为没有限制
def stop_words(texts):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with codecs.open("stop_words.txt", encoding='utf-8') as f:
        str_text = f.read()
        # 把str格式转成unicode格式
        f.close()  # stopwords文本中词的格式是'一词一行'
    for word in word_generator:
        if word.strip() not in str_text:
            words_list.append(word)
    return ' '.join(words_list)  # 注意是空格

def loadcorpus():
    corpus=codecs.open('edu_sep.txt', 'a', 'utf-8')
    source=codecs.open("edu.txt", encoding='utf-8')
    line=source.readline()
    
    while line!="":        
        output=stop_words(line)
        corpus.write(output + ' ')
        line=source.readline()
    else:
        corpus.write('\r\n')
        source.close()
        corpus.close()
        
    return corpus

def corpus_dict(model=None,corpus=None):
    ''' 整理训练结果，重整词典
    '''
    
    if (corpus is not None) and (model is not None):
        gensim_dict=Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),allow_update=True)
        #计算在文档中，每个关键词出现的频率并用稀疏矩阵的方式返回结果。允许增加新的文档来更新这个稀疏矩阵
        w2indx = {v: k+1 for k, v in gensim_dict.items()}
        
        w2vec = {word: model[word] for word in w2indx.keys()}

        def rebuild_corpus(corpus):
           
            data=[]
            for sentence in corpus:
                new_txt=[]
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)
                data.append(new_txt)
            return data
        corpus=rebuild_corpus(corpus)
        #可用参数控制截断和填充从头开始还是从尾进行
        corpus=sequence.pad_sequences(corpus, maxlen=maxlen)
        return w2indx, w2vec,corpus
    else:
        print("没输入，你让我咋输出...")

def word2vec_train(corpus):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
 
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
    model = Word2Vec(LineSentence(corpus),
                     size=vocab_dim,
                     min_count=n_exposures,
                     window=window_size,
                     workers=cpu_count,
                     max_vocab_size=None,
                     batch_words=90000,
                     sg=1, hs=1,
                     iter=n_iterations)
#    model.build_vocab(corpus)
#    model.train(LineSentence(corpus),total_examples= corpus.corpus_count ,epochs=model.iter)
    model.save('edu_model.pkl')
#    index_dict, word_vectors,corpus = corpus_dict(model=model,corpus=corpus)
#    return   index_dict, word_vectors,corpus

def corpus_wv():
    print("Loading corpus...")
    corpus = codecs.open("edu_sep.txt", encoding='utf-8')
    # 未来语料库词典和停用词处理可整合到分词操作中
    #未来对训练结果需要进行进一步加工，放在这个函数后
    print("Training a Word2vec model of corpus...")
    word2vec_train(corpus)
    
    print("Vectors of corpus are built successfully.")


if __name__=='__main__':    
    corpus_wv()
    #loadcorpus()
