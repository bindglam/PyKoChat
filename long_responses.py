import random

def unknown():
    response = ["다시 대답해주세요...",
                "...",
                "이해하지 못 했어요..."][random.randrange(3)]
    return response