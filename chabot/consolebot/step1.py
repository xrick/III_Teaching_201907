import os
from textblob import TextBlob
import random

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)



if __name__ == "__main__":
    inLoop = True
    answer = ""
    print("Hi, 你好！")
    while True:
        #check inLoop
        if not inLoop:
            exit()
        else:
            question = TextBlob(input('輸入:'))
            
        if question == 'quit':
            inLoop = False
            answer = "謝謝，下次見！"
        else:
            answer = check_for_greeting(question)
        print('A:{0}'.format(answer))