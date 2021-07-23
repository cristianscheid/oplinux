class Game:

    def __init__(self, id_opl, file, name, region):
        self.id_opl = id_opl
        self.file = file
        self.id_formatted = (id_opl.replace('_', '-').replace('.', ''))
        self.name = name
        self.region = region
