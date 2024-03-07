import os
from factory import create_app
from factory import db 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
# from chatbots.sessions.session_manager import ConversationSessionManager
from models.chatbots import Chatbot as ChatbotModel
import helpers.helper_functions as hf
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger




class ChatbotManager:
    """
    Class representing a chatbot manager.

    Attributes:
        db_session: The database session.
        session_manager: The conversation session manager.
        model: The chatbot model.

    Methods:
        get_or_create_chatbot: Retrieves an existing chatbot or creates a new one.
        create_chatbot: Creates a new chatbot.
        get_chatbot: Retrieves a chatbot.
        update_chatbot: Updates a chatbot.
        delete_chatbot: Deletes a chatbot.
        initialize_prompt_template: Initializes the prompt template for the chatbot.
        generate_prompt: Generates a prompt for the chatbot.
        handle_message: Handles an incoming message for the chatbot.
    """
    def __init__(self, db_session):
        self.db_session = db_session
        self.session_manager = ConversationSessionManager(db_session)
        self.model = ChatOpenAI(
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"), model="gpt-4-0125-preview", temperature=0.2
        )

    def get_or_create_chatbot(self, name, description=None, **kwargs):
        """
        Retrieves an existing chatbot with the given name or creates a new one.

        Args:
            name: The name of the chatbot.
            description: The description of the chatbot.
            **kwargs: Additional keyword arguments for creating the chatbot.

        Returns:
            The retrieved or created chatbot.
        """
        chatbot = hf.get_db_object(ChatbotModel, name=name)
        if not chatbot:
            chatbot = self.create_chatbot(name, description, **kwargs)

    def create_chatbot(self, name, description=None, **kwargs):
        """
        Creates a new chatbot with the given name and description.

        Args:
            name: The name of the chatbot.
            description: The description of the chatbot.
            **kwargs: Additional keyword arguments for creating the chatbot.

        Returns:
            The created chatbot.
        """
        try:
            new_chatbot = Chatbot(name=name, description=description, **kwargs)
            hf.add_to_db(new_chatbot)
            return new_chatbot
        except Exception as e:
            logger.error(f"Error creating chatbot: {e}")
            raise

    def get_chatbot(self, **kwargs):
        """
        Retrieves a chatbot based on the given keyword arguments.

        Args:
            **kwargs: Keyword arguments for querying the chatbot.

        Returns:
            The retrieved chatbot.

        Raises:
            ce.ResourceNotFoundError: If the chatbot is not found.
        """
        try:
            chatbot = hf.get_db_object(Chatbot, **kwargs)
            if not chatbot:
                raise ce.ResourceNotFoundError("Chatbot not found")
            return chatbot
        except Exception as e:
            logger.error(f"Error getting chatbot: {e}")
            raise

    def update_chatbot(self, chatbot_id, **kwargs):
        """
        Updates a chatbot with the given chatbot ID and keyword arguments.

        Args:
            chatbot_id: The ID of the chatbot.
            **kwargs: Keyword arguments for updating the chatbot.

        Raises:
            ce.ResourceNotFoundError: If the chatbot is not found.
        """
        try:
            chatbot = self.get_chatbot(chatbot_id)
            if chatbot:
                for key, value in kwargs.items():
                    setattr(chatbot, key, value)
                hf.update_db()
            else:
                raise ce.ResourceNotFoundError("Chatbot not found")
        except Exception as e:
            logger.error(f"Error updating chatbot: {e}")
            raise

    def delete_chatbot(self, chatbot_id):
        """
        Deletes a chatbot with the given chatbot ID.

        Args:
            chatbot_id: The ID of the chatbot.

        Raises:
            ce.ResourceNotFoundError: If the chatbot is not found.
        """
        try:
            chatbot = self.get_chatbot(chatbot_id)
            if chatbot:
                hf.delete_from_db(chatbot)
            else:
                raise ce.ResourceNotFoundError(f"Chatbot not found")
        except Exception as e:
            logger.error(f"Error deleting chatbot: {e}")
            raise

    def initialize_prompt_template(self):
        """
        Initializes the prompt template for the chatbot.

        Returns:
            The initialized prompt template.
        """
        # Define basic PromptTemplate with place holders for messages
        return ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful assistant. You may not need to use tools for every query - the user might just want to chat!"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),

        ])

    def generate_prompt(self, input_message):
        """
        Generates a prompt for the chatbot based on the input message.

        Args:
            input_message: The input message.

        Returns:
            The generated prompt.
        """
        # Use chat history and other context to fill in the template
        chat_history = self.message_history_manager.get_chat_history()
        agent_scratchpad = self.message_history_manager.get_agent_scratchpad()

        # Fill template with context
        prompt = self.prompt_template.fill(
            chat_history=chat_history, input=input_message, agent_scratchpad=agent_scratchpad
        )
        return prompt

    def handle_message(self, input_message):
        """
        Handles an incoming message for the chatbot.

        Args:
            input_message: The incoming message.

        Returns:
            The response from the chatbot.
        """
        # Log incoming message
        logger.debug(f"Handling message for {self.chatbot_model.name}: {input_message}")
        # Generate prompt
        prompt = self.generate_prompt(input_message)
        # Generate response
        response = self.model(prompt)
        # Log response
        logger.debug(f"Response for {self.chatbot_model.name}: {response}")

        # Manage message history
        # Add user message to history
        self.message_history_manager.add_user_message(input_message)
        # Add AI message to history
        self.message_history_manager.add_ai_message(response)
        # Return response
        return response
    
    
