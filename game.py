class Game:

    def __init__(self, id_opl, name, path, region):
        self.id_opl = id_opl
        self.id_formatted = (id_opl.replace('_', '-').replace('.', ''))
        self.name = name
        self.path = path
        self.region = region
