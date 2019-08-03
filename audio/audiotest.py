import pyaudio
import speech_recognition as sr
from speech_recognition import Recognizer
from speech_recognition import Microphone

AUDIONAME='harvard.wav'
NOISEAUDIONAME='jackhammer.wav'
ZHAUDIONAME='mandarin01.flac'
"""
r.energy_threshold = 300 #設定多大能量上才會持續收聽
r.dynamic_energy_threshold = False
"""
def _Init_Test(audioname):
    return sr.AudioFile(audioname), Recognizer()

def googleRecognition(audioname):
    harvard_audio = sr.AudioFile(audioname)
    r = Recognizer()
    with harvard_audio as source:
        audio = r.record(source)
        #audio2 = r.record(source)
        #print("the audio type is {}".format(type(audio)))
         # or try zn-TW language='zn-CH'
        #print("Original content:{}".format(r.recognize_google(audio2)))

def googleRecognitionOffSet(audioname):
    harvard_audio, r = _Init_Test(audioname)
    with harvard_audio as source:
        audio = r.record(source,offset=6,duration=4)
        print(r.recognize_google(audio))

def googleRecognitionNoise(audioname):
    raw_audio, r = _Init_Test(audioname)
    with raw_audio as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        audio = r.record(source)
        print(r.recognize_google(audio))

def detectMicrophone():
    mic = sr.Microphone()
    #print(Microphone.list_microphone_names())
    with mic as audio_source:
        r = sr.Recognizer()
        print("Start to listen pls say something:")
        audio = r.listen(audio_source)
        result = r.recognize_google(audio,language='zh-TW')
        if not isinstance(result,dict) or len(result.get("alternative",[])):
            raise sr.UnknownValueError
            print("excute exception and return to here")
        print(reult)

def apprun(audio_name):
    try:
       detectMicrophone()
    except sr.UnknownValueError:
        print("error occured!")
    finally:
        print("Program is terminated")



if __name__ == "__main__":
    apprun(NOISEAUDIONAME)