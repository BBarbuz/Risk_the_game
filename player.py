class Players:
    def __init__(self, __id, __name, __lvl, recruit, ):
        self.__name = __name            # player name
        self.__lvl = __lvl              # player level
        self.__id = __id                # player personal ID
        self.recruit = recruit
        self.alive = alive

    def get_player_name(self):
        return self.__name          # name getter

    def get_player_recruit(self):
        return self.recruit         # recruit getter

    def get_player_level(self):
        return self.__lvl           # level getter

    def get_player_id(self):
        return self.__id           # id getter

    def view_player(self):
        print(f'Kolej: {self.__name} \n\nID:\t{self.__id}')
        print(f'Level:\t{self.__lvl}', '\n')
