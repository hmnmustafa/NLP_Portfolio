#Hamna Mustafa
#hbm170002
#CS4395

import sys
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

#function to process the tokens
def preprocessText(tokens):
    tokens = [t.lower() for t in tokens] #converting the tokens to lowercase
    #Reducing the tokens to only those that are alpha, not a stopword and have a length greater than 5
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    #get the lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    #make unique
    lemmas_unique = list(set(lemmas))

    #doing pos tagging on the unique lemmas
    tags = nltk.pos_tag(lemmas_unique)
    print("Tagged items after pos tagging:")
    print(tags[:20])

    #making a list of only those lemmas that are nouns
    nouns = [t[0] for t in tags if t[1][0] == "N"]
    print("Number of tokens: " + str(len(tokens)))
    print("Number of nouns: " + str(len(nouns)))

    return tokens, nouns

def introGame(lst): #this function will be called everytime a new word has to be guessed
    seed(1234)
    i = randint(0, len(lst)-1) #random integer that will be used as the index for the 50 most common words list
    word = lst[i]
    fill = [*"_"*len(word)] #creating the string with all blanks
    print("".join(fill))

    return fill, word

#this function deals with the guessing game functionality. It takes a list of words as a parameter, chooses a random word from that list and plays the guessing game with the user until they either quit or lose
def guessingGame(lst):

    print("\nLet's play a word guessing game!")

    points = 5 #starting points
    fill, word = introGame(lst) #choosing a new word
    while True:
        guess = input("Guess a letter: ")

        #if the user wants to quit the game
        if guess == '!':
            print("Sorry to see you go! Bye bye!")
            break

        #if the user has already guessed that letter and it has been filled
        elif guess in fill:
            print("That letter has already been filled!")

        #if the user enters without any input
        elif guess == "":
            print("You have to enter a letter!")

        #if the user guesses a correct letter
        elif guess in word:
            points+=1
            print("Right! Score is " + str(points))
            for i in range(0,len(word)): #updating the blanks with the correctly guessed letter
                if word[i] == guess:
                    fill[i] = guess

        #if the user guesses an incorrect letter
        else:
            points -= 1
            if points <= 0: #if the score becomes 0, then they have lost the game
                print("Sorry, you lost!")
                print("Game over! :(")
                break
            else:
                print("Sorry, guess again! Score is " + str(points))

        result = "".join(fill) #joining the list to make a string that is printed
        print(result)

        #if the user correctly guesses all the letters
        if result == word:
            print("\nCongratulations, you solved it! :D\n\nCurrent score: " + str(points))
            print("\nGuess another word:")
            fill, word = introGame(lst) #this will restart the game as a new word will be chosen


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: Filename was not provided")
        exit(1)

    #extracting filename from sysarg
    filename = sys.argv[1]
    with open(filename) as f:
        raw_text = f.read()

    #tokenizing the raw text and calculating the lexical diversity
    tokens = word_tokenize(raw_text)
    setTokens = set(tokens)
    lexicalDiversity = len(setTokens)/len(tokens)
    print("Lexical Diversity: %.2f" % lexicalDiversity)

    #processing the text
    tokens, nouns = preprocessText(tokens)

    #creating a dictionary with the nouns as the key and its count in the text as the value
    nounCount = {}
    for x in tokens:
        if x in nouns:
            if x in nounCount:
                nounCount[x] += 1
            else:
                nounCount[x] = 1

    print("\n50 most common words: ")

    #sorting by count and storing the 50 most common nouns in a list
    mostCommonNouns = sorted(nounCount, key=nounCount.get, reverse=True)[:50]

    #printing the 50 most common nouns
    for pos in mostCommonNouns:
        print(pos, ':', nounCount[pos])

    guessingGame(mostCommonNouns)







