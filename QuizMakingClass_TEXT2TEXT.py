# Create 4 panel quiz in which the goal is to find which panel B,C,D  is identical to the object in panel a in term of some property
# Assume the images already given and arrange according to class/object_instatnce/image.jpg

import cv2
import os
import random
import numpy as np
#------------------------------------------------------------------------------------------------------------
def add_text(image,text):

    font = cv2.FONT_HERSHEY_PLAIN #cv2.FONT_HERSHEY_SIMPLEX
    #cv2.FONT_HERSHEY_PLAIN
    font_scale = 8  # Adjust size as needed
    font_thickness = 4
    color = (255, 255, 255)  # Black color for text

    # Position the text in the top-left corner
    x, y = 10, 83  # Offset for placement; adjust y based on font size

    # Add the text to the image
    cv2.putText(image, text, (x, y), font, font_scale, color, font_thickness)
    return image


#-------------------------------------------------------------------------------------
class make_quize():
    def __init__(self,main_dir = r"",max_img_per_mat=10,max_img_total=10000):
        self.max_img_per_mat=max_img_per_mat
        self.max_img2test=max_img_total
        self.main_dir=main_dir # main folder with image divided into main_dir/class_dir/object_dir/instance_image.png
              #=========================Create dictionary of all images===============================
        self.dic_imgs={} # structure that will contain all images arrange by material and index
        self.list_indx = []  # list of all images
        for mdir in os.listdir(main_dir):
                mat_dir= main_dir + "//" + mdir + "//"

                if not os.path.isdir(mat_dir): continue
                self.dic_imgs[mdir] = []
                for ifl in os.listdir(mat_dir):
                    if ".jpg" in ifl:
                         self.dic_imgs[mdir].append(mat_dir +"/"+ifl)
                         self.list_indx.append({"mat":mdir,"ins_num":len(self.dic_imgs[mdir]),"file":mat_dir +"/"+ifl})
        self.indx=0
        self.finish = False
##################################################################################################################################################
#==========================Go over all images and make one question per image
    def get_next_question(self):
        if self.indx>=len(self.list_indx): return False,0,0
        if self.indx == len(self.list_indx)-1: self.finish=True
        img_data = self.list_indx[self.indx]

        mat = img_data["mat"]  # anchor image material
        anc_path = img_data["file"] # anchor imager path
        self.img_file = img_data["file"]
        nn =  img_data["ins_num"] # anchor instance number
        self.indx += 1
        if len(self.dic_imgs[mat])<2: return self.get_next_question() # there need to be at least two instance of same object for question to generated
        if nn > self.max_img_per_mat:  return self.get_next_question() # limit number of question per object

        #--------------------Select anchor image and positive image-------------------
        anch_im = cv2.imread(anc_path)

        while(True):
                 pos_path = random.choice(self.dic_imgs[mat])
                 if pos_path!= anc_path:
                     pos_im = cv2.imread(pos_path)
                     break
        #---------------Select two negative images
        neg_im=[]
        for kk in range(2):
            while (True):
                neg_mat = random.choice(list(self.dic_imgs.keys()))
                if neg_mat == mat or len(self.dic_imgs[neg_mat]) == 0: continue
                im_path = random.choice(list(self.dic_imgs[neg_mat]))
                neg_im.append(cv2.imread(im_path))
                break



        #----------Create final image--------------------------------------------------------
        pos={'B':[0,512],'C':[512,0],'D':[512,512]}
        choices = ['B','C','D']
        answer=random.choice(choices)


        full_im=np.zeros([1024,1024,3],dtype=np.uint8)
        full_im[:512,:512] = add_text(anch_im,"A")
        y,x= pos[answer]
        full_im[y:y+512,x:x+512]=   add_text(pos_im, answer)

        nneg=0
        for ky in choices:
            if ky != answer:
                y, x = pos[ky]
                full_im[y:y + 512, x:x + 512] = add_text(neg_im[nneg], ky)
                nneg+=1
                if nneg>=len(neg_im):break
        return True,full_im, answer
