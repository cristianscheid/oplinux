from dao import Dao
from view import View


def main():
    dao = Dao()
    view = View(dao)
    view.path_input()


if __name__ == "__main__":
    main()
