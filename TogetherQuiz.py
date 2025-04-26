import cv2
import os
import random
import numpy as np
import together_api_class
import QuizMakingClass#_TEXT2TEXT as QuizMakingClass
import queries

# "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
# "Qwen/Qwen2-VL-72B-Instruct",
# #"Qwen/Qwen2.5-VL-72B-Instruct", # #Expensive #
# "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
# #"meta-llama/Llama-4-Scout-17B-16E-Instruct",


AI_bot = together_api_class.openai_bot(model="Qwen/Qwen2-VL-72B-Instruct",details="high")

input_dir= r"test_images/"
error_dir = r"test_results/"
save_error=True
save_all=True
if __name__ == '__main__':
    quiz_maker=QuizMakingClass.make_quize(main_dir = input_dir, max_img_per_mat=1)
    quiz_maker.run_test(AI_bot,ouput_dir=error_dir,save_error=save_error,save_all=save_all,queries=queries.Objects3D)