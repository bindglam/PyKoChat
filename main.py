# 필요 라이브러리 불러오기
from konlpy.tag import Hannanum
from hanroman import KoreanToRoman
from responses import ResponsesManager
from datetime import date
import utils, threading

class PyKoChat(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 변수 초기화
        self.user_name = input("유저 이름을 입력해주세요: ")
        self.hannanum = Hannanum()
        self.KTR = KoreanToRoman()
        self.responses = ResponsesManager(self.hannanum,self.KTR,self)

    def run(self):
        # 메인 루프
        while True:
            inp = self.responses.get_response(input("\n{}: ".format(self.user_name)))
            print("\nPyKoChat: " + inp)
            utils.speak(inp)

    # PyKoChat의 응답 설정하기
    def set_responses(self, message, response=None):
        response("오늘 날짜는 {}년 {}월 {}일 입니다.".format(date.today().year,date.today().month,date.today().day), ["오늘 날짜 알려줘", "오늘 며칠 이야", "오늘 날짜가 궁금해", "오늘 날짜 좀 알려줘" "오늘 날짜가 궁금해요"])
        if "날씨" in message: # 날씨에 관한 대답
            original_city_name = input("도시 이름을 입력해주세요: ")
            # 도시 이름 그대로 영어로 번역하기 hanroman.py 출처 : https://hoze.tistory.com/2043, https://github.com/YiHoze/texwrapper/blob/master/hanroman.py
            city_name = self.KTR.transcribe(original_city_name)
            response("입력된 {}의 날씨는 {} 이고, 최저 기온은 {}도, 최고 기온은 {}도 입니다. 따라서, 현재 평균 기온은 {}, 습도는 약 {}% 입니다."
                .format(original_city_name,utils.get_weather(city_name)['weather'][0]['main'],utils.get_weather(city_name)['main']['temp_min'],utils.get_weather(city_name)['main']['temp_max'],utils.get_weather(city_name)['main']['temp'],utils.get_weather(city_name)['main']['humidity']), 
                ["오늘 날씨 알려줘", "오늘 날씨", "오늘 날씨가 궁금해", "오늘 날씨 좀 알려줘", "오늘 날씨가 궁금해요"],required_words=["날씨"])

if __name__ == "__main__":
    chatbot = PyKoChat()
    chatbot.start()
