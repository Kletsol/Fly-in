class Zone:
    def __init__(self, zone: dict):
        self.type = zone['zone_type']
        self.name = zone['name']
        self.__x_coord = zone['x_coord']
        self.__y_coord = zone['y_coord']
        self.zone_type = None
        if 'metadata' in zone.keys():
            self.__metadata = zone['metadata']
            if 'zone' in self.__metadata:
                self.zone_type = self.__metadata['zone']

    def get_coords(self):
        return self.__x_coord, self.__y_coord

    def get_visual_coords(self):
        return [self.__x_coord * 180 + 80, self.__y_coord * 180 + 700]

    def get_metadata(self) -> dict:
        return self.__metadata

    def get_color(self) -> str:
        if 'color' in self.__metadata.keys():
            return self.__metadata['color']
        else:
            return 'white'

    def get_rgb(self) -> tuple:
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
            case 'orange':
                return (255, 128, 0)
            case 'purple':
                return (153, 51, 255)
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
            case 'black':
                return (64, 64, 64)
            case 'teal':
                return (0, 153, 153)
            case _:
                return (255, 255, 255)

    def get_next_zones(self, zones, connections) -> list:
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

    def get_cost(self) -> int:
        if self.zone_type is None:
            cost = 1
        else:
            if self.zone_type == 'normal':
                cost = 1
            if self.zone_type == 'restricted':
                cost = 2
            if self.zone_type == 'priority':
                cost = 1
            if self.zone_type == 'blocked':
                cost = -1
        return cost

    def get_capacity(self) -> int:
        if 'max_drones' in self.get_metadata().keys():
            return self.get_metadata()['max_drones']
        else:
            return 1
