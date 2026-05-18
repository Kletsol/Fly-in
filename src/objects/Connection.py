from typing import Any


class Connection:
    """A class instantiated for each connection, with useful methods"""
    def __init__(self, connection: dict[str, Any]):
        self.__zones = connection['linked_zones']
        if 'metadata' in connection.keys():
            self.__metadata = connection['metadata']

    def get_linked_zones(self) -> Any:
        """A getter for the linked zones of the connection
        Returns: Any: The list containing the two linked zones
        """
        return self.__zones

    def get_metadata(self) -> Any:
        """A getter for the metadata of the connection
        Returns: Any: The connection's metadata
        """
        return self.__metadata

    def get_capacity(self) -> int:
        """Gets the capacity of the connection, depending on its presence
        in the metadata, and returns it as an int
        Returns:
            int: The capacity of the connection
        """
        if self.__metadata:
            if 'max_link_capacity' in self.get_metadata():
                return int(self.get_metadata()['max_link_capacity'])
        return 1
