from flet import *
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')


def user_info(users, username):
    for user in users:
        if user["username"] == username:
            return user
