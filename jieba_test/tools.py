
file_name = "xajh/edu_sepD01.txt"
file_name_out = "xajh/edu_sepD01_out.txt"
with open(file_name, 'r', encoding='utf-8') as fh:
    all = fh.read()
    all = all.split(' ')
    with open(file_name_out, 'w', encoding='utf-8') as wh:
        c = 20
        nc = 0
        t = []

        for e in all:
            t.append(e)
            nc += 1
            if nc == 80:
                wh.write(' '.join(t) + "\n")
                nc = 0
                t = []

        if t:
            wh.write(' '.join(t))
