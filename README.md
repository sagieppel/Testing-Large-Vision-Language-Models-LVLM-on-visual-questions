# Run 

Test Large Vision Language Models on multichoice visual matching test. Work for GPT,LLAMA,Claude,GROK,QWEN and Gemini.

The files with name **api_class.py are classes for visual query of the main models using API They can be used to upload image and queries using API of main providers (gemini,LLama,Claude,Gemini,QWEN,GROK).


QuizMakingClass.py Assume that the images are in the test folder and with .jpg. Each leaf subfolder contains images of the same instance. While images in different folders belong to different instances.

Generate image with for panels, The image in panel A and another random panel (C, B, D) belong to the same instance (Subfolders) and the rest of the images are of different instances.
The test is whether the human or model can identify which of the panels (C, B, D) contain the same instance as the one in panel A (for example the same 3D shape, 2D shape, or material).
The input data are images of .jpg type arranged in subfolders where the images in the same folder belong to the same object (for example same 3D shape but rotated) 
and images in different folders belong to different instances (for example different 3D shapes).
See test_images folder for example.


![Example for quiz image made by QuizMakingClass.py identify which panel contain instance (3D shape) identical to the one in panel A](Figure1.jpg)

# How to use:
Get API keys and set the model API key in API_KEYS.py.

In **Quiz.py set path to image dir in in_dir parameter (You cant use the test_images folder supplied).

Set path to output folder where results will be saved to out_folder.


# Testing Humans:

The running QuizMakingClass.py main directly will run the test on the screen and allow the user to choose answers using the keyboard (For testing humans). 

# Data
The Quiz script can run with any image matching test as long as the images are arranged in folders and images of the same instance appear in the same folder (while images belonging to different instances appear in different folders).
In addition, the images must be in .jpg folders (other images will be ignored). Excet this any folder structure and file name are fine.

Example test data can be found in the test_images folder.

For the images used for shapes, textures, and materials matching test see the [LAS&T benchmark] [All](https://github.com/sagieppel/Shape-and-Texture-recognition-in-large-vision-language-models-), [All Mirror](https://icedrive.net/s/CPvz3jZ6hV4WGhQ4v4TA5B3785T5), [3d shapes](https://zenodo.org/records/14681299).

Run script.

###  For more details see: [Shape and texture recognition in large vision-language models](https://arxiv.org/pdf/2503.23062)  and  [Do large language vision models understand 3D shapes?](https://arxiv.org/pdf/2412.10908)
