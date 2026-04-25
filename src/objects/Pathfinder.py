import heapq

class PathFinder:
    def __init__(self, start, end, zones, connections, drones):
        self.start = start
        self.end = end
        self.__zones = zones
        self.__connections = connections
        self.__drones = drones
        self.output = {}
        self.max_time = 200

    def initiate_drones(self):
        for drone in self.__drones:
            drone.set_position(self.start.name)

    def initiate_dict(self, turn):
        positions = {}
        for drone in self.__drones:
            positions.update({drone.get_id(): drone.get_position()})
        self.output.update({f"Turn {turn}": positions})
        print(self.output)

    # def initiate_reservations(self):
    #     reservation_table = {(self.start, 0): len(self.__drones)}
    #     for zone in self.__zones:
    #         reservation_table.update()

    def process(self):
        reservation_table = {(self.start, 0): len(self.__drones)}
        for drone in self.__drones:
            # chercher le chemin le plus court
            path, turn = self.dijkstra(reservation_table)
            if path:
                for zone in path:
                    reservation_table[turn][zone] += 1

    # def dijkstra(self):
    #     queue = [(0, self.start)]
    #     visited = set()

    #     while queue:
    #         turn, zone = heapq.heappop(queue)

    #         if zone == self.end:
    #             return path

    #         if turn >= self.max_time or (zone, turn) in visited:
    #             continue
    #         visited.add((zone, turn))

    #         if self.is_available_zone(zone, turn + 1):
    #             heapq.heappush(queue, (turn + 1, zone))

    #         for next_zone in zone.get_next_zones():
    #             travel_time = next_zone.get_cost()
    #             arrival_time = turn + travel_time

    #             if self.is_available_zone(next_zone, arrival_time):
    #                 heapq.heappush(queue, (arrival_time, next_zone))

    def dijkstra(self, reservations) -> tuple:
        queue = [(0, 0, self.start.name, [self.start])]
        visited = set()

        while queue:
            print("\n------------------\n")
            cost, turn, current_zone_name, path = heapq.heappop(queue)
            print(type(current_zone_name))
            current_zone = self.get_zone(current_zone_name)
            print(current_zone.name)
            print("1")
            if current_zone == self.end:
                print("2")
                return path, cost

            if (current_zone, turn) in visited:
                print("3")
                continue
            visited.add((current_zone, turn))

            print("4")
            for next_zone in current_zone.get_next_zones(self.__zones, self.__connections):
                print(f"Next -> {next_zone.name}")
                print("5")
                move_cost = next_zone.get_cost()
                arrival_time = turn + move_cost
                if self.is_available_zone(next_zone, arrival_time, reservations):
                    print("6")
                    new_cost = cost + move_cost
                    print(new_cost)
                    new_path = path + [next_zone]
                    heapq.heappush(queue, (new_cost, arrival_time, next_zone.name, new_path))

            # if self.is_available_zone(current_zone, turn, turn + 1, reservations):
            #     heapq.heappush(queue, (cost + 1, turn + 1, current_zone, path + [current_zone]))

        return None, None

        # turn_counter = 0
        # current_zone = self.start
        # previous_zone = self.start
        # current_path = []
        # while current_zone != self.end:
        #     print(f"Current -> {current_zone.name}")

        #     # Recuperer les zones voisines
        #     next_zones = current_zone.get_next_zones(self.__zones, self.__connections, previous_zone)

        #     # Trouver laquelle a le cout le plus petit
        #     costs = sorted(next_zones, key=lambda x: x.get_cost())

        #     # L'ajouter au chemin actuellement traite
        #     current_path.append(costs[0])
        #     for zone in current_path:
        #         print(zone.name)

        #     previous_zone = current_zone
        #     current_zone = costs[0]
        #     total = self.get_total_cost(current_path)
        #     print(total)
        #     print("\n----------------------\n")
        # print(turn_counter)
        # return

    @staticmethod
    def get_total_cost(path: list):
        total = 0
        for zone in path:
            total += zone.get_cost()
        return total

    def is_available_zone(self, zone, turn, reservations) -> bool:
        if zone not in reservations.keys():
            return True
        for key in reservations.keys():
            print(zone.name)
            if key[0].name == zone.name:
                if key[1] <= zone.get_capacity():
                    return True
        return False

    def get_zone(self, name):
        for zone in self.__zones:
            if zone.name == name:
                return (zone)
