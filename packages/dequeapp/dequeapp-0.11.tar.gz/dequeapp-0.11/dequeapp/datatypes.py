from PIL import Image
import pickle
import json
import time
import numpy as np

class DequeImage:
    def __init__(self, image:Image ):
        self._image = np.array(image)
        self.type = "Deque.Image"




if __name__ == "__main__":
    with Image.open("/home/riju/Downloads/riju-pahwa.png") as im:
        im = im.tobytes()
    di = DequeImage(image=im)

    print(di.to_json(di))


