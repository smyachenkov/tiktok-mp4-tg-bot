import subprocess
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

VIDEO_OUTPUT_DIR = "/tmp/tiktok/"
TIKTOK_SCRAPER_CMD = "/tmp/node_modules/.bin/tiktok-scraper video {} -d --filepath {}"


def is_tiktok_url(url):
    # todo: implement
    return True


def download_video(url):
    # copy scraper files to tmp directory to allow running it
    # todo: move to another lambda function
    if not os.path.exists("/tmp/node_modules/"):
        logger.info("Copying scraper files")
        subprocess.run("cp -a node_modules /tmp/node_modules/", shell=True)
        subprocess.run("ls -la /tmp/", shell=True)
        subprocess.run("chmod 755 /tmp/node_modules/.bin/tiktok-scraper", shell=True)
    if not os.path.exists(VIDEO_OUTPUT_DIR):
        logger.info("Creating video output directory at %s", VIDEO_OUTPUT_DIR)
        os.mkdir(VIDEO_OUTPUT_DIR)

    logger.info("Downloading video from %s", url)
    p = subprocess.run(
        TIKTOK_SCRAPER_CMD.format(url, VIDEO_OUTPUT_DIR),
        shell=True,
        capture_output=True
    )
    scraper_output = str(p.stdout)
    logger.info(p.stdout)
    logger.info("Video files: %s", os.listdir(VIDEO_OUTPUT_DIR))
    file_name = scraper_output[scraper_output.rfind("/") + 1:scraper_output.index(".mp4") + 4]
    full_file_path = VIDEO_OUTPUT_DIR + file_name
    logger.info("Full video path: %s", full_file_path)
    return full_file_path


def convert_to_gif():
    # todo implement
    p = subprocess.run("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info(p)
