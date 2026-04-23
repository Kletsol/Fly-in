class Drone:
    def __init__(self, id, position):
        self.__id = id
        self.__position = position

    def get_id(self):
        return self.__id

    def get_position(self):
        return self.__position
    
    def set_position(self, position) -> None:
        self.__position = position
        return None
