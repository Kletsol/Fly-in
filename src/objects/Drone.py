class Drone:
    """A class instantiated for each drone, with useful methods"""
    def __init__(self, id: str):
        self.__id = id

    def get_id(self) -> str:
        """A getter for the id of the drone
        Returns: str: The id of the drone
        """
        return self.__id
