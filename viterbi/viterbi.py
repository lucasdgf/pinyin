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

def clean(input, output):
	try:
		text = open(input, 'r').readlines()
	except IOError:
		print "IOError: could not open", input
		sys.exit()
	out = open(output, 'w')
	for line in text:
		line = line.decode('utf-8')
		new_line = ""
		for char in line:
			pinyin = unidecode(char.strip('`'))
			if pinyin:
				new_line += pinyin.lower()
		new_line += '\n'
		out.write(new_line)
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

def precision(test, X):
	total = 0
	correct = 0
	X = X.decode('utf-8')
	for i in range(len(test)):
		if test[i] == X[i]:
			correct += 1
		total += 1
	print correct * 1.0 / total

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

	valid = False
	for state in S:
		if B[state] == Y[0]:
			valid = True
			Beta = 1
			T[1][state, 1] = (pi[state] + 1) * Beta if state in pi else Beta
			T[2][state, 1] = 0
	if valid == False:
		print Y[0] + " is not a syllable in Chinese Pinyin. Please try again."
		sys.exit()

	for i in range(2, t + 1):
		valid = False
		for state in S:
			if B[state] == Y[i - 1]:
				valid = True
				Beta = 1
				values = []
				for x in S:
					if (x, i - 1) in T[1]:
						if x in A:
							if state in A[x]:
								Alpha = A[x][state]
						else:
							Alpha = 0.5
						values.append(T[1][x, i - 1] * Alpha * Beta)
					else:
						values.append(0)
				T[2][state, i], T[1][state, i] = max(enumerate(values), key=lambda values:values[1])
		if valid == False:
			print Y[i - 1] + " is not a syllable in Chinese Pinyin. Please try again."
			sys.exit()

	Z = {}
	X = {}
	values = []
	for state in S:
		if (state, t) in T[1]:
			values.append(T[1][state, t])
		else:
			values.append(0)
	Z[t] = max(enumerate(values), key=lambda values:values[1])[0]
	X[t] = S[Z[t]].encode('utf-8', 'ignore')

	for i in range(t, 1, -1):
		if (S[Z[i]], i) in T[2]:
			Z[i - 1] = T[2][S[Z[i]], i]
		else:
			Z[i - 1] = 0
		X[i - 1] = S[Z[i - 1]].encode('utf-8', 'ignore')

	Y = ""
	for x in X:
		Y += X[x]

	return Y

def main():
	if len(sys.argv) < 3:
		print "usage: python viterby.py input.txt sequence_of_pinyin"
		print "example: python viterby.py alice_tokenized.txt ai li si"
		sys.exit()

	input = sys.argv[1]
	try:
		text = open(input, 'r').readlines()
	except IOError:
		print "IOError: could not open", input
		sys.exit()

	#tokenize(input, "tokenized.txt")

	S = createS(text,[])
	O = createO(text,[])
	pi = initials(text, {})
	A = bigrams(text, {})
	B = createB(text, {})
	Y = [y for y in sys.argv[2:]]
	X = viterbi(O, S, pi, Y, A, B)
	print X

	#precision(test, X)

    
if __name__ == '__main__':
    main()