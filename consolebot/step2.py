import os
from textblob import TextBlob
import random
import logging
from filterWords import FILTER_WORDS

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]


# 定義「無法接受的語句」例外
class UnacceptableUtteranceException(Exception):
    """Raise this (uncaught) exception if the response was going to trigger our blacklist"""
    pass

def starts_with_vowel(word):
    """檢視代名詞的兼容性-- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False


def broback(sentence):
    """
    依據輸入的句子，選擇一個回應句
    """
    logger.info("Broback: respond to %s", sentence)
    resp = respond(sentence)
    return resp

#our first taste
def check_for_greeting(sentence):
    """
    If any of the words in the user's input was a greeting, return a greeting response
    如果任何使用者的輸入，有定義在我們的歡迎詞中，則返回歡迎回覆
    """
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)

# 如果程式不了解使用者的輸入，則由以下回覆挑選一句返回。
NONE_RESPONSES = [
    "uh whatever",
    "meet me at the foosball table, bro?",
    "code hard bro",
    "want to bro down and crush code?",
    "I'd like to add you to my professional network on LinkedIn",
    "Have you closed your seed round, dog?",
]

# 如果使用者試著告訴機器人關於機器人的事項，則隨機選擇以下一句回覆
COMMENTS_ABOUT_SELF = [
    "You are smart!",
    "I worked really hard on that",
    "My Klout score is {}".format(random.randint(100, 500)),
]

# 建構回覆句
def construct_response(pronoun, noun, verb):
    """
    在確認沒有特殊的輸入，則嘗試以使用者輸入的資料，來建構回覆句，
    """
    resp = []

    if pronoun:
        resp.append(pronoun)

    
    # 如果是動詞，則需處理英語的時態的處理，尤其是不規則動詞
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):  # 處理be動詞
            if pronoun.lower() == 'you':
                # 機器人只會回「他們不是」，無論使用者輸入什麼。
                resp.append("aren't really")
            else:
                resp.append(verb_word)
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "")))

    return " ".join(resp)

def check_for_comment_about_bot(pronoun, noun, adjective):
    """
    檢查是否使用者的輸入是否關於機器人本身，則回覆會依照輸入，返回最合適的回覆句，或者是空值。
    """
    resp = None
    if pronoun == 'I' and (noun or adjective):
        if noun:
            if random.choice((True, False)):
                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        else:
            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
    return resp

# 回覆模板，包括不可數名詞
SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "My last startup totally crushed the {noun} vertical",
    "Were you aware I was a serial entrepreneur in the {noun} sector?",
    "My startup is Uber for {noun}",
    "I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "Yeah but I know a lot about {noun}",
    "My bros always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "I'm personally building the {adjective} Economy",
    "I consider myself to be a {adjective}preneur",
]


def preprocess_text(sentence):
    """
    前處理，處理奇怪的輸入。例如：'i'，需要轉成大寫。
    """
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)

def respond(sentence):
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    resp = check_for_comment_about_bot(pronoun, noun, adjective)
    if not resp:
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb)
    if not resp:
        resp = random.choice(NONE_RESPONSES)

    filter_response(resp)
    return resp


def filter_response(resp):
    """
    濾掉所有在filter list的字（不雅字）
    """
    tokenized = resp.split(' ')
    for word in tokenized:
        if '@' in word or '#' in word or '!' in word:
            raise UnacceptableUtteranceException()
        for s in FILTER_WORDS:
            if word.lower().startswith(s):
                raise UnacceptableUtteranceException()


def find_candidate_parts_of_speech(parsed):
    """
    給予一個被解析後的輸入，尋找一個最適的代名詞、名詞、形容詞及動詞，來對應輸入。如果找不到，則回覆None
    """
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    #logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb

def find_pronoun(sent):
    """
    給予一個句字，找一個較合適的代名詞。如果沒有較合適的代名詞，則回覆None
    """
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # 岐義代名詞
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            # 如果使用者提到他們自己，則一定是用代名詞
            pronoun = 'You'
    return pronoun

def find_verb(sent):
    """
    選一個候選動詞
    """
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):  # 動詞
            verb = word
            pos = part_of_speech
            break
    return verb, pos


def find_noun(sent):
    """Given a sentence, find the best candidate noun."""
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':  # 這是名詞
                noun = w
                break
    if noun:
        logger.info("Found noun: %s", noun)

    return noun

def find_adjective(sent):
    """Given a sentence, find the best candidate adjective."""
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':  # 形容詞
            adj = w
            break
    return adj

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