##########################################################################################################################################################################
#######################################Run full quiz, given a function that receive image and output answer run the full test##############################################
    def  run_test(self,answer_question,ouput_dir="",save_error=False,save_all=False,queries=None):
            if queries is None:
                #"Read the description of the shapes in the next section and tell me which of the panels (B,C,D) describe a similar shape in to the shape in panel A (Not one and only one of the shapes in panels B,C and D is the same as the shape in panel A)\nDescription: ")
                #(     "The image contains 4 panels (A, B, C, D) in each panel there is a shape, describe in detail the shape in each panel. Focus on the invariant aspect of each shape and ignore things like orientation, texture/color of background."), # 74%
                # # -------------------------------------------------Good
                # queries_image = [(
                #                      "The image contain 4 panels (A,B,C,D) in each panel there is a shape, describe in lots of details the shape in each of the panels. Focus on the geometrical aspect and ignore things like texture,color and background.")] * 4 #good use this
                # queries_txt = [(
                #                    "Read the description of the shapes in the next section and tell me which of the panels (B,C,D) describe a similar shape in to the shape in panel A  \nDescription: ")] * 4#Good use this
                # # ---------------------------------------------------------------

                # # -------------------------------------------------Semantic 1

                queries_image = [(
                                     "The image contain 4 panels (A,B,C,D) in each panel there is a shape. Describe in max details the shape in each of the panels. Ignore things like texture,color, background and orientation. Describe each shape independently dont refer to other panels shapes in the description.")] * 4  # good use this Final was used for semanyi
                queries_txt = [(
                                   "Read the description of the shapes in the next section and tell me which of the panels (B,C,D) describe a similar shape in to the shape in panel A. The matching should be rotational invariant. \n Here is the description: ")] * 4  # Good use this final was used for semantic

                # ---------------------------------------------------------------
                #The image contain 4 panels (A,B,C,D) in each panel there is a shape, describe in  details the shape in each of the panels. Focus on the geometrical aspect of each shape and ignore things like texture/color and background.
                # [("The image contain 4 panels (A,B,C,D) in each panel there is a shape, describe in  details the shape in each of the panels. Focus on the invariant aspect of each shape and ignore things like orientation, texture/color of background.")]
                #-------------------------------------------------Good
        #        queries_image = [("The image contain 4 panels (A,B,C,D) in each panel there is a shape give detailed description adn the schematic vectorization of the shape in each panel. Focus on the geometrical aspect and ignore things like texture,color and background.")]*4# Good
         #       queries_txt = [("Read the description of the shapes in the next section and tell me which of the panels (B,C,D) describe a similar shape in to the shape in panel A (note that the shape might be rotated)  \nDescription: ")]*4#Good
