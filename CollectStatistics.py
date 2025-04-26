import numpy as np
import cv2
import os
import json
import shutil
sample_dir=r"//media/deadcrow/SSD_480GB/segment_anything/2D_Shape_Matching_Tests-TXT2TXT_GEMINI1.5_NeW/"
main_dir="/media/deadcrow/SSD_480GB/segment_anything/"
out_file=r"/media/deadcrow/SSD_480GB/segment_anything/txt2txt8.xls"

'''
sample_dir=r"/media/deadcrow/SSD_480GB/segment_anything/Test_Textures_Results_claude-3-5-sonnet/"
main_dir="/media/deadcrow/SSD_480GB/segment_anything/"
out_file=r"/media/deadcrow/SSD_480GB/segment_anything/textures2d_full_results.xls"
'''

st_dic={}
fields=[]
# collect fields
for dr in os.listdir(sample_dir):
    if os.path.isdir(sample_dir+"/"+dr):
            st_dic[dr]={}
            fields.append(dr)
nets=[]
# create statitics
for dr in  os.listdir(main_dir):
    dr1=main_dir+"/"+dr
    if os.path.isdir(dr1):
        for sdr in os.listdir(dr1):
            if sdr in fields:
                path=dr1+"/"+sdr+"/logs.txt"
                # Open the JSON file
                if os.path.exists(path):
                    import ast
                    with open(path, "r") as file:
                        data = file.read().strip()
                    parsed_data = ast.literal_eval(data)  # Safely parse the dictionary
                    all_value = parsed_data.get(" Correct ratio", None)
                    print(all_value)
                    st_dic[sdr][dr] = all_value
                    if dr not in nets:
                                nets.append(dr)
txt="Model/Set\t"
for st in fields: txt+=st+"\t"

for nt in nets:
    txt+="\n"+nt+"\t"
    for st in fields:
        if nt in st_dic[st]:
            txt+=str(st_dic[st][nt])+"\t"
        else:
            txt += "X\t"
fl=open(out_file,"w")
fl.write(txt)
fl.close()


# write files



