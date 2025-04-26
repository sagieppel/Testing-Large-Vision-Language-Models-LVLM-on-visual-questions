# Ask the model to explain their response
import X_api_class
import cv2
import os
import random
import numpy as np
import claude_api_class
import QuizMakingClass
import gemini_api_class
import llama_api_class
import gemini_api_class
import openai_api_class
#AI_bot = claude_api_class.claude_bot(model="claude-3-5-sonnet-20241022")
#AI_bot = llama_api_class.openai_bot(model="llama3.2-90b-vision",details="high")
AI_bot = gemini_api_class.gemini_bot(model="gemini-1.5-pro")#gemini-2.0-flash-exp")
#AI_bot = X_api_class.openai_bot(model="grok-2-vision-latest",details="high")
#AI_bot = openai_api_class.openai_bot(model="gpt-4o",details="high")

in_dir =  "//media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/Test_materials_Results_gemini-1.5-pro/Change_Random_object_and_background_3x_size_object_mapping_mode_no_displacement/errors/"
out_dir = "//media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/Test_materials_Results_gemini-1.5-pro/Change_Random_object_and_background_3x_size_object_mapping_mode_no_displacement_errors_Explained_XXXXX2uyuuuu2X/"
if not os.path.exists(out_dir): os.mkdir(out_dir)
for xx,fl in enumerate(os.listdir(in_dir)):


        if ".jpg" in fl:
            im=cv2.imread(in_dir+"/"+fl)
            txt="Which of the panels contain an object with identical  material/texture to the material of the object   in panels A?\n Note that the shape of the object and the setting in which the material appear is different. The texture might also be rotated. \n Explain your answer in detail, including how you got to it and what distinguishing features you used.\n"
            txt+=AI_bot.question_text_image(txt,im)
            cv2.imwrite(out_dir+"/"+fl,im)
            txtfl = open(out_dir+"/"+fl[:-4]+".txt","w")
            txtfl.write(txt)
            txtfl.close()
            print(out_dir+"/"+fl[:-4]+".txt")
            print(txt)

