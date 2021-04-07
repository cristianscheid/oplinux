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
                            game_path = os.path.join(root, file)
                            self.games.append(Game(game_id, game_name, game_path, game_region))
                            iso.close()
                        except:
                            iso.close()
                            self.invalid_isos.append([file, "(Could not find/open 'SYSTEM.CNF' file inside ISO)"])
                    except:
                        self.invalid_isos.append([file, "(Could not open ISO file)"])

    def get_cover(self):
        for game in self.games:
            url = f'https://github.com/cristianscheid/ps2art/raw/main/{game.id_opl}_COV.jpg'
            r = requests.get(url)
            print(r.status_code)
            if r.status_code == 200:
                with open(f"{self.main_path}ART/{game.id_opl}_COV.jpg", 'wb') as f:
                    f.write(r.content)
            else:
                print(game.id_opl)

    def rename(self):
        # Open 'database' and get a list with ('id', 'name')
        with open("data", "rb") as fp:
            data = pickle.load(fp)
        # Retrieve only 'id's from list and store in another list
        data_only_ids = []
        for i in data:
            data_only_ids.append(i[0])

        for game in self.games:
            if game.id_formatted in data_only_ids:
                index = data_only_ids.index(game.id_formatted)
                os.rename(game.path, f"{self.main_path}DVD/{game.id_opl}.{data[index][1]}.iso")