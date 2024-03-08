from flet import *
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')



client = OpenAI()


def chatgpt_response(content):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": content}
    ]
    )
    return response.choices[0].message.content


DEFAULT_PROMPTS = [
    ("Write a thank-you note", "\nto a guest speaker for my class"),
    ("Explain options trading", "\nif I'm familiar with buying and selling stocks"),
    ("Recommend a dish", "\nto impress a date who's a picky eater"),
    ("Suggest fun activities", "\nto help me make friends in a new city")
]


GREEN_COLOR = "#4ECF4B"
FONT_URL = "assets/fonts/Poppins-Regular.ttf"
LOGIN_IMAGE_URL = "assets/img/Rectangle 118.png"
AVATAR_IMAGE_URL = "assets/img/study.png"
RECEIVER_IMAGE_URL = "assets/img/carlos callas.png"
INCOME_VECTOR_URL = "assets/img/Income.png"
EXPENDITURE_VECTOR_URL = "assets/img/expenditure.png"
BACK_ARROW_IMAGE_URL = "assets/img/back-arrow.png"
FORWARD_ARROW_IMAGE_URL = "assets/img/forward-arrow.png"
SENDER_GRADIENT = ["#ff1b6b", "#45caff"]

OPTIONS = [
    (icons.CURRENCY_EXCHANGE, "Exchange"),
    (icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "Payments"),
    (icons.CREDIT_CARD_ROUNDED, "Credits"),
    (icons.CARD_GIFTCARD, "Plans"),
    (icons.PRICE_CHANGE_OUTLINED, "Overdraft"),
    (icons.GRID_VIEW, "More"),
]