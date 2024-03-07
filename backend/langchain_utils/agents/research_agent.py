import os
from pprint import pprint
from flask import jsonify, request
from langchain.tools import DuckDuckGoSearchRun, ArxivQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_experimental.autonomous_agents import AutoGPT
import pinecone
from factory.pinecone_factory import init_pinecone
from factory.token_factory import TokenCounterFactory
from models.blogs import Post
from factory import db


class ResearchAgent:
    def __init__(self):
        self.initialize_tools()
        self.initialize_agent()

    def initialize_tools(self):
        self.search_tool = DuckDuckGoSearchRun()
        self.wikipedia_tool = WikipediaAPIWrapper()
        self.arvix_tool = ArxivQueryRun()
        self.tools = [
            Tool(
                name="search",
                func=self.search_tool.run,
                description="Search tool for current events.",
            ),
            Tool(
                name="Wikipedia",
                func=self.wikipedia_tool.run,
                description="Wikipedia search tool.",
            ),
            Tool(
                name="Arvix",
                func=self.arvix_tool.run,
                description="Useful for searching research papers on Arvix.",
            ),
        ]

    def initialize_agent(self):
        init_pinecone()
        openai_api = os.getenv("OPENAI_API")
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-ada-002", openai_api_key=openai_api
        )
        index_name = os.getenv("PINECONE_INDEX")
        pinecone_client = pinecone.Index(index_name)
        vectorstore = Pinecone(pinecone_client, embeddings_model, "text")
        self.agent = AutoGPT.from_llm_and_tools(
            ai_name="AutoResearch",
            ai_role="Assistant",
            tools=self.tools,
            llm=ChatOpenAI(temperature=0, openai_api_key=openai_api),
            memory=vectorstore.as_retriever(),
        )

    def do_research(self, keyword):
        result = self.agent.run(
            [
                f"write a witty, humorous but concise report about {keyword}",
                f"save the report in the `report` directory",
            ],
            # limit=4,
        )
        # Save the report in the SQL database
        new_post = Post(
            title=f"Report on {keyword}", content=str(result), is_draft=False
        )
        db.session.add(new_post)
        db.session.commit()
        return result

    def list_reports(self):
        posts = Post.query.all()
        return [post.serialize() for post in posts]

    def read_report(self, report_id):
        post = Post.query.get(report_id)
        if post:
            return post.content
        else:
            return "Report not found", 404


# Example usage
agent = ResearchAgent()
keyword = "Blockchain"
result = agent.do_research(keyword)
pprint(result)
