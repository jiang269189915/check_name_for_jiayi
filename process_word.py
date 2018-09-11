#encoding:utf-8
f =open("old_word.txt", 'rb')
word_list = set()
for line in f:
    line = line.strip().split()
    len1 = len(line[0])
    print len1
    i = 0
    ct = 0
    while i < len1 - 2:
       word = line[0][i:i+3]
       ct += 1
       i += 3
       if word not in word_list:
           word_list.add(word)
f.close()
f1 = open("word.txt", 'wb')
for word in word_list:
    print>>f1, word
f1.close()
