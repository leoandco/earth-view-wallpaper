import os
import random
import re
import shlex
import shutil
import subprocess
import uuid

import requests
from bs4 import BeautifulSoup

WALLPAPER_DIR = os.path.expanduser(os.path.join('~', '.wallpapers'))

if not os.path.exists(WALLPAPER_DIR):
    os.mkdir(WALLPAPER_DIR)

try:
    r = requests.get('https://earthview.withgoogle.com')
    soup = BeautifulSoup(r.content, features='html.parser')

    bg_div = soup.select('div.background')[0]
    bg_url = re.match('background-image: url\((?P<url>.*?)\)', bg_div['style']).group('url')

    r = requests.get(bg_url, stream=True)
    wallpaper_path = os.path.join(WALLPAPER_DIR, uuid.uuid4().hex)
    with open(wallpaper_path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
except requests.RequestException:
    wallpaper_path = os.path.join(WALLPAPER_DIR, random.choice(os.listdir(WALLPAPER_DIR)))

subprocess.check_call(shlex.split('/usr/bin/feh --bg-fill {}'.format(wallpaper_path)))
