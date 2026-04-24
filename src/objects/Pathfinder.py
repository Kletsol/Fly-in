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
        paths = {}
        while current_zone != self.end:
            print(f"Current -> {current_zone.name}")

            # Recuperer les zones voisines
            next_zones = current_zone.get_next_zones(self.__zones, self.__connections, previous_zone)

            # Trouver laquelle a le cout le plus petit
            costs = sorted(next_zones, key=lambda x: x.get_cost(), reverse=True)
            for zone in costs:
                print(f"{zone.name}", end=' ')
                    # print(f"Next -> {zone.name}")
                    # print(cost)
            print(f"\nPrevious -> {previous_zone.name}")
            previous_zone = current_zone
            current_zone = zone
            print("\n----------------------\n")
        print(turn_counter)
        return
    
    def update_paths(self, paths):
        pass
