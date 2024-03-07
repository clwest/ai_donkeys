from tkinter import *
import os
import openai
from dotenv import load_dotenv
from PIL import ImageTk, Image
import requests, io
import threading
from threading import Lock
import traceback
import time


load_dotenv()
huggingface_api = os.getenv("HUGGINGFACE_API")



# Globals
images = []
current_image_index = 0
original_images = []  # To store the original PIL Image objects

progress_count = 0 # shared variable for progress tracking
progress_count_lock = Lock()


def update_canvas(photo_image):
    canvas.image = photo_image # Keep reference to avoid garbage collection
    canvas.create_image(0, 0, anchor="nw", image=photo_image)

def update_canvas_with_index(index):
   global current_image_index
   if 0 <= index < len(images):
      current_image_index = index
      canvas.image = images[index]
      canvas.create_image(0, 0, anchor="nw", image=images[index])

def next_image():
   update_canvas_with_index(current_image_index + 1)

def previous_image():
   update_canvas_with_index(current_image_index - 1)

def save_image():
    if original_images:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            original_images[current_image_index].save(file_path)  # Save the original image

def update_timer(index, elapsed_time):
    timer_label.configure(text=f"Image {index + 1} generated in {elapsed_time:.2f} seconds")


def generate_image(user_prompt, progress_increment, index, total_images):
    global progress_count
    print(f"Index: {index}, Total Images: {total_images}")  # Debugging statement
    retries = 3
    retry_delay = 15 # seconds
    last_response = None

    for attempt in range(retries):
      try:
        start_time = time.time()
        update_progress_bar(0)
        print(f"Generating image {index+1}...")
        model_endpoint = "stabilityai/stable-diffusion-2-1"
        test_prompt = "dataautogpt3/OpenDalleV1.1"
        headers = {
            "Authorization": f"Bearer {huggingface_api}"
        }
        data = {
            "inputs": user_prompt,
            # Add other parameters as needed, for example:
            "parameters": {
                "height": 512,
                "width": 512,
                "num_inference_steps": 70,
                "guidance_scale": 7.5
            }
        }
        response = requests.post(f"https://api-inference.huggingface.co/models/{model_endpoint}", headers=headers, json=data)
        last_response = response
        
        if response.status_code == 200:
            end_time = time.time()
            # update_progress_bar(progress_increment * (index + 1)) # Incremantal update
            elapsed_time = end_time - start_time
            
            image = Image.open(io.BytesIO(response.content))
            original_images.append(image) # Store the original image
            photo_image = ImageTk.PhotoImage(image)
            images.append(photo_image) # Append to global list
            root.after(0, lambda: update_canvas(photo_image))
            root.after(0, lambda: update_timer(index, elapsed_time))

            # progress bar update
            with progress_count_lock:
               progress_count += 1
               
               # Set signel image to 100%
               if total_images ==1:
                  root.after(0, lambda: update_progress_bar(100))
               else:
                  progress_percentage = (progress_count / total_images) * 100
                  print(f"Updating progress bar: {progress_percentage}%")  # Debugging statement
                  root.after(0, lambda: update_progress_bar(progress_percentage))
            break

        elif response.status_code == 503 and attempt < retries -1:
           print(f"Model loading, retrying in {retry_delay} seconds...")
           time.sleep(retry_delay)
        else:
           print(f"Error in image generation (Image {index + 1}):", response.status_code, response.text)
           break
        
        last_response = response

      except Exception as e:
          print(f"Exception in generating image {index+1}:", str(e))
          traceback.print_exc()
          break # Exit retry loop on exception
      
    if last_response and last_response.status_code != 200:
       print(f"Failed to generate image {index + 1} after {retries} attempts. ")

def get_prompt_text():
   return prompt_text.get("1.0", tk.END).strip()

def get_number_of_images():
   return int(number_slider.get())

def generate():
  global progress_count
  progress_count = 0
  user_prompt = get_prompt_text()
  number_of_images = get_number_of_images()

  print(f"Number of images to generate: {number_of_images}")

  if number_of_images <= 0:
     print(f"Number of images must be greater than zero")
     return
  
  # Calculate the progress increment for each image
  progress_increment = 100 / number_of_images

  for i in range(number_of_images):
      print(f"Starting generation of image { i + 1}")
      thread = threading.Thread(target=generate_image, args=(user_prompt, progress_increment, i, number_of_images))
      thread.start()

def update_progress_bar(value):
   progress_bar['value'] = value
   root.update_idletasks() # Update the GUI


def update_slider_label(value):
   int_value = int(float(value))
   slider_value_label.configure(text=str(int_value))

