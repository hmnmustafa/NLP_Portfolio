#This is the code I used to format and output the first 5 sentences of each important word into a file
import pickle

with open('knowledgeBase.pickle', 'rb') as handle:
    knowledgeDict = pickle.load(handle)

with open("KnowledgeBaseExample.txt",'w') as f:
    for key in knowledgeDict:
            f.write('\n' + key + ": " + '\n\n')
            for i in range(5):
                f.write(str(i+1) + ") " +  knowledgeDict[key][i] + ".\n")
                f.write('\n')
