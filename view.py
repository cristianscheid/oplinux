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
        print("by Cristian Scheid\n")
        time.sleep(2)
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

    def print_menu(self):
        self.print_logo()
        print("1 = List all games")
        print("2 = Rename games")
        print("3 = Download covers")
        print("\nq = Quit")

    def input_menu(self):
        qt = False
        options = ('1', '2', '3', '4', '5', 'q', 'Q')
        while not qt:
            choice = input("\n---> ")
            if choice not in options:
                print("Choose a valid option! (1-5)")
            elif choice == '1':
                self.dao.print_all_games()
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu()
                    self.input_menu()
            elif choice == '2':
                self.dao.rename()
                print("\n1 = Return to Menu")
                choice = input("\n---> ")
                option = '1'
                if choice == option:
                    self.print_menu()
                    self.input_menu()
            elif choice == '3':
                self.dao.get_cover()
                self.print_menu()
                self.input_menu()
            else:
                qt = True
        os.system('clear')
        quit()
