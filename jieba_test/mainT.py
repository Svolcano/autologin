import jieba


a = "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
stop_words_dict = "stop_words.txt"
all_dict = set()
with open(stop_words_dict, 'r', encoding='utf-8') as fh:
    for i in fh:
        all_dict.add(i.strip())
jieba.load_userdict(stop_words_dict)
splited = jieba.cut(a, cut_all=False)
print(splited)
for e in splited:
    print(e, e in all_dict)