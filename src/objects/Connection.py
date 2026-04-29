from abc import ABC


class Connection(ABC):
    def __init__(self, connection: dict):
        self.__zones = connection['linked_zones']
        if 'metadata' in connection.keys():
            self.__metadata = connection['metadata']

    def get_linked_zones(self) -> list[str]:
        return self.__zones

    def get_metadata(self):
        return self.__metadata

    def get_capacity(self):
        if self.__metadata:
            if 'max_link_capacity' in self.get_metadata():
                return self.get_metadata()['max_link_capacity']
        return 1
