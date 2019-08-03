import pyaudio
import speech_recognition as sr
from speech_recognition import Recognizer

AUDIONAME='harvard.wav'
NOISEAUDIONAME='jackhammer.wav'
ZHAUDIONAME='mandarin01.flac'

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



def apprun(audio_name):
   #googleRecognition(audio_name)
   #googleRecognitionOffSet(audio_name)
   googleRecognitionNoise(audio_name)


if __name__ == "__main__":
    apprun(NOISEAUDIONAME)