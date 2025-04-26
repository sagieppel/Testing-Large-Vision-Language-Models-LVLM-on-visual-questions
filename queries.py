PbrMaterials2D = [
    ("In the image there is 4 panels each panel contain object made of a specific material texture. Which of the panels B,C or D contain an object with the same material texture as the texture in panel A? Note that the object shape, illumination and background might all be different. Your answer must come as a single letter."),
    ("Which of the panels B,C or D, contain object with texture identical to the texture  of the object in panel A? Note that the shape of the object, the enviroment and light might be differnt. Your answer must come as a single letter. Longer answer will not be accepted."),
    ("Which of the panels B,C or D contain object with identical texture to the texture of the  object in panel A? Note that the object shape, background enviroment and light might be different look only on the material/texture. Your answer must come as a single letter."),

]
Textures2D = [
    (
        "Which panel B,C or D contain shape that have identical texture to the texture in panel A. Note that the shape on which the texture appear and the background  will be different for all panels. Your answer must be a single letter."),

    (
        "The image before you contain 4 panels  in each panel there is texture. Which panel  contain a shape that have identical texture to the texture  in panel A? Your answer most come as single letter  B,C or D."),

    (
        "Each of the panels contain two seperate textures. One of the panels B,C,D contains a texture that is identical to one of the two textures in panel A. Which panel is it: B,C or D? Your answer must be a single letter."),
    (
        "The image before you contain 4 panels  in each panel there is an object. Which panel  contain a object that have identical texture  to the object in panel A? Your answer most come as single letter  B,C or D."),
    (
        "The image consists of four panels, each containing a single shape. Your task is to identify the panel where the shape has the same texture as the shape in panel A. Provide your answer as a single letter: B, C, or D.")

]

Shapes2D = [
    ("Carefully analyze the shapes in all panels. Identify the panel that contains a shape that is identical to the shape in Panel A, regardless of texture, background, or orientation. Your answer should be a single letter corresponding to the correct panel."),  # Open AI 83%
    ("Which of the panels contain  shape identical to the shape in panel A . Your answer must come as a single letter and only single letter. Any answer more then one character is an automatic fail."), #openai 82%
    ("Which of the panels contain  shape identical to the shape in panel A (but might have different textures, background, orientation). Your answer must come as a single letter.Any answer more then one character is an automatic fail."), # gem 70 openai 82% probably best
    ("Carefully analyze the shapes in all panels of the image. Your task is to identify the panel that contains a shape that is identical to the shape in Panel A, regardless of its texture, background, color, or orientation (rotation and reflection). Consider only the shape’s structure and outline. Do not be influenced by differences in shading, patterns, or positioning within the panel. Your response should be a single letter corresponding to the correct panel. Note one and only one of the panels B,C or D will contain shaped identical to the one in panel A. Any answer more then one character is an automatic fail.")#0.78
        #("Examine the image carefully and answer. Which of the panels contain  shape identical to the shape in panel A (but with different textures and background and orientation). Your answer must come as a single letter
]


Objects3D = [
    ("Which of the panels contains an object with an identical 3D shape to the object in panel A. Your answer must come as a single letter"),
    ("Which of the panels contains an object with an identical 3D shape to the object in panel A. Ignore orientation texture and background and focus only on the shape. Your answer must come as a single letter"),
    ("Which of the panels contains an object with an identical 3D shape to the object in panel A. Ignore orientation texture and background and focus only on the shape. Your answer must come as a single letter and only single letter (B,C,D)")

]