import time
import shutil
import logging
from time import gmtime, strftime
import os

class timelapse:
    def __init__(self, timelapse_config):
        self.timelapse_config = timelapse_config

    def isActivated(self):
        return self.timelapse_config["active"]
        
    def copyFile(self, old_path):
        logger = logging.getLogger("growlab")

        timelapse_directory = self.timelapse_config["timelapse_directory"]
        # check if the directory already exists
        if not os.path.exists(timelapse_directory):
            os.mkdir(timelapse_directory)
            logger.info("Directory {} Created.".format(timelapse_directory))
        else:    
            logger.info("Directory {} already exists..".format(timelapse_directory))

        # create new path from timelapse_directory, the filename and the timestamp
        new_path = timelapse_directory + strftime("%Y-%m-%d_%H-%M-%S_", gmtime()) + "timelapse.jpg"

        # copy the file to the new path
        try:
            shutil.copy(old_path, new_path)
        # eg. src and dest are the same file
        except shutil.Error as e:
            print(f"Error: {e}")
        # eg. source or destination doesn't exist
        except IOError as e:
            print(f"Error: {e.strerror}")