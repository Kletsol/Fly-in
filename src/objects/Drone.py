class Drone:
    def __init__(self, id, position):
        self.__id = id
        self.__position = position

    def get_id(self):
        return self.__id
