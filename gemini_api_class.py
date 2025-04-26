#https://ai.google.dev/gemini-api/docs/quickstart?lang=python
#https://ai.google.dev/gemini-api/docs/billing
#https://ai.google.dev/gemini-api/docs/models/gemini
#https://aistudio.google.com/plan_information
import os
import base64
import google.generativeai as genai
import API_KEYS

from PIL import Image
import cv2
import numpy as np
# Set your API key
genai.configure(api_key=API_KEYS.gemini_api_key)
sleep_time=4

import PIL.Image

class gemini_bot():
  def __init__(self,model):
          self.model = genai.GenerativeModel(model_name=model)

  ###########################Question text image##########################################################################################
  def question_text_image(self,text,image):
          img = Image.fromarray(image[:, :, ::-1])
          # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          #
          # # Create PIL Image
          # pil_image = Image.fromarray(i_rgb)
          # image_path="temp_im.jpg"
          # cv2.imwrite(image_path,image)
          # img = PIL.Image.open(image_path)
          for i in range(800):
              print("attemept",i,"image question:", text)
              try:
                  response = self.model.generate_content([img, text])
                  return response.text
              except:
                  import time
                  print("attemept",i,"Fail contact gemini sleeping ",sleep_time," seconds and retry")
                  time.sleep(sleep_time)

###########################Question text##########################################################################################
  def question_text(self, text):
      for i in range(600):
          try:
              print("\nattemept",i,"text question:",text)
              response = self.model.generate_content([text])
              return response.text
          except:
              import time
              print("attemept",i,"Fail contact gemini sleeping ",sleep_time," seconds and retry")
              time.sleep(sleep_time)

###########################Full questions############################################################################################
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

  def answer_question_image_to_text_description(self, image, queries_image, queries_text):
      '''Answer question by first asking for text description of each panel and then asking second model that only use the text description to answer the question'''
      print("Answer question", queries_image)
      # -----------------repeat queries until getting correct format of answr (b,c,d)
      for ii in range(len(queries_image)):
          all_text = "\n\n query: " + queries_image[ii] + "\n"  # use to record full interaction
          ky = self.question_text_image(queries_image[ii], image)
          all_text += str(ii) + ") response:  " + ky + "\n"
          if len(ky) != 1 or (ky.lower() not in ['b', 'c', 'd']):
              print(queries_text[ii] + ky)
              all_text += "\n\n" + queries_text[ii] + ky
              ky = self.question_text(queries_text[ii] + ky)
              all_text += "Response:" + queries_text[ii] + "  " + ky
              print("Response:", queries_text[ii], "   ", ky)

              all_text += "Take the following response and reduce it to a single letter (B,C,D), if none of the above leave empty:" + ky
              for i in range(5):
                  all_text += "\nTRY: " + str(i)
                  ky = self.question_text(
                      "Take the following response and reduce it to a single letter (B,C,D), if none of the above leave empty:" + ky)
                  all_text += "\n Response: " + ky
                  if len(ky) <= 1: break

          if len(ky) and (ky.lower() in ['b', 'c', 'd']):
              return ky, all_text
          print(ii, all_text, "\n\nFailed to get real answer switching to next query if exist", )
      return ky, all_text



