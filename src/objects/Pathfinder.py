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
            print("--------------------")
            # chercher le chemin le plus court
            path = self.dijkstra(reservation_table)

    def dijkstra(self, reservations) -> tuple:
        queue = [(0, 0, self.start.name, [self.start.name])]
        visited = set()

        while queue:
            cost, turn, current_zone_name, path = heapq.heappop(queue)
            current_zone = self.get_zone(current_zone_name)
            print(f"-> {current_zone_name}")
            if current_zone == self.end:
                print(path)
                return path

            if (current_zone, turn) in visited:
                continue
            visited.add((current_zone, turn))

            for next_zone in current_zone.get_next_zones(self.__zones, self.__connections):
                if (next_zone == current_zone or next_zone in visited):
                    continue
                move_cost = next_zone.get_cost()
                arrival_time = turn + move_cost
                if self.is_available_zone(next_zone, arrival_time, reservations):
                    new_cost = cost + move_cost
                    new_path = path + [next_zone.name]
                    heapq.heappush(queue, (new_cost, arrival_time, next_zone.name, new_path))

        return None, None

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
