# coding: UTF-8
import sys
from itertools import *
from unidecode import unidecode
from cjklib.characterlookup import CharacterLookup

def tokenize(input, output):
	try:
		text = open(input, 'r').readlines()
	except IOError:
		print "IOError: could not open", input
		sys.exit()

	cjk = CharacterLookup('T')
	out = open(output, 'w')

	for line in text:
		line = line.decode('utf-8')
		new_line = ""
		for char in line:
			pinyin = cjk.getReadingForCharacter(char, 'Pinyin')
			if pinyin:
				new_line += char
		new_line += '\n'
		out.write(new_line.encode('utf-8'))
	out.close()

def initials(input, dict):
    for line in input:
        line = line.decode('utf-8')
        if line[0] not in dict:
        	dict[line[0]] = 1
        else:
        	dict[line[0]] += 1
    return dict

def bigrams(input, ngrams):
    for line in input:
        line = line.decode('utf-8').strip("\n")
        for k in range(0, len(line) - 1):
            char1 = line[k].encode('utf-8', 'ignore')
            char2 = line[k + 1].encode('utf-8', 'ignore')
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
            pin = unidecode(char).lower()
            if pin not in O:
                O.append(pin)
    return O

def createB(input, B):
    B = {}
    for line in input:
        line = line.decode('utf-8')
        for char in line:
            if char not in B:
                B[char] = unidecode(char).lower().strip(' ')
    return B

def viterbi(O, S, pi, Y, A, B):
	"""
		Implements Viterbi's algorithm and returns the most
		likely sequence of characters given a sequence of 
		pinyin syllables.

		Args:
			O: observation space (list of all possible pinyin)
			S: state space (list of all possible characters)
			pi: array of initial probabilities s.t. pi_i == P(x1 == s_i)
			Y: sequence of observations (pinyin text)
			A: transition matrix
			B: emission matrix

		Returns:
			X: list of states (pinyin text in characters)

		Raises:
			None
	"""

	# probabilities matrix
	T = {}
	T[1] = {}
	T[2] = {}
	t = len(Y)

	#print "delta 1:"
	for state in S:
		if B[state] == Y[0]:
			Beta = 1
		else:
			Beta = 0
		T[1][state, 1] = (pi[state] + 1) * Beta if state in pi else Beta
		T[2][state, 1] = 0
		#print "\ndelta1(" + str(state.encode('utf-8', 'ignore')) + ") = " + str(T[1][state, 1])
		#print "chosen: " + str(S[T[2][state, 1]].encode('utf-8', 'ignore'))

	for i in range(2, t + 1):
		#print "\ndelta " + str(i)
		for state in S:
			if B[state] == Y[i - 1]:
				Beta = 1
			else:
				Beta = 0
			values = []
			for x in S:
				if x in A:
					if state in A[x]:
						Alpha = A[x][state]
				else:
					Alpha = 0.5
				values.append(T[1][x, i - 1] * Alpha * Beta)
			T[2][state, i], T[1][state, i] = max(enumerate(values), key=lambda values:values[1])
			#print "\ndelta" + str(i) + "(" + str(state.encode('utf-8', 'ignore')) + ") = " + str(T[1][state, i])
			#print "chosen: " + str(S[T[2][state, i]].encode('utf-8', 'ignore'))

	Z = {}
	X = {}
	values = [T[1][state, t] for state in S]
	Z[t] = max(enumerate(values), key=lambda values:values[1])[0]
	X[t] = S[Z[t]].encode('utf-8', 'ignore')

	for i in range(t, 1, -1):
		Z[i - 1] = T[2][S[Z[i]], i]
		X[i - 1] = S[Z[i - 1]].encode('utf-8', 'ignore')

	Y = ""
	for x in X:
		Y += X[x]

	return Y

def main():
    input = sys.argv[1]
    try:
    	text = open(input, 'r').readlines()
    except IOError:
		print "IOError: could not open", input
		sys.exit()

    #tokenize("alice.txt", "alice_tokenized.txt")
    
    S = createS(text,[])
    O = createO(text,[])
    pi = initials(text, {})
    A = bigrams(text, {})
    B = createB(text, {})
    Y = ["wo", "shi", "zhong", "guo", "ren"]

    print viterbi(O, S, pi, Y, A, B)

    
if __name__ == '__main__':
    main()