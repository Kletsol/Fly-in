class Dijkstra:
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

    def process(self):
        turn_counter = 0
        current_zone = self.start
        previous_zone = self.start
        while current_zone != self.end:
            print(f"Current -> {current_zone.name}")
            next_zones = current_zone.get_next_zones(self.__zones, self.__connections)
            for zone in next_zones:
                print(f"Next -> {zone.name}")
                print(zone.get_cost())
            print(f"Previous -> {previous_zone.name}")
            previous_zone = current_zone
            current_zone = zone
            print("\n----------------------\n")
        print(turn_counter)
        return
