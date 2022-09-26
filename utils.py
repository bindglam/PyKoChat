from gtts import gTTS
from hanroman import KoreanToRoman
import vlc, requests, json

# tts 소리 재생
def speak(text):
    if not text == "...":
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
    # 도시 이름 그대로 영어로 번역하기 hanroman.py 출처 : https://hoze.tistory.com/2043, https://github.com/YiHoze/texwrapper/blob/master/hanroman.py
    KTR = KoreanToRoman()
    editcity = KTR.transcribe(city)
    api = f"https://api.openweathermap.org/data/2.5/weather?q={editcity}&appid={apiKey}&lang={lang}&units={units}"

    result = requests.get(api)
    result = json.loads(result.text)

    return result