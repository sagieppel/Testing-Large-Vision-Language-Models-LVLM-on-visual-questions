#https://console.x.ai/team/f1bf66fa-edbd-4e07-a691-1391cf5436a6/billing/credits
#-----------------------------------------------------------------------------
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
api_key =  API_KEYS.grok_api_key
class openai_bot():
  def __init__(self,model,details="high"):
          self.client = OpenAI(
               api_key="xai-Zg1IgUOqfpZ7ej8HEH4WwNbOmvQ3fWXc9EVM6C5L14pTB7JL9rUBEdDsxSmfnRHjq5FudNzpAE6l84Ug", #XAI_API_KEY,
               base_url="https://api.x.ai/v1",)


          self.model =  model# "gpt-4o-mini",#"gpt-4o",#,"gpt-4o-mini""gpt-4-turbo"#
          self.details = details
##########################################Question using text and image#################################################################################
  def question_text_image(self,text,image):
      base64_image = encode_image(image)
      for i in range(500):
          try:
              print(i, "image query: ",text)
              response = self.client.chat.completions.create(
                                  model= self.model,
                                  messages=[
                                    {
                                      "role": "user",
                                      "content": [
                                        {
                                          "type": "text",
                                          "text": text,
                                        },
                                        {
                                          "type": "image_url",
                                          "image_url": {
                                            "url":  f"data:image/jpeg;base64,{base64_image}",
                                           "detail":  self.details#"high"# "low", "auto"
                                          },
                                        },
                                      ],
                                    }
                                  ]#temp=0 # give bad results
                      )

              return (response.choices[0].message.content)
          except:
                      print(i,"error no response from gpt  sleeping 4 seconds and retry")
                      time.sleep(4)


#####################################################################################################################
  def question_text(self,text):
      for ii in range(500):

         try:
              response = self.client.chat.completions.create(
                          model= self.model,#"gpt-4o",#,"gpt-4o-mini"
                          messages=[
                            {
                              "role": "user",
                              "content": [
                                {
                                  "type": "text",
                                  "text": text,
                                },
                              ],
                            }
                          ]#,temperature=0bad
              )
              return (response.choices[0].message.content)
         except:
             print(ii,"error no response from gpt on pure text query  sleeping 4 seconds and retry")
             time.sleep(4)



###########################Full questions############################################################################################
  def answer_question(self,image,queries): # Answer question in query queries regarding image
      print("Answer question", queries)
      #-----------------repeat queries until getting correct format of answer (b,c,d)
      for ii in range(len(queries)):
          all_text = "\n\n query: " + queries[ii]+"\n"  # use to record full interaction
          ky = self.question_text_image(queries[ii], image) # Get answer query+image
          all_text += str(ii) + ") response:  " + ky + "\n"
          #---------------Reduce answer to single letter--------------------------------------------------------
          if len(ky) > 1 or ky.lower() not in ['b', 'c', 'd']:
              ky=self.question_text("Take the following response and reduce it to a single letter which the selected panel letter B,C,D. If no correct panel is mention in the answer write N. Note response of more than single character is an error. \nHere is the text:\n"+ky)
              all_text += str(ii) +") Take the following response and reduce it to a single letter which the selected panel letter B,C,D. If no correct panel is mention in the answer write N. Note response of more than single character is an error. \nHere is the text:\n" + ky
              if len(ky)>1:
                  if (" B" in ky) and (" C" not in ky) and (" D" not in ky): ky = "B"
                  if (" B" not in ky) and (" C" in ky) and (" D" not in ky): ky = "C"
                  if (" B" not in ky) and (" C" not in ky) and (" D" in ky): ky = "D"
                  all_text +="\n Automatic Extracting answer: "+str(ky)

          if len(ky) and (ky.lower() in ['b', 'c', 'd']):
               return ky, all_text
          print(ii,all_text,"\n\nFailed to get real answer switching to next query if exist",)
      return ky, all_text


