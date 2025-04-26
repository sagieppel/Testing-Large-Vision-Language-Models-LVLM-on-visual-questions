# Run 

Test Large Vision Language Models on multichoice visual matching test. Work for GPT,LLAMA,Claude,GROK,QWEN and Gemini.

The classes are general **api_class.py are classes for visual query of the main models (gemini,LLama,Claude,Gemini,QWEN,GROK).

QuizMakingClass.py Assume that the images in the test folder and with .jpg. And that each leaf subfolder contain images of same instance.

Generate 4 panel image in panel A and another random panel belong to same instance (Sub folders) and the rest of the images are of different instances.

Use this images to test the models.

# How to use:
Get API keys and set models API key in API_KEYS.py.

In **Quiz.py set path to image dir in in_dir parameter (You cant use the test_images folder supplied).

Set path to output folder where results will be saved to out_folder.

# Data
The Quiz script can run with any image matching test as long as the images are are arranged in folders and images of the same instance appear in the same folder (whil images belonging to different instance appear in different folder).
In addition the images must be in .jpg folders (other images will be ignored). Excet this any folder structure and file name are fine.

Example test data can be found in test_images folder.

For the images used for shapes, textures, materials matching test see the [LAS&T benchmark] [All](https://github.com/sagieppel/Shape-and-Texture-recognition-in-large-vision-language-models-), [All Mirror](https://icedrive.net/s/CPvz3jZ6hV4WGhQ4v4TA5B3785T5), [3d shapes](https://zenodo.org/records/14681299).

Run script.

###  For more details see: [Shape and texture recognition in large vision-language models](https://arxiv.org/pdf/2503.23062)  and  [Do large language vision models understand 3D shapes?](https://arxiv.org/pdf/2412.10908)
