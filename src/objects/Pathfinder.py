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

    def process(self):
        zones_state: dict[int, dict[str, int]] = {}
        links_state: dict[int, dict[str, int]] = {}
        for drone in self.__drones:
            print("--------------------")
            # chercher le chemin le plus court
            path = self.dijkstra(zones_state, links_state)

    def dijkstra(self, zones_state, links_state) -> tuple:
        path: dict[tuple[str, int], float] = {}
        previous: dict[tuple[str, int], tuple[str, int]] = {}
        queue = [(0, 0, self.start.name)]
        visited = set()

        while queue:
            cost, turn, current_zone_name = heapq.heappop(queue)

            if (current_zone_name, turn) in path:
                print("1")
                if cost > path[(current_zone_name, turn)]:
                    print("2")
                    continue

            current_zone = self.get_zone(current_zone_name)
            print(f"-> {current_zone_name}")
            if current_zone == self.end:
                print(path)
                print("\n-------------------------\n")
                print(previous)
                new_path = self.get_path(self.start.name, (current_zone.name, turn), previous)
                return {k: new_path[k] for k in sorted(new_path)}

            if turn > self.max_time:
                print("3")
                continue

            if (current_zone, turn) in visited:
                print("4")
                continue

            for next_zone in current_zone.get_next_zones(self.__zones, self.__connections):
                print("5")
                if (next_zone == current_zone or next_zone in visited):
                    print("6")
                    continue
                move_cost = next_zone.get_cost()
                arrival_time = turn + move_cost
                if not self.is_available_zone(next_zone, arrival_time, zones_state):
                    print("7")
                    continue
                if not self.is_available_link(current_zone, next_zone, turn, links_state):
                    print("8")
                    continue
                new_cost = cost + move_cost
                if new_cost < path.get((next_zone.name, arrival_time), float('inf')):
                    print("9")
                    path[(next_zone.name, arrival_time)] = new_cost
                    previous[(next_zone.name, arrival_time)] = (current_zone.name, turn)
                    heapq.heappush(queue, (new_cost, arrival_time, next_zone.name))
                    visited.add((current_zone, turn))

            wait_t = turn + 1
            if self.is_available_zone(current_zone, wait_t, zones_state):
                new_cost = cost + 1
                if new_cost < path.get((current_zone.name, wait_t), float('inf')):
                    path[(current_zone.name, wait_t)] = new_cost
                    previous[(current_zone.name, wait_t)] = (current_zone.name, turn)
                    heapq.heappush(queue, (new_cost, wait_t, current_zone.name))

        return {}

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
    
    def is_available_link(self, zone_1, zone_2, turn, reservation) -> bool:
        for link in self.__connections:
            if zone_1 in link.get_linked_zones() and zone_2 in link.get_linked_zones():
                capacity = link.get_capacity()
        return True

    def get_zone(self, name):
        for zone in self.__zones:
            if zone.name == name:
                return (zone)

    def get_path(self, start_name: str, end_state: tuple[str, int], previous: dict[tuple[str, int], tuple[str, int]]) -> dict[int, str]:
        """Reconstruct the full turn-to-position path by back-tracking.

        Handles both single-turn moves and two-turn restricted-zone
        transitions by inserting an intermediate ``'hub1-hub2'`` entry.

        Args:
            start_name (str): Name of the start node (backtracking stops
                here).
            end_state (tuple[str, int]): ``(node_name, turn)`` of the goal
                state.
            previous (dict): Predecessor map built during the search.

        Returns:
            dict[int, str]: Complete path from turn 0 to the goal.
        """

        path: dict[int, str] = {}

        curr_name, curr_turn = end_state
        while curr_name != start_name:
            print(curr_name)
            path[curr_turn] = curr_name
            prev_name, prev_turn = previous[(curr_name, curr_turn)]
            if curr_turn - prev_turn == 2:
                path[curr_turn - 1] = f"{prev_name}-{curr_name}"
            else:
                while curr_turn - prev_turn != 1:
                    curr_turn -= 1
                    path[curr_turn] = curr_name
            curr_name, curr_turn = prev_name, prev_turn

        while curr_turn > 0:
            path[curr_turn] = curr_name
            curr_turn -= 1
        path[0] = start_name
        return path
