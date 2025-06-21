#!/usr/bin/python3
from appscript import app, mactypes
from dotenv import load_dotenv
import os
import requests
import subprocess
import re

load_dotenv()

BASE_DIR = os.getenv("BASE_DIR", os.curdir)


def get_random_image(file_name: str):
    picsum_url = "https://picsum.photos/2560/1440"
    wallpaper_content = requests.get(picsum_url, stream=True)
    file_path = os.path.join(BASE_DIR, f"assets/{file_name}.jpg")
    with open(file_path, "wb") as handle:
        for chunk in wallpaper_content.iter_content(chunk_size=500):
            handle.write(chunk)

    print(file_path)
    return file_path


def set_wallpaper(screen_num: int, file_path: str):
    try:
        # app("Finder").desktop_picture.set(mactypes.File(file_path))
        print(f"Changing wallpaper for screen {screen_num}")
        script = f"""
        tell application "System Events"
            tell desktop {screen_num}
                set the size of the picture to the size of the desktop
                set picture to "{file_path}"
            end tell
        end tell
        """
        command = ["osascript", "-e", script]
        subprocess.call(command)
        print(script, command)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    wallpaper_path = get_random_image("wallpaper")
    set_wallpaper(1, wallpaper_path)
    set_wallpaper(2, wallpaper_path)
