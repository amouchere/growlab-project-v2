import time
from picamera2 import Picamera2
from libcamera import Transform
from os import mkdir, path
from os.path import isdir

class camera:
    def __init__(self, camera_opts):
        self.camera_opts = camera_opts
        output_directory = self.camera_opts["output_directory"]
        if not isdir(output_directory):
            mkdir(output_directory)

    def capture(self):
        output_directory = self.camera_opts["output_directory"]
        picam = Picamera2()

        config = picam.create_preview_configuration(
            main={"size": (self.camera_opts["width"], self.camera_opts["height"])}, 
            transform=Transform(hflip=self.camera_opts["horizontal_flip"], vflip=self.camera_opts["vertical_flip"]))
        picam.configure(config)

        picam.start()
        time.sleep(2)
        image_path = output_directory + "image.jpg"
        picam.capture_file(image_path)

        picam.close()
        return image_path
