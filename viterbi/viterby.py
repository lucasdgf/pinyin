# coding: UTF-8
from itertools import *
def argmax(pairs):
    return max(enumerate(x), key=lambda x:x[1])[0]

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
		T[1][state, 1] = pi[state] * B[state][Y[0]]
		T[2][state, 1] = 0
		#print "\ndelta1(" + str(state.encode('utf-8', 'ignore')) + ") = " + str(T[1][state, 1])
	#print "chosen: " + str(S[T[2][state, 1]].encode('utf-8', 'ignore'))

	for i in range(2, t + 1):
		#print "\ndelta " + str(i)
		for state in S:
			values = [T[1][x, i - 1] * A[x][state] * B[state][Y[i - 1]] for x in S]
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

O = ["hen", "wo", "ni"]
S = [x for x in u'恨你我很']
pi = {u"很": 0.1, u"我": 0.4, u"你": 0.4, u"恨": 0.1}
Y = ["wo", "hen", "hen", "ni"]
A = {}
A[u"我"] = {u"我": 0.0, u"很": 0.6, u"你": 0.1, u"恨": 0.3}
A[u"很"] = {u"我": 0.2, u"很": 0.0, u"你": 0.2, u"恨": 0.8}
A[u"你"] = {u"我": 0.2, u"很": 0.4, u"你": 0.0, u"恨": 0.4}
A[u"恨"] = {u"我": 0.4, u"很": 0.1, u"你": 0.4, u"恨": 0.1}

B = {}
B[u"我"] = {"wo": 1, "hen": 0, "ni": 0}
B[u"很"] = {"wo": 0, "hen": 1, "ni": 0}
B[u"你"] = {"wo": 0, "hen": 0, "ni": 1}
B[u"恨"] = {"wo": 0, "hen": 1, "ni": 0}

print viterbi(O,S,pi,Y,A,B)	
