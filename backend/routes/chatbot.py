import re
import logging
import uuid
import os
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import spacy

# Flask configuration
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify, make_response

# Langchain
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Helpers, Managers and other functions
from factory.limiter_factory import limiter
from factory import db
from schemas.chatbots import ChatbotSchema
from utils.content_utils import *
from services.logging_config import root_logger as logger
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from chatbots.managers.chatbot_manager import ChatbotManager
from chatbots.managers.message_manager import ChatMessageManger
from chatbots.managers.session_manager import ConversationSessionManager

load_dotenv()

# Function to register a new Chatbot
chatbot_blp = Blueprint("chatbot", "chatbot", url_prefix="/api/chatbots")
chatbot_schema = ChatbotSchema()

@chatbot_blp.route('/chatbots', methods=['POST'])
def create_chatbot():
    # Deserialize and validate the incoming JSON data
    try:
        chatbot_data = chatbot_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Initialize ChatbotManager with the current database session
    chatbot_manager = ChatbotManager(db.session)

    # Use the ChatbotManager to create a new Chatbot
    try:
        chatbot = chatbot_manager.create_chatbot(**chatbot_data)
        # Serialize the new chatbot instance for the response
        return chatbot_schema.dump(chatbot), 201
    except Exception as e:
        logger.error(f"Failed to create chatbot: {e}")
        return jsonify({"error": "Failed to create chatbot"}), 500

    # # Serialize the new chatbot instance for the response
    # return schema.dump(chatbot), 201

