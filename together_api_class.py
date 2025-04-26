 # pip install together
 # https://docs.together.ai/docs/vision-overview
 # billing and API KEY
 # https://api.together.xyz/settings/billing
 # https://api.together.xyz/settings/api-keys
import API_KEYS
from together import Together
import base64


import os
import time

import numpy as np

import API_KEYS
import base64
from openai import OpenAI
import cv2
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)  # you can change '.jpg' to '.png' if you want PNG format
    return base64.b64encode(buffer).decode('utf-8')  # Encode the bytes to base64

# API key setup
api_key =  API_KEYS.open_AI_api_key
############################################################################################################################
class openai_bot():
  def __init__(self,model,details="high"):
          self.client = Together(api_key=API_KEYS.together_api_key)

          self.model =  model
          self.details = details
         # "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
         # "Qwen/Qwen2-VL-72B-Instruct",
         # #"Qwen/Qwen2.5-VL-72B-Instruct", # #Expensive #
         # "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
         # #"meta-llama/Llama-4-Scout-17B-16E-Instruct",

##########################################Question using text and image#################################################################################
  def question_text_image(self,text,image):

      base64_image = encode_image(image)
      for i in range(500):
          try:
              print(i, "image query: ",text)
              stream = self.client.chat.completions.create(
                  model = self.model,
                  messages=[
                      {
                          "role": "user",
                          "content": [
                              {"type": "text", "text": text},
                              {
                                  "type": "image_url",
                                  "image_url": {
                                      "url": f"data:image/jpeg;base64,{base64_image}",
                                  },
                              },
                          ],
                      }
                  ],
                  stream=True,
              )

          except:
                      print(i,"error no response from ",self.model,"  sleeping 4 seconds and retry")
                      time.sleep(4)
                      continue

          txt = ""
          for chunk in stream:
              if chunk.choices:
                  txt += chunk.choices[0].delta.content  # or ""  else "", end="", flush=True)


          return (txt)
###########################Question text ##########################################################################################
  def question_text(self,text):

      for i in range(500):
          try:
              print(i, "image query: ", text)
              stream = self.client.chat.completions.create(
                  model=self.model,
                  # "Qwen/Qwen2-VL-72B-Instruct",#"Qwen/Qwen2.5-VL-72B-Instruct",#Expensive #"meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",#"meta-llama/Llama-4-Scout-17B-16E-Instruct",#"meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                  messages=[
                      {
                          "role": "user",
                          "content": [
                              {"type": "text", "text": text},

                          ],
                      }
                  ],
                  stream=True,
              )

          except:
              print(i, "error no response from ", self.model, "  sleeping 4 seconds and retry")
              time.sleep(4)
              continue

          txt = ""
          for chunk in stream:
              if chunk.choices:
                  txt += chunk.choices[0].delta.content  # or ""  else "", end="", flush=True)

          return (txt)
###########################Full questions############################################################################################
  def answer_question(self, image, queries):  # Answer question in queries regarding image
      print("Answer question", queries)
      # -----------------repeat queries until getting correct format of answer (b,c,d)
      for ii in range(len(queries)):
          all_text = "\n\n query: " + queries[ii] + "\n"  # use to record full interaction
          ky = self.question_text_image(queries[ii], image)  # Get answer query+image
          all_text += str(ii) + ") response:  " + ky + "\n"
          # ---------------Reduce answer to single letter--------------------------------------------------------
          if len(ky) > 1 or ky.lower() not in ['b', 'c', 'd']:
              ky = self.question_text(
                  "Take the following response and reduce it to a single letter which the selected panel letter B,C,D. If no correct panel is mention in the answer write N. Note response of more than single character is an error. \nHere is the text:\n" + ky)
              all_text += str(
                  ii) + ") Take the following response and reduce it to a single letter which the selected panel letter B,C,D. If no correct panel is mention in the answer write N. Note response of more than single character is an error. \nHere is the text:\n" + ky
              if len(ky) > 1:
                  if (" B" in ky) and (" C" not in ky) and (" D" not in ky): ky = "B"
                  if (" B" not in ky) and (" C" in ky) and (" D" not in ky): ky = "C"
                  if (" B" not in ky) and (" C" not in ky) and (" D" in ky): ky = "D"
                  all_text += "\n Automatic Extracting answer: " + str(ky)

          if len(ky) and (ky.lower() in ['b', 'c', 'd']):
              return ky, all_text
          print(ii, all_text, "\n\nFailed to get real answer switching to next query if exist", )
      return ky, all_text

#################################################################################################################################################

  def answer_question_image_to_text_description(self,image,queries_image,queries_text):
      '''Answer question by first asking for text description of each panel and then asking second model that only use the text description to answer the question'''
      print("Answer question", queries_image)
      #-----------------repeat queries until getting correct format of answr (b,c,d)
      for ii in range(len(queries_image)):
          all_text = "\n\n query: " + queries_image[ii]+"\n"  # use to record full interaction
          ky = self.question_text_image(queries_image[ii], image)
          all_text += str(ii) + ") response:  " + ky + "\n"
          if len(ky) != 1 or (ky.lower() not in ['b', 'c', 'd']):
              print(queries_text[ii] + ky)
              all_text+="\n\n"+queries_text[ii] + ky
              ky=self.question_text(queries_text[ii]+ky)
              all_text+="Response:"+queries_text[ii]+"  "+ky
              print("Response:",queries_text[ii],"   ",ky)

              all_text += "Take the following response and reduce it to a single letter (B,C,D), if none of the above leave empty:" +ky
              for i in range(5):
                  all_text+="\nTRY: "+str(i)
                  ky=self.question_text("Take the following response and reduce it to a single letter (B,C,D), if none of the above leave empty:" +ky)
                  all_text+="\n Response: "+ky
                  if len(ky)<=1: break

          if len(ky) and (ky.lower() in ['b', 'c', 'd']):
               return ky, all_text
          print(ii,all_text,"\n\nFailed to get real answer switching to next query if exist",)
      return ky, all_text


