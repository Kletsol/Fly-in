from abc import ABC


class Connection(ABC):
    def __init__(self, connection: dict):
        self.__zones = connection['linked_zones']
        if 'metadata' in connection.keys():
            self.__metadata = connection['metadata']

    def get_linked_zones(self):
        return self.__zones

    def get_metadata(self):
        return self.__metadata
