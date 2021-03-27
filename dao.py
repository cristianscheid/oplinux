import os
import pickle

import pycdlib
import re
import requests

from game import Game
from serial import Serial


class Dao:

    def __init__(self):
        self.games = []
        self.invalid_iso_files = []
        self.main_path = ""

    def search_iso(self):
        # Get '.iso' files in the 'DVD' folder
        for root, dirs, files in os.walk(self.main_path + 'DVD/'):
            for file in files:
                if file.endswith(".iso"):
                    iso = pycdlib.PyCdlib()
                    # Get 'id'/check if is a valid (PSX) file
                    try:
                        iso.open(os.path.join(root, file))
                        for child in iso.list_children(iso_path='/'):
                            raw = str(child.file_identifier())
                            for serial in Serial.all_serials:
                                # If is a valid '.iso' create a 'Game' object and add to the 'games' list
                                if raw.find(serial) != -1:
                                    if serial in Serial.ntsc_j_c_k_serials:
                                        game_region = 'NTSC-J/C/K'
                                    elif serial in Serial.ntsc_u_serials:
                                        game_region = 'NTSC-U'
                                    else:
                                        game_region = 'PAL'
                                    temp = re.findall(r'\d+', raw)
                                    game_id = [serial, temp[0], temp[1]]
                                    game_name = os.path.join(file)[:-4]
                                    game_path = os.path.join(root, file)
                                    self.games.append(Game(game_id, game_name, game_path, game_region))
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
        # Opens 'database' and get a list with ('id', 'name')
        with open("data", "rb") as fp:
            data = pickle.load(fp)
        # Retrieve only 'id's from list and store in another list
        data_only_ids = []
        for i in data:
            data_only_ids.append(data[0])
        # If a game 'id' is in the database, file is renamed with the official name
        for game in self.games:
            if game.get_formatted_id() in data_only_ids:
                index = data_only_ids.index(game.get_formatted_id())
                os.rename(game.path, f"{self.main_path}DVD/{game.get_formatted_id}.{data[1][index]}.iso")
