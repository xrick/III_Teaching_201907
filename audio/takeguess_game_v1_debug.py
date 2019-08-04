import random
import time
import speech_recognition as sr
import sys


def EnterGameLogic():

    WORDS = ["昂首闊步", "碧海青天", "拔刀相助", "安安穩穩", "奔走相告", "愛人以德"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    answer = random.choice(WORDS)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    instructions = (
        "請由以下的成語中猜中一個:\n"
        "{words}\n"
        "每次遊玩共有{n}機會。\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)
    # create recognizer and mic instances
    print(instructions)
    guess_counter = 0
    #prompt_counter= 0
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.energy_threshold = 300
    audio_clip = None
    if not isinstance(rec, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with mic as source:
        rec.adjust_for_ambient_noise(source)
        audio_clip = rec.listen(source)


    while 1:
        guess_counter += 1
        #print('進行第 {} 次猜看看. 請說：'.format(guess_counter))
        print("進行辨識,")
        guess = rec.recognize_google(audio_clip, language="zh-TW")
        res = response
        try: 
            res["transcription"] = guess
        except sr.RequestError:
            res["success"] = False
            res["error"] = "Google語音API無法使用"
        except sr.UnknownValueError:
            res["error"] = "您的輸入有問題，請重新啟動程式"
            #print(guess)
            if not res["success"]:
                break
            
        # 如果程式發生錯誤，跳出while-loop
        if res["error"]:
            print("發生錯誤: {}".format(res["error"]))
            break
            
        # 輸出玩家講的結果
        print("你/妳的答案: {}".format(res["transcription"]))
        #進行答案比對及計算使用者是否可以再繼玩
        guess_is_correct = res["transcription"] == answer
        user_has_more_attempts = guess_counter < NUM_GUESSES
        if guess_is_correct:
            print("答對了，恭喜你/妳獲得獎金：.......100萬(顆石頭)".format(answer))
            break
        elif user_has_more_attempts:
            print("不對喔，不過你/妳還有{}次機會.\n".format(guess_counter))
        else:
                print("抱歉，沒猜中耶，\n正確答案是: '{}'.".format(answer))
                break

if __name__=="__main__":
    EnterGameLogic()
