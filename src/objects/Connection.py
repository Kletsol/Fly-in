from typing import Any


class Connection:
    def __init__(self, connection: dict[str, Any]):
        self.__zones = connection['linked_zones']
        if 'metadata' in connection.keys():
            self.__metadata = connection['metadata']

    def get_linked_zones(self) -> Any:
        return self.__zones

    def get_metadata(self) -> Any:
        return self.__metadata

    def get_capacity(self) -> int:
        if self.__metadata:
            if 'max_link_capacity' in self.get_metadata():
                return int(self.get_metadata()['max_link_capacity'])
        return 1
