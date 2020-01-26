from collections import Counter
import nltk

document = 'We are, and always will be, the United States of America.'

#terms = document.split()
terms = nltk.word_tokenize(document)
terms_counter = Counter(terms)

for term in terms_counter:
    print('%s : %d회 출현' % (term, terms_counter[term]))



