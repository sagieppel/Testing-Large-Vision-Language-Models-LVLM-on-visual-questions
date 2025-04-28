import cv2
import os
import random
import numpy as np
import claude_api_class
import QuizMakingClass
import queries

AI_bot = claude_api_class.claude_bot(model="claude-3-5-sonnet-20241022")

input_dir= r"test_images/"
error_dir = r"test_results/"
save_error=True
save_all=True
if __name__ == '__main__':
    quiz_maker=QuizMakingClass.make_quize(main_dir = input_dir, max_img_per_instance=1,max_instance_per_class=2)
    quiz_maker.run_test(AI_bot,ouput_dir=error_dir,save_error=save_error,save_all=save_all,queries=queries.Objects3D)