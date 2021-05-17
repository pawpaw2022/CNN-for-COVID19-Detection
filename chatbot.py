# Import libraries
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# import warnings
# warings.filterwarnings('ignore') # Avoid warning msgs showing up.

# Download the punkt package
# nltk.download('punkt', quiet= True)

# Get the article
article = Article('https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963')
# article = Article('https://en.wikipedia.org/wiki/COVID-19_pandemic_in_the_United_States')
article.download()
article.parse()
article.nlp()
corpus=article.text

# Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) # A list of sentences

# A function to return a random greeting response to a users greeting
def greeting_response(text):
    text = text.lower()

    # Bots greeting response
    bot_greetings = ['wassup', 'hi', 'hey', 'hello', 'nihao']
    # Users greeting
    user_greetings = ['hi', 'hey', 'hello', 'greetings', 'wassup', 'yo','nihao']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def age_response(text):
    text = text.lower()

    # Bots greeting response
    user_greetings = ['age', 'old']
    # Users greeting
    bot_greetings = ["My owner Paul is 21 years old!", "21 years old"]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def name_response(text):
    text = text.lower()

    # Bots greeting response
    user_greetings = ['name', 'who']
    # Users greeting
    bot_greetings = ["My name is Doc Bot", "You can call me Doc Bot.", "I am Doc Bot, your personal assistant."]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def joke_response(text):
    text = text.lower()

    # Bots greeting response
    user_greetings = ['joke', 'bored']
    # Users greeting
    bot_greetings = ["My wife said I should do lunges to stay in shape. That would be a big step forward.",
                     "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
                     "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along."]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


# Create the bots response
def bot_response(user_input):
    user_input = user_input.lower()  # lowercase the input
    sentence_list.append(user_input)  # append the msg to array
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)  # bag-of-word the msg
    similarity_scores = cosine_similarity(cm[-1], cm)  # calculate
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response += ' ' + sentence_list[index[i]]
            response_flag = 1
            j += 1

        if j > 2:
            break

    if response_flag == 0:
        bot_response += ' ' + "I am sorry, I don't understand that. "

    sentence_list.remove(user_input)
    bot_response = bot_response[:300]
    return bot_response


if __name__ == '__main__':
    # Start the chat
    print("Doc Bot: I am your personal medical assistant, Doc Bot. I will answer your queries about COVID-19 Disease. \nIf you want to exit, type 'bye'.")

    exit_list = ['exit', 'see you later', 'bye', 'quit', 'break', 'goodbye']

    while True:
        user_input = input()
        if user_input.lower() in exit_list:
            print('Doc Bot: Chat with you later ~')
            break
        else:
            if greeting_response(user_input) != None:
                print('Doc Bot: ' + greeting_response(user_input))

            elif age_response(user_input) != None:
                print('Doc Bot: ' + age_response(user_input))

            elif name_response(user_input) != None:
                print('Doc Bot: ' + name_response(user_input))

            elif joke_response(user_input) != None:
                print('Doc Bot: ' + joke_response(user_input))

            else:
                print('Doc Bot: ' + bot_response(user_input))