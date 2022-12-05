import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import pickle

#this function takes in a filename and creates unigram and bigram dictionaries
def createUnigramBigram(filename):
    with open(filename, encoding='utf8') as f:
        raw_text = f.read()
    text = raw_text.replace('\n', "")
    s = ''.join(c for c in text if c.isalnum() or c == ' ')
    tokens = word_tokenize(s)

    #using nltk to make unigrams from tokens
    unigrams = ngrams(tokens, 1)

    #creating a dictionary with the unigram as keys and their count in the text as values
    unigram_dict = {}
    for unigram in set(unigrams):
      unigram_dict[unigram[0]] = text.count(unigram[0])


    #using nltk to make bigrams from tokens
    bigrams = list(ngrams(tokens, 2))

    #creating a dictionary with the bigram tokens as keys and their count in the text as values
    bigram_dict = {}
    for bigram in set(bigrams):
        if bigram not in bigram_dict:
            bi = bigram[0] + ' ' + bigram[1]
            bigram_dict[bi] = text.count(bi)




    return unigram_dict, bigram_dict


if __name__ == "__main__":
    enUnigramDict, enBigramDict = createUnigramBigram("LangId.train.English")
    itUnigramDict, itBigramDict = createUnigramBigram("LangId.train.Italian")
    frUnigramDict, frBigramDict = createUnigramBigram("LangId.train.French")


    #pickling the unigram and bigram dictionaries for the English training file
    with open('englishUnigram.pickle', 'wb') as handle:
        pickle.dump(enUnigramDict, handle)

    with open('englishBigram.pickle', 'wb') as handle:
        pickle.dump(enBigramDict, handle)

    #pickling the unigram and bigram dictionaries for the Italian training file
    with open('italianUnigram.pickle', 'wb') as handle:
        pickle.dump(itUnigramDict, handle)

    with open('italianBigram.pickle', 'wb') as handle:
        pickle.dump(itBigramDict, handle)

    #pickling the unigram and bigram dictionaries for the French training file
    with open('frenchUnigram.pickle', 'wb') as handle:
        pickle.dump(frUnigramDict, handle)

    with open('frenchBigram.pickle', 'wb') as handle:
        pickle.dump(frBigramDict, handle)
