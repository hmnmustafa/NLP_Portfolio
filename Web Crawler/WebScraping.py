#CS4395 Assignment 6
#Hamna B Mustafa
#hbm170002
from bs4 import BeautifulSoup
import requests
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import pickle

#this function takes a starter url and finds 20 other urls that are linked in the starter url
def webCrawler(starter_url):

    #extracting information from the starter url
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data,features="html.parser")

    #finding 20 relevant urls
    counter = 0
    print("Relevant URLs:")
    urlList = []
    for link in soup.find_all('a'): #this loop will loop over all hyperlinks
        link_str = str(link.get('href')) #convert to string
        if '&' in link_str: #formatting
            i = link_str.find('&')
            link_str = link_str[:i]
        #making sure the link is not another wikipedia page and is not a video. Also, ensuring it relevancy my checking that the link contains 'Hamilton'
        if 'wiki' not in link_str and 'video' not in link_str and ('Hamilton' in link_str or 'hamilton' in  link_str) and link_str.startswith('http'):
            print(link.get('href'))
            urlList += [link.get('href')]
            counter += 1
        if counter >= 20:
            break
    print("end of crawler")
    return urlList

def visible(element):
    #checking to see if the tag is visible and relevant
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a','button','b']:
        return False
    elif re.search('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def scrapeText(urlList):
    #iterating over all the urls extracted and scraping all their data and outputting it into a file
    i = 1
    urlFiles = []
    for link in urlList:
        r = requests.get(link)
        html = r.text
        soup = BeautifulSoup(html,features="html.parser")
        data = soup.findAll(text=True)
        result = filter(visible, data)  #filtering the data so only invisible and unnecessary data is filtered out
        temp_list = list(result)      # list from filter
        temp_str = ' '.join(temp_list)
        filename = 'url' + str(i) + ".txt"
        urlFiles += [filename]
        with open(filename, 'w') as f: #writing data to a file
            f.write(temp_str)
        f.close()
        i+=1

    return urlFiles #returning a list that contains all the file names that each url's data wad written into

def cleanupText(filename, i):
    #taking a file with raw data scraped from a url and cleaning it up
    with open(filename) as f:
        raw_text = f.read()
    f.close()

    raw_text = re.sub('<.*>', "",raw_text) #removing all text enclosed within <>
    raw_text = re.sub('END .*\n', "",raw_text) #removing text starting with 'END '
    raw_text = raw_text.replace('\n', "") #removing newlines
    raw_text = raw_text.replace('\t', "") #removing tabs
    raw_text = raw_text.replace('\r', "") #removing carriage returns
    sentences = sent_tokenize(raw_text) #tokening the text into sentences
    newFile = "cleanedUrl" +  i  +  ".txt"

    with open(newFile, 'w') as f: #writing the cleaned up data into a file
        for sentence in sentences:
            f.write(sentence)

    f.close()
    return newFile #returning the file with the cleaned file

def extractImportantTerms(filenames):
    #concatening all the text from all the cleaned files
    text = ''
    for file in filenames:
        with open(file) as f:
            text += f.read()
        f.close()

    #tokenizing the text and preprocessing
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens] #converting all tokens to lowercase
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')] #removing all stopwords and non-alpha words

    #creating a dictionary with the token is the key and its count in the text as the value
    tokenCount = {}
    for x in tokens:
        if x in tokenCount:
            tokenCount[x] += 1
        else:
            tokenCount[x] = 1

    #finding the 40 most commonly used words in the data
    mostCommonTokens = sorted(tokenCount, key=tokenCount.get, reverse=True)[:40]

    print("40 most important terms and their count:")
    for pos in mostCommonTokens:
        print(pos, ':', tokenCount[pos])

    return mostCommonTokens

def buildKnowledgebase(mostCommon, cleanedFiles):
    sentences = []

    #reading in the sentences from the cleaned files into a list
    for file in cleanedFiles:
        with open(file) as f:
            text = f.read()
        sentence = text.split(".")
        sentences += sentence

    #creating a knowledge base with the chose 10 important words as keys and the sentences in which those words appear as values
    knowledgeBase = {}
    for word in mostCommon: #iterating over the words
        for sentence in sentences: #iterating over the sentences
            if word in sentence or word.capitalize() in sentence: #checking if sentence contains the word
                #adding the sentence in the dictionary if it contains the word
                if word in knowledgeBase:
                    knowledgeBase[word] += [sentence]
                else:
                    knowledgeBase[word] = [sentence]

    return knowledgeBase



if __name__ == "__main__":
    #I chose the Hamilton musical's wikipedia page as my starter url
    starter_url = 'https://en.wikipedia.org/wiki/Hamilton_(musical)'

    urlList = webCrawler(starter_url) #finding relevant urls
    urlFiles = scrapeText(urlList) #scraping text from urls and writing them to files

    n = 1
    cleanUrls = []
    for f in urlFiles:
        cleanUrls += [cleanupText(f, str(n))] #cleaning the text
        n+=1

    extractImportantTerms(cleanUrls) #extracting the 40 most common words in the corpus

    print("From the above 40 words, choosing the following 10 because they are the most relevant:")
    #I chose the following 10 words from the most common 40 words because they seemed the most relevant and important
    commonWords = ['hamilton', 'miranda', 'musical', 'burr', 'history', 'broadway','culture','washington','theatre','america']
    print(commonWords)

    knowledgeBase = buildKnowledgebase(commonWords, cleanUrls) #building knowledge base
    with open('knowledgeBase.pickle', 'wb') as handle: #pickling the knowledge base
        pickle.dump(knowledgeBase, handle)



