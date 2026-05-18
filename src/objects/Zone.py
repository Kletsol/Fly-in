from typing import Any


class Zone:
    """A class instantiated for each zone, with useful methods"""
    def __init__(self, zone: dict[Any, Any]):
        """Initiates the class with the information we got from parsing

        Args:
            zone (dict[Any, Any]): The parsed informations from the input file
        """
        self.type = zone['zone_type']
        self.name = zone['name']
        self.__x_coord = zone['x_coord']
        self.__y_coord = zone['y_coord']
        self.zone_type = None
        self.__metadata = zone['metadata']
        if self.__metadata is not None:
            if 'zone' in self.__metadata:
                self.zone_type = self.__metadata['zone']

    def get_coords(self) -> tuple[int, int]:
        """A getter for the coordinates of the zone

        Returns:
            tuple[int, int]: Coordinates x and y
        """
        return self.__x_coord, self.__y_coord

    def get_visual_coords(self) -> list[int]:
        """A getter for the coordinates of the zone, adapted to be
        usable in visualization

        Returns:
            list[int]: The coordinates adapted for visualization
        """
        return [self.__x_coord * 180 + 80, self.__y_coord * 180 + 700]

    def get_metadata(self) -> dict[Any, Any] | Any:
        """A getter for the zone's metadata

        Returns:
            dict[Any, Any] | Any: The zone's metadata
        """
        return self.__metadata

    def get_color(self) -> str | Any:
        """A getter for the color of the zone

        Returns:
            str | Any: The color of the zone
        """
        if self.__metadata is not None:
            if 'color' in self.__metadata.keys():
                return self.__metadata['color']
        return 'white'

    def get_rgb(self) -> tuple[int, int, int]:
        """A getter that converts color into usable RGB data

        Returns:
            tuple[int, int, int]: A tuple with three RGB values
        """
        match self.get_color():

            case 'white':
                return (255, 255, 255)
            case 'blue':
                return (51, 153, 255)
            case 'cyan':
                return (0, 255, 255)
            case 'green':
                return (0, 204, 0)
            case 'red':
                return (204, 0, 0)
            case 'darkred':
                return (153, 0, 0)
            case 'orange':
                return (255, 128, 0)
            case 'purple':
                return (153, 51, 255)
            case 'violet':
                return (102, 0, 204)
            case 'pink':
                return (255, 0, 255)
            case 'yellow':
                return (255, 255, 51)
            case 'gold':
                return (255, 215, 0)
            case 'grey':
                return (160, 160, 160)
            case 'brown':
                return (102, 51, 0)
            case 'maroon':
                return (139, 69, 19)
            case 'black':
                return (64, 64, 64)
            case 'teal':
                return (0, 153, 153)
            case 'crimson':
                return (255, 0, 0)
            case _:
                return (255, 255, 255)

    def get_next_zones(self, zones: list[Any], connections: list[Any]) -> \
            list[Any]:
        """From a given zone, returns all neiboring zones

        _extended_summary_

        Returns:
            list[Any]: A list of zones 'adjacent' to the current zone
        """
        next_zones = []
        for connection in connections:
            if connection.get_linked_zones()[0] == self.name:
                for zone in zones:
                    if connection.get_linked_zones()[1] == zone.name:
                        next_zones.append(zone)
            elif connection.get_linked_zones()[1] == self.name:
                for zone in zones:
                    if connection.get_linked_zones()[0] == zone.name:
                        next_zones.append(zone)
        return next_zones

    def get_cost(self) -> float:
        """A method to get the cost of a movement toward a zone,
        depending on the type of that zone

        Returns:
            float: The cost of the movement, in turns
        """
        if self.zone_type is None:
            cost = 1.0
        else:
            if self.zone_type == 'normal':
                cost = 1.0
            if self.zone_type == 'restricted':
                cost = 2.0
            if self.zone_type == 'priority':
                cost = 1.0
            if self.zone_type == 'blocked':
                cost = float('inf')
        return cost

    def get_priority_benefit(self) -> bool:
        """A method that checks whether the zone is a priority or not"""
        if self.zone_type == 'priority':
            return True
        return False

    def get_capacity(self) -> int | Any:
        """A getter for the capacity of the zone

        Returns:
            int | Any: A certain value if specified in the metadata, else 1
        """
        if self.__metadata is not None:
            if 'max_drones' in self.get_metadata().keys():
                return self.get_metadata()['max_drones']
        return 1
