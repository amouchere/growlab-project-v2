#!/bin/python3

import json, logging, os, sys 
import pytz
from time import sleep
from camera import camera
from timelapse import timelapse
from preview import preview
from datetime import datetime

def main():
    # Create logger
    logging.basicConfig(filename='/home/pi/growlab.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger("growlab")

    print("-----------")
    logging.info("================")
    logging.info("Starting growlab")
    logging.info("================")

    logging.info(os.getcwd())

    # Parse config file
    config = {}
    try:
        with open("./resources/config.json") as f:
            config = json.loads(f.read())
    except Exception as e:
        logging.error("Error: {}".format(e))
        sys.exit(1)

    logging.info("Loaded config, saving images every {} seconds to {}".format( config["timelapse"]["interval_seconds"], config["image"]["output_directory"]))

    # initialize objects
    prev = preview(config["preview"], config["image"])
    cam = camera(config["image"])
    timlap = timelapse(config["timelapse"])
    pwd = os.getcwd()


    while True:
        
        tz_Paris = pytz.timezone('Europe/Paris')
        datetime_Paris = datetime.now(tz_Paris)
        hour = datetime_Paris.hour

        logging.info("=== New capture in progress ... ")

        # get new image
        image_path = cam.capture()
        
        # Archive for timelapse 
        if (timlap.isActivated()):
            timlap.copyFile(image_path)
            logging.info("=== Image archiving : done")
        else:
            logging.info("=== Image archiving : disabled")

        # Build preview files (image )
        prev.check_preview_directory()

         # Save image with incrusted data from sensors
        prev.prepare_preview(image_path, datetime_Paris)
        logging.info("=== Preview preparation : done")

        # Publish the preview
        prev.publish_preview()
        logging.info("=== Preview publishing : done")
                    
        logging.info("... sleep for {} seconds".format(config["timelapse"]["interval_seconds"]))
        sleep(config["timelapse"]["interval_seconds"])

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.error(type(e).__name__)
            logging.exception(e)
            raise e
