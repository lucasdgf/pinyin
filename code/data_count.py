import sys
from collections import defaultdict
from unidecode import unidecode

def initials(input, initialDict):
    for line in input:
        line = line.decode('utf-8')
        #print line[0]
        initialDict[line[0]] += 1
    return initialDict

def bigrams(input,ngrams):
    ngrams = {}
    for line in input:
        line= line.decode('utf-8')
        line = line.strip("\n")
        for k in range(0, len(line) - 1):
            char1 = line[k].encode('utf-8', 'ignore')
            char2 = line[k+1].encode('utf-8', 'ignore')
            if char1 not in ngrams:
                ngrams[char1] = {}
            if char2 not in ngrams[char1]:
                ngrams[char1][char2] = 1
            else:
                ngrams[char1][char2] += 1
            
    return ngrams

def createS(input,S):
    for line in input:
        line = line.decode('utf-8')
        for char in line:
            if char not in S:
                S.append(char)
    return S

def createO(input,O):
    for line in input:
        line = line.decode('utf-8')
        for char in line:
            pin = unidecode(char).lower().strip(' ')
            if pin not in O and pin.isalpha():
                O.append(pin)
    return O

def createB(input, O):
    B = {}
    for line in input:
        line = line.decode('utf-8')
        for char in line:
            if char not in B:
                B[char] = unidecode(char).lower().strip(' ')
    return B

def main():
    input = sys.argv[1]
    f = open(input, 'r').readlines()
    out = open("output.txt", "w")
    S = createS(f,[])
    O = createO(f,[])
    #out.write(str(S))
    initialMatrix = defaultdict(int)
    pi = initials(f, initialMatrix)
    #print pi
    A = bigrams(f, {})
    #out.write(str(A))
    B = createB(f, O)
    out.write(str(A))
    #print A

    
if __name__ == '__main__':
    main()
    