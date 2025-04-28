# Test multiple models on multiple tests
import cv2
import os
import random
import numpy as np
import together_api_class
import openai_api_class
import QuizMakingClass#_TEXT2TEXT as QuizMakingClass
import queries
import gemini_api_class
# "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
# "Qwen/Qwen2-VL-72B-Instruct",
# #"Qwen/Qwen2.5-VL-72B-Instruct", # #Expensive #
# "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
# #"meta-llama/Llama-4-Scout-17B-16E-Instruct",
main_out_dir=r"/media/deadcrow/SSD_480GB/results_vlm/"
if not os.path.exists(main_out_dir): os.mkdir(main_out_dir)

inputs_dirs={"2d_textures":{"query":queries.Textures2D,"path":r"/media/deadcrow/SSD_480GB/segment_anything/2D_textures_matchig_test"},
             "2d_shapes":{"query":queries.Shapes2D,"path":r"/media/deadcrow/SSD_480GB/segment_anything/2D_Shape_Matching_Tests/"},
             "3d_materials":{"query":queries.PbrMaterials2D,"path":r"/media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/All_Test"},
             "3d_objects":{"query":queries.Objects3D,"path":r"/media/deadcrow/6TB/python_project/Can_LVM_See3D/All_Tests"}
    }

models_dic={
     "Qwen2_VL_72BInstruct":together_api_class.openai_bot(model="Qwen/Qwen2-VL-72B-Instruct",details="high"),
    "Llama_32_90B":together_api_class.openai_bot(model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",details="high"),
    "Llama4Scout17B_16E_Instruct": together_api_class.openai_bot(model="meta-llama/Llama-4-Scout-17B-16E-Instruct",details="high"),
    "o4mini":openai_api_class.openai_bot(model="o4-mini", details="high"),
    "gemini_2_5_flash_preview": gemini_api_class.gemini_bot(model="gemini-2.5-flash-preview-04-17"),
    "gemini_2_0_flash_thinking_exp": gemini_api_class.gemini_bot(model="gemini-2.0-flash-thinking-exp")
}

save_error=True
save_all=True
skip_exists=True

for model_name in models_dic: # go ove ALL modelw
     model=models_dic[model_name]
     for test_type in inputs_dirs: # go over all main dirs
         main_in_dir=inputs_dirs[test_type]["path"]
         queries=inputs_dirs[test_type]["query"]
         print("Testing model:",model_name," on ",test_type)
         out_dir = main_out_dir+ "/MODEL_"+model_name+"_TEST_"+test_type
         if not os.path.exists(out_dir): os.mkdir(out_dir)

         for sdir in os.listdir(main_in_dir):
             input_dir = main_in_dir + "//" + sdir + "//"
             print(input_dir)
             if not os.path.isdir(input_dir): continue
             error_dir = out_dir + "//" + sdir + "//"
             if os.path.exists(error_dir + "/finish.txt") and skip_exists: continue
             quiz_maker = QuizMakingClass.make_quize(main_dir=input_dir, max_img_per_instance=1,max_img_total=200, max_instance_per_class=1)
             quiz_maker.run_test(model, ouput_dir=error_dir, save_error=save_error, save_all=save_all,queries=queries)
             fl=open(error_dir + "/finish.txt","w")
             fl.close()



