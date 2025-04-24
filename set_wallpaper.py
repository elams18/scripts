#!/usr/bin/python3
from appscript import app, mactypes
from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()

CLIENT_KEY = os.getenv("CLIENT_KEY")
BASE_DIR = os.getenv("BASE_DIR", os.curdir)


def get_random_image(file_name: str):
    wallpaper_data = requests.get(
        f"https://api.unsplash.com/photos/random?page=1&query=search&client_id={CLIENT_KEY}"
    )
    wallpaper_url = wallpaper_data.json()["urls"]["full"]
    picsum_url = "https://picsum.photos/2560/1440"

    wallpaper_content = requests.get(picsum_url, stream=True)

    url_format = "https://images.unsplash.com/(.*)?crop=(.*)&cs=(.*)&fm=(.*)&ixid=(.*)ixlib=(.*)&q=(.*)"

    match = re.match(url_format, wallpaper_url)
    fm = match.group(4)

    file_path = os.path.join(BASE_DIR, f"assets/{file_name}.{fm}")
    with open(file_path, "wb") as handle:
        for chunk in wallpaper_content.iter_content(chunk_size=500):
            handle.write(chunk)

    return file_path


def set_wallpaper(file_path: str):
    try:
        app("Finder").desktop_picture.set(mactypes.File(file_path))
    except Exception as e:
        print(e)


def set_screen_saver(file_path: str):
    try:
        # Get the System Events application
        system_events = app("System Events")

        # Get the Screen Saver preferences
        screen_saver_prefs = system_events.preferences.screen_saver

        # Set the new wallpaper
        screen_saver_prefs.picture_path.set(mactypes.File(file_path))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    wallpaper_path = get_random_image("wallpaper")
    set_wallpaper(wallpaper_path)
    # screen_saver_path = get_random_image("screen_saver_path")
    # set_screen_saver(screen_saver_path)
