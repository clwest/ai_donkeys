from tkinter import *
import openai
import customtkinter as ctk
import os
from dotenv import load_dotenv
import pickle

from dotenv import load_dotenv
load_dotenv()

from textwrap import dedent
from crewai import Agent, Crew

from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents


class ImageCrewFrame(ctk.CTkFrame):
  def __init__(self, master, **kwrags):
    super().__init__(master, **kwrags)

    self.label = ctk.CTkLabel(self, text="Generate Images for ads.")
    self.label.grid(row=0, column=0, padx=20)

class App(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("Marketing Crew AI")
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)


    self.image_frame = ImageCrewFrame(master=self)
    self.image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="news")

    # Initialize the tasks and agents
    self.tasks = MarketingAnalysisTasks()
    self.agents = MarketingAnalysisAgents()

    # Create Input fields
    ctk.CTkLabel(self, text="What is the product website you want a marketing strategy for?", padx=20, pady=20).pack()
    self.product_website_entry = ctk.CTkEntry(self, corner_radius=10, text_color="cyan", placeholder_text="www.example.com")
    self.product_website_entry.pack()


    ctk.CTkLabel(self, text="Any extra details about the product and or the instagram post you want?", padx=20, pady=10).pack()
    self.product_details_entry = ctk.CTkEntry(self, corner_radius=10, text_color="cyan", placeholder_text="Short discription")
    self.product_details_entry.pack()

    # Button
    ctk.CTkButton(self, text="Generate Marketing Strategy", command=self.generate_strategy, fg_color="black", anchor="ew").pack()




  def generate_strategy(self):
    product_website = self.product_website_entry.get()
    product_details = self.product_details_entry.get()

    # CrewAI Logic
    product_competitor_agent = self.agents.product_competitor_agent()
    strategy_planner_agent = self.agents.strategy_planner_agent()
    creative_agent = self.agents.creative_content_creator_agent()

    website_analysis = self.tasks.product_analysis(product_competitor_agent, product_website, product_details)
    market_analysis = self.tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
    campaign_development = self.tasks.campaign_development(strategy_planner_agent, product_website, product_details)
    write_copy = self.tasks.instagram_ad_copy(creative_agent)

    # Setup crew
    copy_crew = Crew(
      agents=[product_competitor_agent, strategy_planner_agent, creative_agent],
      tasks=[website_analysis, market_analysis, campaign_development, write_copy],
      verbose=True,
    )
    ad_copy = copy_crew.kickoff()

    # Display Results
    self.result_text.delete('1.0', END)
    self.result_text.insert(END, "Your post copy:\n" + ad_copy + "\n\n")






app = App()
app.configure(fg_color=("CadetBlue3", "CadetBlue4"))
app.geometry("650x650")
app.mainloop()