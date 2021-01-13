import moviepy.editor as mp
import numpy
from chromakey import Chromakey


def remove_green_screen(image):
    image = Chromakey(image).simple_cutout()
    result = numpy.array(image)
    image.close()
    return result


video = mp.VideoFileClip('assets/small-green.mp4')
bg = mp.ImageClip('assets/bg.jpg', duration=video.duration)
bg = bg.set_fps(video.fps)
bg = bg.resize(video.size)

video = video.fl_image(remove_green_screen)

final = mp.CompositeVideoClip([bg])
final.write_videofile('result.mp4')
