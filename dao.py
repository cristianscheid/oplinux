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

    def path_exists(self):
        if self.main_path[-1] != '/':
            self.main_path += '/'
        if self.main_path[-4:] == 'DVD/':
            string_len = len(self.main_path)
            self.main_path = self.main_path[:string_len - 4]
        if self.main_path[0:1] == '~':
            new_string = f"/home/{os.getlogin()}{self.main_path[1:]}"
            self.main_path = new_string
        if os.path.exists(self.main_path):
            return True
        return False

    def search_iso(self):
        self.games.clear()
        self.invalid_isos.clear()
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
                            id_opl = raw[raw.find(':\\') + 2: raw.find(';')]
                            serial = id_opl.split('_')
                            if serial[0] in Serial.ntsc_j_c_k_serials:
                                region = 'NTSC-J'
                            elif serial[0] in Serial.ntsc_u_serials:
                                region = 'NTSC-U'
                            elif serial[0] in Serial.pal_serials:
                                region = 'PAL'
                            else:
                                region = 'Not Found'
                            file = os.path.join(file)
                            name = file[:-4]
                            # If the ISO file has the id in front of the name, ignore the id
                            # This way only the name is saved as the game name
                            if name[:11] == id_opl:
                                name = name[12:]
                            self.games.append(Game(id_opl, file, name, region))
                            iso.close()
                        except:
                            iso.close()
                            self.invalid_isos.append([file, "(Could not find/open 'SYSTEM.CNF' file inside ISO)"])
                    except:
                        self.invalid_isos.append([file, "(Could not open ISO file)"])
        self.games.sort(key=lambda x: x.name)

    def print_all_games(self):
        print(f"Games in '{self.main_path}':\n")
        print('Region |   Serial   |   Name\n')
        for game in self.games:
            print(f'{game.region} | {game.id_formatted} | {game.name}')
        if len(self.invalid_isos) > 0:
            print('\nInvalid ISO files:\n')
            for iso in self.invalid_isos:
                print(f'{iso[0]} {iso[1]}')

    def rename(self):
        # Open 'data' archive and get a list of games with ('id', 'name')
        with open("data", "rb") as fp:
            data = pickle.load(fp)
        # Retrieve only id's from list and store in another list
        data_only_ids = []
        for i in data:
            data_only_ids.append(i[0])
        # Create list of id's from the games renamed
        id_games_renamed = []
        # Empty list in case the function is called more then once
        id_games_renamed.clear()
        for game in self.games:
            if game.id_formatted in data_only_ids:
                # The index() method returns the position at the first occurrence of the specified value
                index = data_only_ids.index(game.id_formatted)
                if game.id_formatted not in id_games_renamed:
                    new_name = f"{data[index][1]}"
                    os.rename(f"{self.main_path}DVD/{game.file}", f"{self.main_path}DVD/{game.id_opl}.{new_name}.iso")
                    game.name = new_name
                    id_games_renamed.append(game.id_formatted)
                # If the game has copies, rename appending 'Copy + {number of the copy}'
                else:
                    new_name = f"{data[index][1]} Copy {id_games_renamed.count(game.id_formatted)}"
                    os.rename(f"{self.main_path}DVD/{game.file}", f"{self.main_path}DVD/{game.id_opl}.{new_name}.iso")
                    game.name = new_name
                    id_games_renamed.append(game.id_formatted)
            else:
                self.not_found_id.append(game)

    def get_art_cover(self):
        print("\nDownloading front cover arts...\n")
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
        print("\nDownloading back cover arts...\n")
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
        print("\nDownloading spine arts...\n")
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
        print("\nDownloading disc arts...\n")
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
        print("\nDownloading background arts...\n")
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
        print("\nDownloading logo arts...\n")
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
        print("\nDownloading screenshot arts...\n")
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
