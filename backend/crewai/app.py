from tkinter import *
import openai
import customtkinter as ctk
import os
from dotenv import load_dotenv
import pickle


class App(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("Crew AI")
    # self.geometry("650x650")
    self.geometry("650x650+300+120")




app = App()
app.configure(fg_color=("CadetBlue3", "CadetBlue4"))
app.mainloop()