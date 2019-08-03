import pyaudio
import speech_recognition as sr
from speech_recognition import Recognizer

AUDIONAME='harvard.wav'

def googleRecognition(audio):
    harvard_audio = sr.AudioFile('harvard.wav')
    with harvard_audio as source:
        r = Recognizer()
        audio = r.record(source)
        #print("the audio type is {}".format(type(audio)))
        print(r.recognize_google(audio))


def apprun(audio_name):
   googleRecognition(audio_name)


if __name__ == "__main__":
    apprun(AUDIONAME)