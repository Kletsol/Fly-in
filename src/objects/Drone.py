class Drone:
    def __init__(self, id: str):
        self.__id = id

    def get_id(self) -> str:
        return self.__id
