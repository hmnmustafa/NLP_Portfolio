

import json
import pickle

if __name__ == "__main__":
    with open('knowledgeBase.json') as file:
        data = json.load(file)

    training_sentences = []
    training_labels = []
    labels = []
    responses = []


    for intent in data['knowledgeBase']:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)

            training_labels.append(intent['tag'])
        responses.append(intent['responses'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    print("Successfully created training data")

    with open('training_sentences.pickle', 'wb') as f:
        pickle.dump(training_sentences, f)

    with open('training_labels.pickle', 'wb') as f:
        pickle.dump(training_labels, f)


