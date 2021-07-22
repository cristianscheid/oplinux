import os
import pyfiglet
import time

class View:

    def __init__(self, dao):
        self.dao = dao
        self.slp_time = 3

    def print_logo(self):
        os.system('clear')
        logo = pyfiglet.figlet_format("OPLinux")
        print(logo)

    def path_input(self):
        self.print_logo()
        self.dao.main_path = '~/Documents/PS2/OPL_FOLDER'
        #self.dao.main_path = input("Insert the path of your OPL folder as below:\n\n"
        #                           "'/home/user/MyOPLFolder/' or '~/MyOPLFolder/'\n\n---> ")

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
            print(f"No PS2 game found in '{self.dao.main_path}'\nPlease check the path/folder")
            time.sleep(self.slp_time)
        else:
            print(f"Found:\n{len(self.dao.games)} PS2 game(s)\n{len(self.dao.invalid_isos)} invalid ISO file(s)")
            time.sleep(self.slp_time)
    # Main menu
    def print_menu(self):
        self.print_logo()
        print("1 = List all games")
        print("2 = Rename games")
        print("3 = Download art")
        print("\nq = Quit")
        qt = False
        options = ('1', '2', '3', '4', '5', 'q', 'Q')
        while not qt:
            choice = input("\n---> ")
            if choice not in options:
                print("Choose a valid option! (1-5)")
            # List all games
            elif choice == '1':
                self.dao.print_all_games()
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu()
            # Rename games
            elif choice == '2':
                self.dao.rename()
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu()
            elif choice == '3':
                self.print_menu_art()
            else:
                qt = True
        os.system('clear')
        quit()
    # Art download menu
    def print_menu_art(self):
        print("Choose which arts you want to download:\n")
        print("1 = Front cover")
        print("2 = Back cover")
        print("3 = Spine")
        print("4 = Disc")
        print("5 = Background")
        print("6 = Logo")
        print("7 = Screenshot")
        print("8 = All")
        print("\n9 = Return to main menu")
        options = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        while True:
            choice = input("\n---> ")
            if choice not in options:
                print("Choose a valid option! (1-9)")
            elif choice == '1':
                self.dao.get_art_cover()
            elif choice == '2':
                self.dao.get_art_back_cover()
            elif choice == '3':
                self.dao.get_art_spine()
            elif choice == '4':
                self.dao.get_art_disc()
            elif choice == '5':
                self.dao.get_art_background()
            elif choice == '6':
                self.dao.get_art_logo()
            elif choice == '7':
                self.dao.get_art_screenshot()
            elif choice == '8':
                self.dao.get_art_all()
            elif choice == '9':
                self.print_menu()
