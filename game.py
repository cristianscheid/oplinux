class Game:

    def __init__(self, id, name, path, region):
        self.id = id
        self.name = name
        self.path = path
        self.region = region

    def get_formatted_id_opl(self):
        return f"{self.id[0]}_{self.id[1]}.{self.id[2]}"

    def get_formatted_id(self):
        return f"{self.id[0]}-{self.id[1]}{self.id[2]}"
