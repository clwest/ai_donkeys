import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from factory.token_factory import TokenCounterFactory
from pprint import pprint


class ChatManager:
    """
    Manages the chat functionality by setting up the destination chains, router chain, and main chain.
    """

    def __init__(self):
        # Load environment variables
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        self.llm = ChatOpenAI(
            temperature=0.4, model="gpt-4-1106-preview"
        )

        self.prompt_info = prompt_info
        self.destination_chains = self.setup_destination_chains()
        self.router_chain = self.setup_router_chain()
        self.chain = self.setup_main_chain()

    def setup_destination_chains(self):
        """
        Sets up the destination chains based on the prompt info.
        Returns a dictionary of destination chains.
        """
        destination_chains = {}
        for p_info in prompt_info:
            name = p_info["name"]
            prompt_template = p_info["template"]
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            output_parser = CommaSeparatedListOutputParser()
            chain = LLMChain(llm=self.llm, prompt=prompt, output_parser=output_parser)
            destination_chains[name] = chain

        return destination_chains

    def setup_router_chain(self):
        """
        Sets up the router chain based on the prompt info.
        Returns the router chain.
        """
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_info]
        destinations_str = "\n".join(destinations)
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )

        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )

        return LLMRouterChain.from_llm(self.llm, router_prompt)

    def setup_main_chain(self):
        """
        Sets up the main chain with the router chain, destination chains, and default chain.
        Returns the main chain.
        """
        init_prompt = ChatPromptTemplate.from_template("{input}")
        output_parser = CommaSeparatedListOutputParser()
        init_chain = LLMChain(
            llm=self.llm, prompt=init_prompt, output_parser=output_parser
        )

        return MultiPromptChain(
            router_chain=self.router_chain,
            destination_chains=self.destination_chains,
            default_chain=init_chain,
            verbose=True,
        )

    def run_query(self, query):
        """
        Runs the query through the main chain and returns the response.
        """
        return self.chain.run(query)
