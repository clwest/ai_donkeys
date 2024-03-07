from tkinter import *
import tkinter as tk
import customtkinter as ctk
import ttkbootstrap as tb
import os
from tkinter import filedialog
import openai
from dotenv import load_dotenv
from PIL import ImageTk, Image
import requests, io
import threading
import traceback
import time
from crewai import Agent, Task, Crew, Process
from langchain.chat_models import ChatOpenAI

load_dotenv()
huggingface_api = os.getenv("HUGGINGFACE_API")


openai_api = os.getenv("OPENAI_API")

model = ChatOpenAI(
    verbose=True,
    model="gpt-4-1106-preview",
    temperature=0.3,
    openai_api_key=openai_api,
)

user_input_text = ""


# Define Crew Agents
query_understanding_agent = Agent(
    role="Query Understanding Agent",
    goal="Interpret user queries",
    backstory="""
              A seasoned linguistic analyst with a rich background in computational linguistics and natural language processing. 
              Having worked in diverse fields, from customer service automation to AI-driven research, this agent possesses an uncanny ability to decipher complex queries. 
              Trained in multiple languages and versed in various dialects, it excels at extracting meaning, intent, and nuance from user inputs. Its expertise lies in identifying the underlying questions or needs, even in the most ambiguously phrased queries, ensuring that the core of every conversation is understood accurately.
              """,
    llm=model,
    verbose=True,
)

response_generation_agent = Agent(
    role="Response Generation Agent",
    goal="Generate responses to user queries",
    backstory="""
              A creative and articulate AI, crafted by a team of writers and conversational designers, with a deep understanding of human communication and storytelling. 
              This agent's journey began in the realm of interactive fiction and evolved through years of experience in customer engagement and public relations. 
              It specializes in generating responses that are not only contextually relevant but also engaging and empathetic. Known for its versatility, the agent can adapt its tone and style to suit various scenarios, from formal business interactions to casual conversations, always aiming to provide responses that resonate with the audience.
              """,
    llm=model,
    verbose=True,
)

# Define Crew Tasks
query_task = Task(
    description=f"Analyze the user query: {user_input_text} and extract key information",
    agent=query_understanding_agent,
)

response_task = Task(
    description=f"Generate a response based on the analyzed query: {user_input_text}",
    agent=response_generation_agent,
)

# Instantiate the Crew
chatbot_crew = Crew(
    agents=[query_understanding_agent, response_generation_agent],
    tasks=[query_task, response_task],
    process=Process.sequential,
    verbose=True,
)


# Function to update tasks with the latest user input
def update_tasks_with_input():
    query_task.description = (
        f"Analyze the user query: {user_input_text} and extract key information"
    )
    response_task.description = (
        f"Generate a response based on the analyzed query: {user_input_text}"
    )


def process_input():
    global user_input_text
    user_input_text = user_input_entry.get()

    # Update tasks with the new user input
    update_tasks_with_input()
    # Process the input using CrewAI (adapt this part to integrate with CrewAI's actual operation)
    response = chatbot_crew.kickoff()
    # Display the response in the UI
    response_label.configure(text=response)


root = ctk.CTk()
root.title("CrewAI Chatbot")
root.geometry("650x650")

user_input_entry = Entry(root, width=50)
user_input_entry.pack()

# Button to send input
send_button = ctk.CTkButton(root, text="Send", command=process_input)
send_button.pack()

# Label to display the response
response_label = ctk.CTkTextbox(root)
response_label.pack()

root.mainloop()
