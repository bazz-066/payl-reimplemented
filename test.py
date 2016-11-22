from paylmodel import PaylModel, ByteFrequency

gram1 = {'A':0.1818181818, 'B':0.0909090909, 'C':0, 'D':0.0909090909, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0.0909090909, 'J':0, 'K':0.0909090909, 'L':0, 'M':0.0909090909, 'N':0.0909090909, 'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0, 'U':0.1818181818, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0, ' ':0.0909090909}
gram2 = {'A':0.1333333333, 'B':0.1333333333, 'C':0, 'D':0.0666666667, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0.2, 'J':0, 'K':0.0666666667, 'L':0, 'M':0, 'N':0.0666666667, 'O':0, 'P':0.0666666667, 'Q':0, 'R':0, 'S':0, 'T':0, 'U':0.0666666667, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0, ' ':0.1333333333 }
gram3 = {'A':0.2222222222,'B':0.1111111111,'C':0,'D':0,'E':0,'F':0,'G':0.1111111111,'H':0.1111111111,'I':0.1111111111,'J':0.1111111111,'K':0,'L':0,'M':0,'N':0.1111111111,'O':0,'P':0,'Q':0,'R':0,'S':0,'T':0,'U':0,'V':0,'W':0,'X':0,'Y':0,'Z':0,' ':0.1111111111}

ngram1 = {}
ngram2 = {}
ngram3 = {}

for key, value in gram1.iteritems():
    if type(key) is str:
        ngram1[str(ord(key))] = gram1[key]

for key, value in gram2.iteritems():
    if type(key) is str:
        ngram2[str(ord(key))] = gram2[key]

for key, value in gram3.iteritems():
    if type(key) is str:
        ngram3[str(ord(key))] = gram3[key]

models = PaylModel(20, 200)
models.add_grams(ngram1)
models.add_grams(ngram2)

print models.distance(ngram3)


