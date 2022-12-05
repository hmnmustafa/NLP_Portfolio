#!/usr/bin/python
import socket
import json
import numpy as np
import pickle
import requests
import nltk

server = "irc.libera.chat"  # Server
channel = "#hamiltonFan"  # Channel
botnick = "TaraBot"  # nickname

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # Here we connect to the server using port 6667
ircsock.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " :Hamna bot\n", "UTF-8"))  # user authentication
ircsock.send(bytes("NICK " + botnick + "\n","UTF-8"))  # here we actually assign the nick to the bot

ircsock.send(bytes("JOIN " + channel + "\n","UTF-8"))



generalTags = ["greeting","goodbye","thanks","about","name","theirname","help","more"]

def send(channel, msg):
    # Transfer data
    ircsock.send(bytes("PRIVMSG " + channel + " :" + msg +'\r\n', "UTF-8"))

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def preprocess(msg, prevTag):



    if prevTag == 'name':
        new_msg = ""
        wordsList = nltk.word_tokenize(msg)
        tagged = nltk.pos_tag(wordsList)

        name = ""
        for tup in tagged:
            if tup[1] == 'NNP':
                name = tup[0]
                break
            new_msg += tup[0] + " "


        if not name:
            new_msg = ""
            for tup in tagged:
                if tup[1] == 'NN':
                    name = tup[0]
                    break
                new_msg += tup[0] + " "

        new_msg += "nnp"

        msg = new_msg

        userModel[userid]["name"] = name

    msg = msg.lower()


    data = query(
        {
            "inputs": {
                "source_sentence": msg,
                "sentences": training_sentences
            }
        })


    i = data.index(max(data))
    tag = training_labels[i]

    for t in knowledgeBase['knowledgeBase']:
        if t['tag'] == tag:
            response = np.random.choice(t['responses'])
            print("ChatBot:", response)

    if prevTag == 'name':
        response+=name

    prevTag = tag

    if tag not in generalTags:
        userModel[userid]["queries"] += [msg]
        userModel[userid]["responses"] += [response]



    return response,prevTag

def timeout():
    response = "User has left so I'm leaving too!"
    send(channel, response)

    with open('userData.pickle', 'wb') as f:
        pickle.dump(userModel, f)



if __name__ == "__main__":
    prevTag = ""
    api_token = "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"
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {api_token}"}

    with open("knowledgeBase.json") as file:
        knowledgeBase = json.load(file)

    with open('training_sentences.pickle', 'rb') as handle:
        training_sentences = pickle.load(handle)

    with open('training_labels.pickle', 'rb') as handle:
        training_labels = pickle.load(handle)

    try:
        userModel= pickle.load(open("userData.pickle", "rb"))
    except (OSError, IOError) as e:
        userModel = {}


    while 1:  # Be careful with these! it might send you to an infinite loop


        ircmsg = ircsock.recv(2048).decode("UTF-8")  # receive data from the server


        if "PRIVMSG" in ircmsg and channel in ircmsg:
            msgArr = ircmsg.split(":")
            content = msgArr[-1]

            userid = msgArr[1].split("@")[1].split(" ")[0]

            if userid not in userModel:
                userModel[userid] = {"name":"", "queries":[], "responses":[]}
            response, prevTag = preprocess(content, prevTag)
            send(channel, response)

        if "JOIN" in ircmsg and channel in ircmsg:
            msgArr = ircmsg.split(":")
            content = msgArr[-1]
            userid = msgArr[1].split("@")[1].split(" ")[0]
            greeting = "Hi there! It's nice to see you"
            rememberedFact = ''
            if userid in userModel:
                greeting += " again " + userModel[userid]["name"]
                if userModel[userid]["queries"] != []:
                    rememberedFact += userModel[userid]["queries"][-1]
            greeting += "!"
            print(userModel)



            send(channel, greeting)

            if rememberedFact:
                response = "I'm glad I could help you last time with your question:"
                send(channel, response)
                response =  rememberedFact
                send(channel, response)
                send(channel, "I hope I can help you today too!")



        if "QUIT" in ircmsg:
            timeout()
            exit()
