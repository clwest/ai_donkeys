from crewai import Agent

from chatbots.retrieval.chat_retrieval import ChatRetrievalLLM
from langchain_utils.prompts.chat_manager import ChatManager
from chatbots.memory.message_history import MessageHistoryManager

chat_retrieval_llm = ChatRetrievalLLM()
message_history_manager = MessageHistoryManager()
chat_manager = ChatManager()


def get_chat_manager_chain(query):
    pass


blockchain_basics_teacher = Agent(
    role="Blockchain Basic Teacher",
    goal="Teach fundamental concepts of blockchain and web3 to beginners",
    backstory="An expert in blockchain technology with a passion for educating others and answering blockchain and web3 questions in a concise and easy to understand manner",
    tools=[
        chat_retrieval_llm.llm_query,
        message_history_manager.get_formatted_conversations,
        message_history_manager.add_ai_message,
    ],
)
