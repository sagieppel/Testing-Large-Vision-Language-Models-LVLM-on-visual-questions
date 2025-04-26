import anthropic
import base64
import os
import time
import API_KEYS
import numpy as np
os.environ['ANTHROPIC_API_KEY'] = API_KEYS.claude_api_key

#---------------
import os
import base64
import cv2
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)  # you can change '.jpg' to '.png' if you want PNG format
    return base64.b64encode(buffer).decode('utf-8')  # Encode the bytes to base64
# API key setup
class claude_bot():
  def __init__(self,model="claude-3-5-sonnet-20241022"):
          self.client = anthropic.Anthropic()
          self.model=model #"claude-3-opus-20240229"

  ###########################Question text image##########################################################################################
  def question_text_image(self,text,image):
          base64_image = encode_image(image)
          for i in range(500):
              try:
                  message = self.client.messages.create(
                        model=self.model,
                        max_tokens=1024,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/jpeg",
                                            "data": base64_image
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": text
                                    }
                                ]
                            }
                        ]
                    )
                  break
              except:
                 print("error failed to contact claude sleeping 4 seconds and retry")
                 time.sleep(4)
                 continue

          return message.content[0].text
###########################Question text##########################################################################################
  def question_text(self,text):
          for i in range(500):
              try:
                  message = self.client.messages.create(
                        model=self.model,
                        max_tokens=1024,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": text
                                    }
                                ]
                            }
                        ]
                    )
                  break
              except:
                 print("error no response from claude  sleeping 4 seconds and retry")
                 time.sleep(4)
                 continue

          return message.content[0].text
###########################Full questions############################################################################################
  def answer_question(self, image, queries=None):
      # -----------------repeat queries until getting correct format of answr (b,c,d)
      for kk in range(6):
          for ii in range(len(queries)):
              all_text = "\n\n query: " + queries[ii] + "\n"  # use to record full interaction
              ky = self.question_text_image(queries[ii], image)
              all_text += str(ii) + ") response:  " + ky +"\n"

              if len(ky) > 1 or ky.lower() not in ['b', 'c', 'd']:
                  ky = self.question_text("Take the following response and reduce it to a single letter:\n" + ky)
                  all_text += str(ii) + ")Take the following response and reduce it to a single letter: response:  " + ky
                  if len(ky) > 1:
                      if (" B" in ky) and (" C" not in ky) and (" D" not in ky): ky = "B"
                      if (" B" not in ky) and (" C" in ky) and (" D" not in ky): ky = "C"
                      if (" B" not in ky) and (" C" not in ky) and (" D" in ky): ky = "D"
                      all_text += str(ii) + ")Extracting answer" + str(ii)

              if len(ky) and (ky.lower() in ['b', 'c', 'd']):
                  return ky, all_text
      return ky, all_text