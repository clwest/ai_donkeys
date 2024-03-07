from langchain.agents import load_tools
from pprint import pprint

requests_tools = load_tools(["requests_all"])

pprint(requests_tools)
