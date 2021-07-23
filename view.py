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

    # Get path from user
    def path_input(self):
        while True:
            self.print_logo()
            # self.dao.main_path = '~/Documents/PS2/OPL_FOLDER'
            self.dao.main_path = input("Insert the path of your OPL folder as below:\n\n"
                                       "'/home/user/MyOPLFolder/' or '~/MyOPLFolder/'\n\n---> ")
            if self.dao.path_exists():
                self.dao.search_iso()
                if len(self.dao.games) > 0:
                    print(f"\nFound {len(self.dao.games)} PS2 game(s)")
                    print(f"{len(self.dao.invalid_isos)} invalid ISO file(s)")
                    time.sleep(self.slp_time)
                    self.print_menu()
                else:
                    print(f"\nNo PS2 game found in '{self.dao.main_path}'\nPlease check the path/folder")
                    time.sleep(self.slp_time)
            else:
                print("\nInvalid path(doesn't exist)!")
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
                self.print_logo()
                self.dao.search_iso()
                self.dao.print_all_games()
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu()
            # Rename games
            elif choice == '2':
                self.print_logo()
                print("\nRenaming games...")
                self.dao.search_iso()
                self.dao.rename()
                self.print_logo()
                print("\nRenaming games -- Ok")
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu()
            elif choice == '3':
                self.print_logo()
                self.print_menu_art()
            else:
                qt = True
        os.system('clear')
        quit()

    # Art download menu
    def print_menu_art(self):
        self.print_logo()
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
            self.dao.search_iso()
            if choice not in options:
                print("Choose a valid option! (1-9)")
            elif choice == '1':
                self.print_logo()
                self.dao.get_art_cover()
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '2':
                self.print_logo()
                self.dao.get_art_back_cover()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '3':
                self.print_logo()
                self.dao.get_art_spine()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '4':
                self.print_logo()
                self.dao.get_art_disc()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '5':
                self.print_logo()
                self.dao.get_art_background()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '6':
                self.print_logo()
                self.dao.get_art_logo()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '7':
                self.print_logo()
                self.dao.get_art_screenshot()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '8':
                self.print_logo()
                self.dao.get_art_all()
                print("\n1 = Return to Art Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu_art()
            elif choice == '9':
                self.print_menu()
