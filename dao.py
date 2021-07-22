import os
import pickle

import pycdlib
import requests

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from game import Game
from serial import Serial

class Dao:

    def __init__(self):
        self.main_path = ""
        self.games = []
        self.invalid_isos = []
        self.not_found_id = []
        self.not_found_cover = []

    def search_iso(self):
        for root, dirs, files in os.walk(self.main_path + 'DVD/'):
            for file in files:
                if file.endswith('.iso'):
                    try:
                        iso = pycdlib.PyCdlib()
                        iso.open(os.path.join(root, file))
                        try:
                            extracted = BytesIO()
                            iso.get_file_from_iso_fp(extracted, iso_path='/SYSTEM.CNF;1')
                            raw = extracted.getvalue().decode('utf-8')
                            game_id = raw[raw.find(':\\') + 2: raw.find(';')]
                            serial = game_id.split('_')
                            if serial[0] in Serial.ntsc_j_c_k_serials:
                                game_region = 'NTSC-J'
                            elif serial[0] in Serial.ntsc_u_serials:
                                game_region = 'NTSC-U'
                            elif serial[0] in Serial.pal_serials:
                                game_region = 'PAL'
                            else:
                                game_region = 'Not Found'
                            game_name = os.path.join(file)[:-4]
                            self.games.append(Game(game_id, game_name, game_region))
                            iso.close()
                        except:
                            iso.close()
                            self.invalid_isos.append([file, "(Could not find/open 'SYSTEM.CNF' file inside ISO)"])
                    except:
                        self.invalid_isos.append([file, "(Could not open ISO file)"])

    def print_all_games(self):
        print(f"Games in {self.main_path}:\n")
        print('Region |   Serial   |   Name\n')
        self.games.sort(key=lambda x: x.name)
        for game in self.games:
            if game.name[:11] == game.id_opl:
                print(f'{game.region} | {game.id_formatted} | {game.name[12:]}')
            else:
                print(f'{game.region} | {game.id_formatted} | {game.name}')
        if len(self.invalid_isos) > 0:
            print('\nInvalid ISO files:\n')
            for iso in self.invalid_isos:
                print(f'{iso[0]} {iso[1]}')

    def get_art_cover(self):
        print("Downloading front cover arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/cover/{game.id_opl}_COV.jpg"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_COV.jpg", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_back_cover(self):
        print("Downloading back cover arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/back_cover/{game.id_opl}_COV2.jpg"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_COV2.jpg", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_spine(self):
        print("Downloading spine arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/spine/{game.id_opl}_LAB.jpg"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_LAB.jpg", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_disc(self):
        print("Downloading disc arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/disc/{game.id_opl}_ICO.png"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_ICO.png", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_background(self):
        print("Downloading background arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/background/{game.id_opl}_BG.jpg"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_BG.jpg", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_logo(self):
        print("Downloading logo arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/logo/{game.id_opl}_LGO.png"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_LGO.png", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_screenshot(self):
        print("Downloading screenshot arts...\n")
        for game in self.games:
            url = f"https://github.com/cristianscheid/ps2art/raw/main/screenshot/{game.id_opl}_SCR.jpg"
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_SCR.jpg", 'wb') as f:
                    f.write(r.content)
                print(f"{game.name} -- Ok")
            else:
                print(f"{game.name} -- Not found")

    def get_art_all(self):
        self.get_art_cover()
        self.get_art_back_cover()
        self.get_art_spine()
        self.get_art_disc()
        self.get_art_background()
        self.get_art_logo()
        self.get_art_screenshot()

    def rename(self):
        # Open 'data' archive and get a list of games with ('id', 'name')
        with open("data", "rb") as fp:
            data = pickle.load(fp)
        # Retrieve only 'id's from list and store in another list
        data_only_ids = []
        for i in data:
            data_only_ids.append(i[0])
        # Create list of ids from the games renamed
        id_games_renamed = []
        self.games.sort(key=lambda x: x.name)
        for game in self.games:
            if game.id_formatted in data_only_ids:
                # The 'index()' method returns the position at the first occurrence of the specified value
                index = data_only_ids.index(game.id_formatted)
                if game.id_formatted not in id_games_renamed:
                    new_name = f"{game.id_opl}.{data[index][1]}"
                    os.rename(f"{self.main_path}DVD/{game.name}.iso", f"{self.main_path}DVD/{new_name}.iso")
                    game.name = new_name
                    id_games_renamed.append(game.id_formatted)
                # If the game is duplicated, rename appending 'Copy'
                else:
                    new_name = f"{game.id_opl}.{data[index][1]} Copy {id_games_renamed.count(game.id_formatted)}"
                    os.rename(f"{self.main_path}DVD/{game.name}.iso", f"{self.main_path}DVD/{new_name}.iso")
                    game.name = new_name
                    id_games_renamed.append(game.id_formatted)
            else:
                self.not_found_id.append(game)
        # Empty list of renamed games in case the 'rename' function is called again
        id_games_renamed.clear()
