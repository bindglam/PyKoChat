import speech_recognition as sr
from gtts import gTTS
import vlc, requests, json

# tts 소리 재생
def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename='voice.mp3'
    tts.save(filename)
    p = vlc.MediaPlayer(filename)
    p.play()

#날씨 확인
def get_weather(city):
    apiKey = "06f034a3a4df1b7c639069a6aa5e5f9b"
    lang = 'kr' #언어
    units = 'metric' #화씨 온도를 섭씨 온도로 변경
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}&units={units}"

    result = requests.get(api)
    result = json.loads(result.text)

    return result