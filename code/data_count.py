import sys
from collections import defaultdict

def initials(input, initialDict):
    for line in input:
        line = line.decode('utf-8')
        #print line[0]
        initialDict[line[0]] += 1
    return initialDict

def bigrams(input,ngrams):
    for line in input:
        line= line.decode('utf-8')
        line = line.strip("\n")
        for k in range(0, len(line) - 1):
            char1 = line[k].encode('utf-8', 'ignore')
            char2 = line[k+1].encode('utf-8', 'ignore')
            if char1 not in ngrams.keys():
                ngrams[char1] = defaultdict(int)
            ngrams[char1][char2] += 1
            
    return ngrams

def createS(input,S):
    for line in input:
        line = line.decode('utf-8')
        for char in line:
            if char not in S:
                S.append(char)
    return S

def main():
    input = sys.argv[1]
    f = open(input, 'r').readlines()
    S = createS(f,[])
    #print S
    initialMatrix = defaultdict(int)
    pi = initials(f, initialMatrix)
    #print pi
    A = bigrams(f, {})
    print A
    
if __name__ == '__main__':
    main()
    