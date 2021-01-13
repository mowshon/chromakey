from chromakey import Chromakey

image = Chromakey('images/cyan.jpg')
image.alpha_matting_cutout().show()
