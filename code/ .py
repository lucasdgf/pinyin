# coding: UTF-8
import sys
from unidecode import unidecode
from cjklib import characterlookup 

def to_pinyin(filename):
	try:
		input = open(filename, 'r').readlines()
	except IOError:
		print "IOError: could not open", filename
		sys.exit()

	cjk = characterlookup.CharacterLookup() 

	for line in input:
		line = line.decode('utf-8')
		new_line = ""
		for char in line:
			pinyin = cjk.getReadingForCharacter(char, 'Pinyin')
			if pinyin:
				simplified = unidecode(pinyin[0])
				new_line += simplified + char + " "
		line = new_line
		print line


to_pinyin("simplified.txt")