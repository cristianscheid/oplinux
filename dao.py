import os
import pycdlib
import re
import requests
from bs4 import BeautifulSoup

from game import Game


class Dao:

    def __init__(self):
        self.games = []
        self.invalid_iso_files = []
        self.main_path = ""

    def search_iso(self):
        serials = ('SCUS', 'SLUS', 'SCES', 'SLES')
        for root, dirs, files in os.walk(self.main_path + 'DVD/'):
            for file in files:
                if file.endswith(".iso"):
                    iso = pycdlib.PyCdlib()
                    try:
                        iso.open(os.path.join(root, file))
                        for child in iso.list_children(iso_path='/'):
                            raw = str(child.file_identifier())
                            for serial in serials:
                                if raw.find(serial) != -1:
                                    temp = re.findall(r'\d+', raw)
                                    game_id = [serial, temp[0], temp[1]]
                                    game_name = os.path.join(file)
                                    game_path = os.path.join(root, file)
                                    self.games.append(Game(game_id, game_name, game_path))
                                    iso.close()
                                    break
                    except:
                        self.invalid_iso_files.append(os.path.join(file))

    def get_cover(self):
        for i in range(len(self.games)):
            url = f'https://psxdatacenter.com/psx2/images2/covers/{self.games[i].get_formatted_id_url}.jpg'
            r = requests.get(url)
            print(r.status_code)
            if r.status_code != 404:
                with open(f"{self.main_path}ART/{self.games[i].get_formatted_id}_COV.jpg", 'wb') as f:
                    f.write(r.content)

    def rename(self):
        for i in range(len(self.games)):
            url = 'https://psxdatacenter.com/psx2/ulist2.html'
            # https://psxdatacenter.com/psx2/plist2.html
            # https://psxdatacenter.com/psx2/jlist2.html
            content = requests.get(url)
            soup = BeautifulSoup(content.text, 'html.parser')
            result = soup.find(string=re.compile(self.games[i].get_formatted_id_url)).find_next(
                "td").text.strip().title()
            os.rename(self.games[i].path, f"{self.main_path}DVD/{self.games[i].get_formatted_id}.{result}.iso")
