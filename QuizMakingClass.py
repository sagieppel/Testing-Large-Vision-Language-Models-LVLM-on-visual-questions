# Create 4 panel quiz in which the goal is to find which panel B,C,D  is identical to the object in panel a in term of some property
# Assume the images already given and arrange according to class/object_instatnce/image.jpg

import cv2
import os
import random
import numpy as np
######################################################################################################################################
def add_text(image,text): # Add text to image

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
############################colldect data images/and instance aon all instances from dir#############################################################################################
# Note all images belonging to the same instance must be in the same dir and have .jpg file, other then this the dir structure doesnt matter
def collect_folder_data(dr,dr_name="", dic_imgs = {},list_indx = []):
    for ifl in os.listdir(dr):
        path = dr + "/" + ifl
        if ".jpg" in ifl:  # if the folder structure is  mdir/instance_dir/img.jpg
            if dr_name not in dic_imgs: dic_imgs[dr_name] = []  # all the images belong to specific folder
            dic_imgs[dr_name].append(path)
            list_indx.append({"mat": dr_name, "ins_num": len(dic_imgs[dr_name]), "file": path})
        else:
            if os.path.isdir(path):
                dic_imgs, list_indx=collect_folder_data(path, dr_name=dr_name+"_"+ifl, dic_imgs=dic_imgs, list_indx=list_indx)
    return  dic_imgs, list_indx




####################################################################################################################################
class make_quize():
    def __init__(self,main_dir = r"",max_img_per_mat=10,max_img_total=10000):
        self.max_img_per_mat=max_img_per_mat # Total number of image to test per instance
        self.max_img2test=max_img_total # total number of image to test
        self.main_dir=main_dir # main folder with image divided into main_dir/class_dir/object_dir/instance_image.png
              #=========================Create dictionary of all images===============================
        self.dic_imgs={} # structure that will contain all images arrange by instance and index
        self.list_indx = []  # list of all images

        self.dic_imgs, self.list_indx = collect_folder_data(main_dir)

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

     #---------Output dirs for logs--------------------------------------------------------------------------
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
                     ky,logs_txt = answer_question(quiz_image,queries=queries) # get answer from function
                else:
                     ky,logs_txt = answer_question.answer_question(quiz_image,queries=queries)  # get answer from class
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
    test_dir = "test_images//"
    results_dir = "test_resulrs//"
    queries=["Which panel contain identical (B,C,D) shape to the one in panel A, press letter to choose"]
    quiz_maker=make_quize(main_dir = test_dir,max_img_per_mat=1,max_img_total=100)
    quiz_maker.run_test(answer_question,ouput_dir=results_dir,save_error=True,save_all=True,queries=queries)


