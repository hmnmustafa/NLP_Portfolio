import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

#this function takes in a sentence, along with the unigram and bigram count dictionaries of one language and the total vocab. It then computes the probability that the test sentence belongs to the given language
def calculateProb(test_sentence,unigram_dict, bigram_dict, V):

    tokens = word_tokenize(test_sentence)
    bigrams_test = list(ngrams(tokens, 2)) #create bigrams for the test sentence

    p_laplace = 1 #probability variable

    for bigram in bigrams_test: #loops over the test sentence bigrams and computes each bigrams probability with laplace smoothing
        b = bigram_dict[bigram] if bigram in bigram_dict else 0 #checks to see if the test bigram was present in the training set and updates b accordingly
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0 #checks to see if the first word of the bigram was present in the training set and updates u accordingly

        #the formula (b+1)/(u+v) is the probability formula with laplace smoothing, where b is the bigram count, u is the unigram count of the first word in the test bigram and V is the total vocabulary
        p_laplace = p_laplace * ((b + 1) / (u + V))

    return p_laplace


if __name__ == "__main__":

    #unpickling all the bigram and unigram dictionaries

    with open('englishUnigram.pickle', 'rb') as handle:
        enUnigramDict = pickle.load(handle)

    with open('englishBigram.pickle', 'rb') as handle:
        enBigramDict = pickle.load(handle)

    with open('italianUnigram.pickle', 'rb') as handle:
        itUnigramDict = pickle.load(handle)

    with open('italianBigram.pickle', 'rb') as handle:
        itBigramDict = pickle.load(handle)

    with open('frenchUnigram.pickle', 'rb') as handle:
        frUnigramDict = pickle.load(handle)

    with open('frenchBigram.pickle', 'rb') as handle:
        frBigramDict = pickle.load(handle)


#vocab is total number of unique words
vocab = len(frUnigramDict) + len(enUnigramDict) + len(itUnigramDict)
testfile = "LangId.test"

#reading in the sentences from the test file into a list
with open(testfile, encoding='utf8') as f:
    test_text = f.readlines()

f = open("Probability_predictions.txt", "w") #creating file to write predictions in

languages = ["English","Italian","French"]

with open('LangId.sol') as solFile: #reading in the solution file to compare out predictions with the actual solution
    solutionList = solFile.readlines()


i = 0
correct = 0
print('Incorrectly classified items:')
for line in test_text: #calculating the probabilites of the sentence belonging to each language
    line = ''.join(c for c in line if c.isalnum() or c == ' ')
    l = []
    l += [calculateProb(line, enUnigramDict, enBigramDict, vocab)]
    l += [calculateProb(line, itUnigramDict, itBigramDict, vocab)]
    l += [calculateProb(line, frUnigramDict, frBigramDict, vocab)]
    iL = l.index(min(l)) #finding the index of the min probability
    f.write(languages[iL] + '\n') #writing the language that corresponds to the min probability into the output file

    if (languages[iL] == solutionList[i].split()[1]): #checking to see if our prediction was correct
        correct+=1
    else:
        print("Line " + str(i+1))
    i+=1

accuracy = (correct/i)*100 #number of correctly predicted sentences over the total number of sentences
print("Accuracy: " + str(accuracy))

f.close()


