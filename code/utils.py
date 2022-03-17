# -*- coding: utf-8 -*-
from gtts import gTTS
from playsound import playsound
import os
# from tempfile import NamedTemporaryFile
# import win32com.client as win
# import pyttsx3


def Text2Voice(text, language):
    fp = '.temp.mp3'
    tts = gTTS(text=text, lang=language)
    tts.save(fp)
    playsound(fp)
    # os.remove(fp)
    # gTTS(text=text, lang=language).write_to_fp(voice := NamedTemporaryFile())
    # playsound(voice.name)
    # voice.close()


def Text2Voice_v2(text):
    speak = win.Dispatch("SAPI.SpVoice")
    speak.Speak(text)


def Text2Voice_v3(text, language):
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # for item in voices:
    #     print(item.id, item.languages)
    if language == 'ch':
        engine.setProperty('voices', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    Text2Voice('hello','en')
    Text2Voice(u'你好', 'zh-cn')
    Text2Voice(u'こんにちは', 'ja')
