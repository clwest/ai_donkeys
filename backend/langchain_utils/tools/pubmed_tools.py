from langchain.tools import PubmedQueryRun

tool = PubmedQueryRun()
print(tool.run("Stacks Network"))