#---------------------------------------------------------------
             ##   queries_txt = [("Take the following response and reduce it to a single letter which the selected panel letter B,C,D. If no correct panel is mention in the answer write N. Note response of more than single character is an error. \nHere is the text:\n")]

                # queries = [
                #     ("In the image there is 4 panels each panel contain object made of a specific material texture. Which of the panels B,C or D contain an object with the same material texture as the texture in panel A? Note that the object shape, illumination and background might all be different. Your answer must come as a single letter."),
                #     ("Which of the panels B,C or D, contain object with texture identical to the texture  of the object in panel A? Note that the shape of the object, the enviroment and light might be differnt. Your answer must come as a single letter. Longer answer will not be accepted."),
                #     ("Which of the panels B,C or D contain object with identical texture to the texture of the  object in panel A? Note that the object shape, background enviroment and light might be different look only on the material/texture. Your answer must come as a single letter."),
                #
                # ]
                # queries = [
                #     ("Which panel B,C or D contain shape that have identical texture to the texture in panel A. Note that the shape on which the texture appear and the background  will be different for all panels. Your answer must be a single letter."),   # 92%
                #     ("The image before you contain 4 panels  in each panel there is texture. Which panel  contain a shape that have identical texture to the texture  in panel A? Your answer most come as single letter  B,C or D."),   # 87%
                #     ("Each of the panels contain two seperate textures. One of the panels B,C,D contains a texture that is identical to one of the two textures in panel A. Which panel is it: B,C or D? Your answer must be a single letter."),
                #     ("The image before you contain 4 panels  in each panel there is an object. Which panel  contain a object that have identical texture  to the object in panel A? Your answer most come as single letter  B,C or D."), # 86%
                #     ("The image consists of four panels, each containing a single shape. Your task is to identify the panel where the shape has the same texture as the shape in panel A. Provide your answer as a single letter: B, C, or D.") # 87%
                # ]

                # queries = [
                #     ("Carefully analyze the shapes in all panels. Identify the panel that contains a shape that is identical to the shape in Panel A, regardless of texture, background, or orientation. Your answer should be a single letter corresponding to the correct panel."),  # Open AI 83%
                #     ("Which of the panels contain  shape identical to the shape in panel A . Your answer must come as a single letter and only single letter. Any answer more then one character is an automatic fail."), #openai 82%
                #     ("Which of the panels contain  shape identical to the shape in panel A (but might have different textures, background, orientation). Your answer must come as a single letter.Any answer more then one character is an automatic fail."), # gem 70 openai 82% probably best
                #     ("Carefully analyze the shapes in all panels of the image. Your task is to identify the panel that contains a shape that is identical to the shape in Panel A, regardless of its texture, background, color, or orientation (rotation and reflection). Consider only the shape’s structure and outline. Do not be influenced by differences in shading, patterns, or positioning within the panel. Your response should be a single letter corresponding to the correct panel. Note one and only one of the panels B,C or D will contain shaped identical to the one in panel A. Any answer more then one character is an automatic fail.")#0.78
                #         #("Examine the image carefully and answer. Which of the panels contain  shape identical to the shape in panel A (but with different textures and background and orientation). Your answer must come as a single letter
                # ]
           #-------------------Output dirs for logs--------------------------------------------------------------------------
            if save_error or save_all:
               import shutil
               if os.path.exists(ouput_dir): shutil.rmtree(ouput_dir)
               os.mkdir(ouput_dir)
               error_dir = ouput_dir + "//errors//"
               if save_error and not os.path.exists(error_dir): os.mkdir(error_dir)

           #----------------------------------------------------------------------------------------------

            num_correct = 0
            num_invalid = 0
            num_false = 0
            num_questions = 0
            itr=0
            while (not self.finish):
                itr+=1

                success, quiz_image, answer = self.get_next_question() # get question image
                if not success: break

                if "function" in str(answer_question):
                     ky,logs_txt = answer_question(quiz_image,queries_image=queries_image,queries_text=queries_txt) # get answer from function
                else:
                     ky,logs_txt = answer_question(quiz_image,queries_image=queries_image,queries_text=queries_txt)  # get answer from class
                logs_txt = "\n\n\n###########################################################\n\n\n" + str(num_questions+1) + "):" + self.img_file + "\nCorrect answer: " + answer + "\n" + logs_txt

                if save_all:
                    log_file = open(ouput_dir + "//" + str(num_questions+1) + ".txt","w")
                    log_file.write(logs_txt)
                    log_file.close()
                    cv2.imwrite(ouput_dir + "//" + str(num_questions+1) +"_Answer_"+answer+".jpg",quiz_image)
                if  ky.lower() == answer.lower():
                    num_correct += 1
                    logs_txt += "\nCorrect Answer\n"+ky
                elif ky.lower() in ['b', 'c', 'd']:
                    print("false")
                    num_false += 1
                    logs_txt += "\nWrong Answer: "+ky+' vs correct:' + answer+"\n"
                    if save_error:
                        log_file = open(error_dir + "//" + str(num_questions+1) + ".txt","w")
                        log_file.write(logs_txt)
                        log_file.close()
                        cv2.imwrite(error_dir + "//" + str(num_questions+1) +"_Answer_" + answer+ ".jpg",quiz_image)
                else:
                    print("\n invalid choice")
                    num_invalid += 1
                num_questions += 1
         #       for ddd in range(10):
                print(logs_txt)
                print(num_questions, ")")
                print("correct=", num_correct, " Correct ratio=", num_correct / (num_correct + num_false+0.000001), " ALL=",
                      num_correct / num_questions)
                print("invalid=", num_invalid, "invalid ration=", num_invalid / num_questions)
                if self.max_img2test<=(num_questions-num_invalid): break
            print("correct=", num_correct, " Correct ratio=", num_correct / (num_correct + num_false+0.000001), " ALL=", num_correct / num_questions)
            out_dic =  {"num_questions":num_questions,"num false":num_false,"num invalid":num_invalid, "invalid ratio":(num_invalid / num_questions),"correct" : num_correct, " Correct ratio": num_correct / (num_correct + num_false+0.00001), "ALL": num_correct / num_questions}
            if len(ouput_dir):
                 log_file=open(ouput_dir+"/logs.txt","w")
                 log_file.write(str(out_dic))
                 log_file.close()
            return {"num_questions":num_questions,"num false":num_false,"num invalid":num_invalid, "invalid ratio":(num_invalid / num_questions),"correct" : num_correct, " Correct ratio": num_correct / (num_correct + num_false), "ALL": num_correct / num_questions}





###########################################################################################################################################################
def answer_question(image,queries=[""]):
    while (True):

        cv2.destroyAllWindows()

        cv2.imshow(queries[0], image)
        ky = cv2.waitKey()
        if chr(ky).lower() in ['b', 'c', 'd']:
            return str(chr(ky)), queries[0]+"\nUser Answer: " +str(chr(ky))

#####################################################################################################################################################################
if __name__ == '__main__':
    quiz_maker=make_quize(main_dir = r"/media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/all_tests/Change_only_Random_object_3x_size_object_mapping_mode_no_displacement_3XX/",max_img_per_mat=1,max_img_total=100)
    quiz_maker.run_test(answer_question,ouput_dir="/media/deadcrow/6TB/python_project/Can-large-vision-language-models-understand-materials-and-textures/LOGS_Change_Object_and_background_orient_3x_sizssse//",save_error=True,save_all=True)


