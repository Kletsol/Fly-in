class Zone:
    def __init__(self, zone: dict):
        self.type = zone['zone_type']
        self.name = zone['name']
        self.__x_coord = zone['x_coord']
        self.__y_coord = zone['y_coord']
        if 'metadata' in zone.keys():
            self.__metadata = zone['metadata']

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
