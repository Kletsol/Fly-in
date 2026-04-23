class Zone:
    def __init__(self, zone: dict):
        self.type = zone['zone_type']
        self.name = zone['name']
        self.__x_coord = zone['x_coord']
        self.__y_coord = zone['y_coord']
        if 'metadata' in zone.keys():
            self.__metadata = zone['metadata']
            if 'zone_type' in self.__metadata:
                self.__zone_type = self.__metadata['zone_type']

    def get_coords(self):
        return self.__x_coord, self.__y_coord

    def get_visual_coords(self):
        return [self.__x_coord * 180 + 80, self.__y_coord * 180 + 700]

    def get_metadata(self):
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

    def get_cost(self) -> float:
        try:
            if self.__zone_type == 'normal':
                return 1.0
            if self.__zone_type == 'restricted':
                return 2.0
            if self.__zone_type == 'priority':
                return 0.9
            if self.__zone_type == 'blocked':
                return -1
        except Exception:
            return 1.0
