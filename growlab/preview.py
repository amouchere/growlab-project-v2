import os, subprocess, logging, time
from subprocess import check_output
from os import mkdir, path
from os.path import isdir
from PIL import Image, ImageFont, ImageDraw
from jinja2 import Template

class preview:
    def __init__(self, git_opts, image_config):
        self.git_opts = git_opts
        self.image_config = image_config

    def execute(self, command):
        PIPE = subprocess.PIPE

        logger = logging.getLogger("growlab")
        try:
            # logger.info(check_output(command, shell=True))
            process = subprocess.Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()

            logger.info(stdoutput)
            logger.error(stderroutput)
        except subprocess.CalledProcessError as err:
            logger.error(err)

    def check_preview_directory(self):
         # Make sure the repo is cloned
        git_dir = self.git_opts["git_dir"]
        git_path = self.git_opts["git_path"]

        if not isdir(git_dir):
            mkdir(git_dir)
            command = "git clone {} {}".format(git_path, git_dir)
            self.execute(command)


    def publish_preview(self):
        git_dir = self.git_opts["git_dir"]


        command = "cd {} && git pull".format(git_dir)
        self.execute(command)

        # Commit and push
        command = "cd {} && git add . && git commit -m ':bento: Update preview' && git push -f".format(git_dir)
        self.execute(command)

    def prepare_preview(self, input_filename, datetime):
        logger = logging.getLogger("growlab")

        output_path = self.git_opts["git_dir"]

        img = Image.open(input_filename, "r")
        img = img.resize((int(self.image_config["width"]/2), int(self.image_config["height"]/2)), Image.ANTIALIAS)
        img.save(output_path+"/preview.jpg", "JPEG")

        template_text = ""
        with open("resources/index.jinja", 'r') as file:
            template_text = file.read()

        template = Template(template_text)
        vals = {}
        vals["time"] = datetime
        vals["uid"] = "{}".format(time.time())

        html = template.render(vals)
        with open(output_path+"/index.html", "w") as html_file:
            html_file.write(html)
            logger.info("Wrote {}..OK".format(output_path+"/index.html"))