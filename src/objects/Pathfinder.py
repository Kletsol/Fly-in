class PathFinder:
    def __init__(self, start, end, zones, connections, drones):
        self.start = start
        self.end = end
        self.__zones = zones
        self.__connections = connections
        self.__drones = drones

    def initiate_drones(self):
        for drone in self.__drones:
            drone.set_position(self.start.name)
            print(drone.get_position())

    def initiate_dict(self, turn):
        output = {}
        positions = {}
        for drone in self.__drones:
            positions.update({drone.get_id(): drone.get_position()})
        output.update({f"Turn {turn}": positions})
        print(output)

    def djikstra(self):
        turn_counter = 0
        self.initiate_drones()
        self.initiate_dict(turn_counter)
        return
