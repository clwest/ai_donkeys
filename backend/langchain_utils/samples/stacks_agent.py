import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage
from typing import List
from langchain_utils.prompts import prompt_definitions

from factory.token_factory import TokenCounterFactory

# Load environment variables
load_dotenv()
openai_api = os.getenv("OPENAI_API")
token_counter_factory = TokenCounterFactory()


# blockchainAgent class definition
class BlockchainAgent:
    def __init__(self, system_message: SystemMessage, model: ChatOpenAI) -> None:
        self.system_message = system_message
        self.model = model
        self.init_messages()

    def reset(self) -> None:
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        self.stored_messages = self.stored_messages[-10:]
        return self.stored_messages

    def step(self, input_message: HumanMessage) -> AIMessage:
        messages = self.update_messages(input_message)

        # Add custom logic to handle guiding prompt and blockchain/AI prompting
        # ...

        output_message = self.model(messages)
        self.update_messages(output_message)

        return output_message


# Custom function to integrate guiding prompt and other prompts with the agent
def integrate_prompts_with_agent(agent: BlockchainAgent, user_input: str) -> AIMessage:
    # This function needs to integrate the guiding prompt and blockchain/AI prompts
    # with the blockchainAgent to create a conversation flow.
    user_input_lower = user_input.lower()
    selected_prompt = None
    for prompt in blockchain_template + blockchain_and_ai_template:
        if (
            prompt["question"].lower() in user_input_lower
            or prompt["answer"].lower() in user_input_lower
        ):
            selected_prompt
            break

    if selected_prompt:
        custom_prompt = f"{selected_prompt['question']}\n{selected_prompt['answer']}"
    else:
        custom_prompt = f"{starting_template}\nUser Question: {user_input}"

    # Step 3 Customize the Propmt
    # Come back to modify prompts

    # 4: Combine guiding propmt

    # 5: Generate AI Response
    input_message = HumanMessage(content=custom_prompt)
    ai_response = agent.step(input_message)

    return ai_response


# Initialize your agent
system_message = SystemMessage(content=starting_template)
model = ChatOpenAI(
    verbose=True,
    model="gpt-3.5-turbo",
    temperature=0.3,
    openai_api_key=openai_api,
)
agent = BlockchainAgent(system_message, model)
agent.reset()
token_counter = token_counter_factory.create_token_counter(agent)
# Example interaction
user_input = (
    "Is there staking available on the blockchain network?  If now how does it work?"
)
agent_response = integrate_prompts_with_agent(agent, user_input)
print(f"Agent's Response: {agent_response.content}")
