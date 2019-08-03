import speech_recognition as sr
import pyaudio

EXIT_WHILE_THREE = 2

def EnterConstantListen():
    mic = sr.Microphone()
    r = sr.Recognizer()
    r.energy_threshold = 400
    print("開始無限收音，請講話")
    exit_counter = 0
    while 1:
        try:
            with mic as audio_source:
                speech_clip = r.listen(audio_source,timeout=4)
                regres = r.recognize_google(speech_clip,language='zh-TW')
                if regres=="離開程式":
                    print("謝謝使用。")
                    break
                else:
                    print(regres)
        except:
            print("google辨識發生問題，請別亂講話")
        finally:
            exit_counter += 1
            if exit_counter > EXIT_WHILE_THREE:
                print("已翻譯三次，離開程式")
                break
            else:
                print("請繼續講話")

        
            
            

def main():
    EnterConstantListen()


if __name__ == "__main__":
    main()