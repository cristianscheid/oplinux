import os

import pyfiglet as pyfiglet
import time


class View:

    def __init__(self, dao):
        self.dao = dao
        self.slp_time = 2
        self.i = 0

    def print_logo(self):
        os.system('clear')

        logo = pyfiglet.figlet_format("OPLinux")

        print(logo)

    def path_input(self):
        self.print_logo()

        if self.i == 0:
            print("by Cristian Scheid\n")
            time.sleep(2)
            self.print_logo()
            self.i += 1

        # self.dao.main_path = '~/PS2'
        self.dao.main_path = input("Insert the path of your OPL folder as below:\n\n"
                                   "'/home/user/MyOPLFolder/' or '~/MyOPLFolder/'\n\n---> ")

    def path_exists(self):
        exists = False
        if self.dao.main_path[-1] != '/':
            self.dao.main_path += '/'
        if self.dao.main_path[-4:] == 'DVD/':
            string_len = len(self.dao.main_path)
            self.dao.main_path = self.dao.main_path[:string_len - 4]
        if self.dao.main_path[0:1] == '~':
            new_string = f"/home/{os.getlogin()}{self.dao.main_path[1:]}"
            self.dao.main_path = new_string
        if not os.path.exists(self.dao.main_path):
            print("\nInvalid path(doesn't exist)!")
            time.sleep(self.slp_time)
            return False
        return True

    def how_many_games(self):
        self.print_logo()
        if len(self.dao.games) < 1:
            print(f"No PSX game found in '{self.dao.main_path}'\nPlease check the path/folder")
            time.sleep(self.slp_time)
        elif len(self.dao.invalid_iso_files) < 1:
            print(f"Found in '{self.dao.main_path}':\n\n-> {len(self.dao.games)} PSX games")
        else:
            print(
                f"Found in '{self.dao.main_path}':\n\n-> {len(self.dao.games)} PSX games\n-> {len(self.dao.invalid_iso_files)} invalid (non PSX) '.iso'")
            time.sleep(self.slp_time)

    def print_menu(self):
        self.print_logo()
        print("1 = List All Games")
        print("2 = Rename Games")
        print("3 = Download Covers")
        print("\nq = Quit")

    def input_menu(self):
        qt = False
        options = ('1', '2', '3', '4', '5', 'q', 'Q')
        while not qt:
            choice = input("\n---> ")
            if choice not in options:
                print("Choose a valid option! (1-5)")
            elif choice == '1':
                self.print_all_games()
            else:
                qt = True
        os.system('clear')
        quit()

    def print_all_games(self):
        self.print_logo()
        print(f"Games in {self.dao.main_path}:\n")
        for game in self.dao.games:
            if game.name[:11] == game.get_formatted_id():
                print(game.name[12:])
            else:
                print(game.name)
        print("\n1 = Return to Menu")
        choice = input("\n---> ")
        option = '1'
        if choice == option:
            self.print_menu()
            self.input_menu()


