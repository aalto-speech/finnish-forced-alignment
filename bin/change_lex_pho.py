#!/usr/bin/env python3

__author__ = 'jpleino1'
import collections
import unicodedata
import sys
from codecs import open
import csv

def main(corpus_file, phone_map_file):
    c = collections.Counter()
    for line in open(corpus_file, encoding='utf-8'):
        for word in line.split():
            c[word] += 1
    n = 0
    words_more_than_n = [k for k,v in c.items() if v > n]
    words_more_than_n.sort()

    reader = csv.reader(open(phone_map_file, encoding='utf-8'))
    phone_map = dict(reader)	
    dic_name = "lexicon.txt"
    dictionary_more_than_n = open(dic_name, "w",encoding='utf-8')
    dictionary_more_than_n.write(u"!SIL SIL\n")
    dictionary_more_than_n.write(u"<UNK> SPN\n")
    odd_characters = ['+', '!', '"', '(', ')', ',', '-', '.', ':', '?', '_', '‑', '—', "'", '=', "[", "]", "¤", "§"]
    for word in words_more_than_n:
        line = word
        line = unicodedata.normalize(u'NFC', line)
        if line.isdecimal() or line[1:].isdecimal() or line[:-1].isdecimal() or line[1:-1].isdecimal() or line[0] == '<' or line.lower() == '!sil':
            continue
        dictionary_more_than_n.write(line)
        if len(line) == 1 and (line in odd_characters):
            dictionary_more_than_n.write(u" SIL\n")
            continue
        for letter in line:
            if letter not in odd_characters:
                dictionary_more_than_n.write(u" " + phone_map[letter])
        dictionary_more_than_n.write(u"\n")

    dictionary_more_than_n.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
