class Game:

    def __init__(self, id, name, path):
        self.id = id
        self.name = name[:len(name) - 4]
        self.path = path

    def get_formatted_id(self):
        formatted_id = f"{self.id[0]}_{self.id[1]}.{self.id[2]}"
        return formatted_id

    def get_formatted_id_url(self):
        formatted_id_url = f"{self.id[0]}-{self.id[1]}{self.id[2]}"
        return formatted_id_url