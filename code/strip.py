# coding: UTF-8

import sys
import string

def main():
    f = open('alice.txt', 'r')
    n = open('alice_new.txt', 'w')
    
    for line in f:
        new = line.replace('。', '')
        new = new.replace('：','')
        new = new.replace('，','')
        new = new.replace('“','')
        new = new.replace('”', '')
        new = new.replace('’', '')
        new = new.replace('‘', '')
        new = new.replace('！', '')
        new = new.replace('（', '')
        new = new.replace('）', '')
        new = new.replace('？', '')
        new = new.replace('；', '')
        new = new.replace('《', '')
        new = new.replace('》', '')
        new = new.replace('……', '')
        new = new.replace('.', '')
        if new != ' \n':
            n.write(new)

    f.close()
    n.close()
    
if __name__ == "__main__":
    main()