from chromakey import Chromakey

image = Chromakey('assets/tv.jpg', color='#15fd15', lower_ratio=0.5)
image.simple_cutout().show()
