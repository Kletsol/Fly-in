class PathFinder:
    def __init__(self, start, end, zones, connections, drones):
        self.start = start
        self.end = end
        self.__zones = zones
        self.__connections = connections
        self.__drones = drones
        self.output = {}

    def initiate_drones(self):
        for drone in self.__drones:
            drone.set_position(self.start.name)

    def initiate_dict(self, turn):
        positions = {}
        for drone in self.__drones:
            positions.update({drone.get_id(): drone.get_position()})
        self.output.update({f"Turn {turn}": positions})
        print(self.output)

    def dijkstra(self):
        turn_counter = 0
        print(turn_counter)
        return
