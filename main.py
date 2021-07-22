from dao import Dao
from view import View

def main():
    dao = Dao()
    view = View(dao)
    while len(dao.games) < 1:
        view.path_input()
        if view.path_exists():
            dao.search_iso()
            view.how_many_games()
    view.print_menu()

if __name__ == "__main__":
    main()