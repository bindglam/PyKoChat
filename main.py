# 필요 라이브러리 불러오기
from datetime import date
from konlpy.tag import Hannanum
from hanroman import KoreanToRoman
import random, json, utils, time
import long_responses as long

class ChatBot:
    def __init__(self):
        # 변수 초기화
        self.user_name = input("유저 이름을 입력해주세요: ")
        self.hannanum = Hannanum()
        self.KTR = KoreanToRoman()

        # 메인 루프
        while True:
            inp = self.get_response(input("\n{}: ".format(self.user_name)))
            print("\nPyKoChat: " + inp)
            utils.speak(inp)

    # 유저 입력 일치도 분석
    def message_probability(self, user_message, recognised_words, single_response=False, required_words=[]):
        intents_percentage = []
        for recognised_word in recognised_words:
            message_certainty = 0
            has_required_words = True
            
            for word in user_message:
                if word in recognised_word:
                    message_certainty += 1

            percentage = float(message_certainty) / float(len(recognised_word)) if message_certainty > 0 else 0

            for word in required_words:
                if word not in user_message:
                    has_required_words = False
                    break

            if has_required_words or single_response:
                intents_percentage.append(int(percentage*100))
            else:
                intents_percentage.append(0)
        return max(intents_percentage)

    # 인텐트, 대답 설정 및 알맞은 대답 고르기
    def check_all_messages(self, message):
        highest_prob_list = {}

        def response(bot_response, list_of_sentences, single_response=False, required_words=[]):
            nonlocal highest_prob_list
            sentences_words = []
            for sentence in list_of_sentences:
                sentencepos = self.hannanum.pos(sentence)
                lox = []
                for x in sentencepos:
                    if x[1] == "N" or x[1] == "M" or x[1] == "I":
                        lox.append(x[0])
                sentences_words.append(lox)
            highest_prob_list[bot_response] = self.message_probability(message, sentences_words, single_response, required_words)

        # 일반적인 인텐트(대답) 불러오기
        file_path = "intents.json"

        with open(file_path, "r") as fp:
            data = json.load(fp)

        for intent in data["intents"]:
            response(random.choice(intent["responses"]), intent["patterns"], single_response=intent["single_response"], required_words=intent["required_words"])

        response("오늘 날짜는 {}년 {}월 {}일 입니다.".format(date.today().year,date.today().month,date.today().day), ["오늘 날짜 알려줘", "오늘 며칠 이야", "오늘 날짜가 궁금해", "오늘 날짜 좀 알려줘" "오늘 날짜가 궁금해요"])
        if "날씨" in message: # 날씨에 관한 대답
            original_city_name = input("도시 이름을 입력해주세요: ")
            # 도시 이름 그대로 영어로 번역하기 hanroman.py 출처 : https://hoze.tistory.com/2043, https://github.com/YiHoze/texwrapper/blob/master/hanroman.py
            city_name = self.KTR.transcribe(original_city_name)
            response("입력된 {}의 날씨는 {} 이고, 최저 기온은 {}도, 최고 기온은 {}도 입니다. 습도는 약 {}% 입니다."
                .format(original_city_name,utils.get_weather(city_name)['weather'][0]['main'],utils.get_weather(city_name)['main']['temp_min'],
                utils.get_weather(city_name)['main']['temp_max'],utils.get_weather(city_name)['main']['humidity']), ["오늘 날씨 알려줘", "오늘 날씨", "오늘 날씨가 궁금해", "오늘 날씨 좀 알려줘", "오늘 날씨가 궁금해요"],required_words=["날씨"])
        
        best_match = max(highest_prob_list, key=highest_prob_list.get)
        #print(highest_prob_list)

        return long.unknown() if highest_prob_list[best_match] < 1 else best_match

    # 유저 입력 필요 부분만 걸러내기
    def get_response(self, user_input):
        isentencepos = self.hannanum.pos(user_input)
        message = []
        for x in isentencepos:
            if x[1] == "N" or x[1] == "M" or x[1] == "I":
                message.append(x[0])
        response = self.check_all_messages(message)
        time.sleep(1)
        return response

if __name__ == "__main__":
    chatbot = ChatBot()
