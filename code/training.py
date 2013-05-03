# coding: UTF-8
import cjklib
from cjklib.characterlookup import CharacterLookup

c = u'好'

cjk = CharacterLookup('T')
readings = cjk.getReadingForCharacter(c, 'Pinyin')
for r in readings:
    print r