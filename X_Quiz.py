import cv2
import os
import random
import numpy as np
import X_api_class
import QuizMakingClass
import queries
# "chatgpt-4o-latest"
#"grok-2-vision-latest"
AI_bot = X_api_class.openai_bot(model="grok-2-vision-latest",details="high")


input_dir= r"/media/deadcrow/SSD_480GB/segment_anything/2D_Shape_Matching_Tests/Rotation_Textured_shape_Textured_Background"
error_dir = r"/media/deadcrow/6TB/Data_zoo/x_quize/"
save_error=True
save_all=True
if __name__ == '__main__':
    quiz_maker=QuizMakingClass.make_quize(main_dir = input_dir, max_img_per_mat=1)
    quiz_maker.run_test(AI_bot,ouput_dir=error_dir,save_error=save_error,save_all=save_all,queries=queries.Shapes2D)