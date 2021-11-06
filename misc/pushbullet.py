#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pushbullet.py
Push a file or text message to Pushbullet.

Place a txt-file in the same folder as this script containing your pushbullet token.
"""
import requests
import argparse
import json
import logging
from pathlib import Path


class Pushbullet:
    def __init__(self):
        self.endpoints = {
            "devices": "https://api.pushbullet.com/v2/devices",
            "chats": "https://api.pushbullet.com/v2/chats",
            "channels": "https://api.pushbullet.com/v2/channels",
            "me": "https://api.pushbullet.com/v2/users/me",
            "push": "https://api.pushbullet.com/v2/pushes",
            "upload_request": "https://api.pushbullet.com/v2/upload-request",
            "ephemerals": "https://api.pushbullet.com/v2/ephemerals"
        }

        # Get access token
        token_path = Path(__file__).parent / "pushbullet.txt"
        try:
            self.access_token = token_path.read_text()
        except Exception as e:
            logging.error(e)
            logging.error(f"Couldn't get the access token")

        self.headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    def get_file_type(self, file_name):
        """Determine the post type based on file type"""
        if str(file_name).lower().endswith((".jpg", ".jpeg")):
            post_type = "image/jpeg"
        # elif file_name.lower().endswith((".mov", ".mp4", ".mpg", ".avi", ".flv", ".mkv", ".m4v")):
        #     post_type = "video"
        # elif file_name.lower().endswith((".png", ".gif", ".bmp", ".tif", ".tif")):
        #     post_type = "audio"
        else:
            post_type = None

        return post_type

    def upload_file(self, file_path, file_type=None):
        """Upload a file to pushbullet"""
        headers = self.headers
        file_path = Path(file_path).resolve()
        file_name = file_path.name

        # Get the file type if it's not entered
        if not file_type:
            file_type = self.get_file_type(file_name)

        upload_request_data = {"file_name": file_name,
                               "file_type": file_type}

        upload_request = requests.post(self.endpoints["upload_request"],
                                       headers=headers,
                                       data=json.dumps(upload_request_data)
                                       )
        logging.debug(upload_request)

        # Get json from upload request
        upload_request_json = upload_request.json()
        logging.debug(upload_request_json)

        # Upload file
        file_upload = requests.post(upload_request_json["upload_url"],
                                    files={"file": open(file_path, "rb")})

        return upload_request_json

    def send_push(self, body=None, title=None, file=None):
        """Send a push notification to pushbullet"""
        headers = self.headers
        data = {"type": "note"}

        # Send a file push
        if file is not None:
            file_upload = self.upload_file(file)

            data = {"type": "file",
                    "file_type": file_upload["file_type"],
                    "file_url": file_upload["file_url"],
                    "file_name": file_upload["file_name"],
                    }

        # Add the body content
        if body:
            data["body"] = body

        if title:
            data["title"] = title

        logging.debug(data)

        # Send request
        push_response = requests.post(self.endpoints["push"],
                                      headers=headers,
                                      data=json.dumps(data)
                                      )
        push_response_json = push_response.json()
        logging.debug(push_response_json)

        return push_response_json


def logger(level):
    """Create a logger with file and stream handler"""
    # Create logger
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    if level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif level == 'info':
        logger.setLevel(logging.INFO)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create file handler and set level to debug
    fh = logging.FileHandler('tjj-bot.log', mode='a')
    fh.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def main():
    """docstring for main"""
    # Create logger
    logger("info")

    parser = argparse.ArgumentParser(description="Push a piece of text and/or image")
    parser.add_argument("body",
                        help="an integer for the accumulator",
                        type=str)
    parser.add_argument("-f", "--file",
                        help="File to push",
                        type=str,
                        action="store")
    parser.add_argument("-t", "--title",
                        help="Title of the push",
                        type=str,
                        action="store")

    args = parser.parse_args()

    if args:
        push = Pushbullet()

        title = args.title
        file = args.file
        body = args.body

        if Path(args.body).is_file():
            file = args.body
            body = None
        push.send_push(title=title, body=body, file=file)


if __name__ == "__main__":
    main()
