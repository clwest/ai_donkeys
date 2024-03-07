from langchain.tools import YouTubeSearchTool

youtube_search = YouTubeSearchTool()

print(youtube_search.run("Learn to write smart contracts with Solidity"))
