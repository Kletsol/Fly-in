import heapq
from src import Zone, Connection, Drone
from typing import Any


class PathFinder:
    def __init__(self, start: Zone, end: Zone, zones: list[Zone],
                 connections: list[Connection], drones: list[Drone]) -> None:
        self.start = start
        self.end = end
        self.__zones = zones
        self.__connections = connections
        self.__drones = drones
        self.max_time = 2000

    def process(self) -> dict[str, list[list[Any]]]:
        global_state: dict[str, dict[tuple[str, float], int]] = \
            {'nodes': {}, 'edges': {}}
        final_schedule = {}

        for drone in self.__drones:
            path, arrival_time = self.dijkstra_space_time(global_state)
            if path:
                self.update_states(path, global_state)
                final_schedule[drone.get_id()] = path
            else:
                raise Exception(f"\033[0;31m[ERROR]: Drone {drone.get_id()}"
                                " could not find a path\033[0;0m")
        return final_schedule

    def dijkstra_space_time(self, global_state: dict[str, dict[
            tuple[str, float], int]]
    ) -> tuple[list[list[Any]], float] | tuple[None, None]:
        queue = [(0.0, 0, 0.0, self.start.name, [[0, self.start.name]])]
        visited: dict[tuple[Any, float], tuple[float, int]] = {}

        while queue:
            cost, penalty, turn, curr_zone_name, path = heapq.heappop(queue)

            if turn > self.max_time:
                continue

            if curr_zone_name == self.end.name:
                return path, turn  # On a trouvé le chemin le plus rapide

            key = (curr_zone_name, turn)
            if key in visited:
                if visited[key] <= (cost, penalty):
                    continue
            visited[key] = (cost, penalty)

            current_zone: Zone = self.get_zone(curr_zone_name)
            # --- EXPLORATION DES VOISINS (Mouvements + Attente) ---
            # 1. Attendre sur place (toujours possible si capacité respectée)
            next_zones = current_zone.get_next_zones(self.__zones,
                                                     self.__connections)

            wait_turn = turn + 1
            if self.is_available_zone(current_zone, wait_turn, global_state):
                new_cost = cost + 1
                new_penalty = penalty + current_zone.get_priority_penalty()
                heapq.heappush(queue, (new_cost, new_penalty, wait_turn,
                                       curr_zone_name, path +
                                       [[wait_turn, curr_zone_name]]))

            for next_zone in next_zones:
                # Arrival_time calculation
                travel_time = next_zone.get_cost()
                arrival_time = turn + travel_time

                if not self.is_available_link_full(current_zone, next_zone,
                                                   int(turn),
                                                   int(arrival_time),
                                                   global_state):
                    continue

                if not self.is_available_zone(next_zone, arrival_time,
                                              global_state):
                    continue

                new_cost = cost + travel_time
                new_penalty = penalty + next_zone.get_priority_penalty()

                heapq.heappush(queue,
                               (new_cost, new_penalty, arrival_time,
                                next_zone.name, path +
                                ([[turn + 1, self.get_connection(
                                    curr_zone_name, next_zone.name, True)],
                                    [arrival_time, next_zone.name]] if
                                    arrival_time == turn + 2 else
                                    [[arrival_time, next_zone.name]])))

        return None, None

    def is_available_zone(self, zone: Zone, turn: float,
                          global_state: dict[str, dict[tuple[str, float], int]]
                          ) -> bool:
        current_occupancy = global_state['nodes'].get((zone.name, turn), 0)
        capacity = zone.get_capacity()
        if zone.type in ['start_hub', 'end_hub']:
            capacity = len(self.__drones)
        if current_occupancy < capacity:
            return True
        return False

    def get_connection(self, prev_zone: str, next_zone: str,
                       return_name: bool) -> Any:
        zones = ''
        for connection in self.__connections:
            zones_list = connection.get_linked_zones()
            if prev_zone in zones_list and next_zone in zones_list:
                zones = f"{zones_list[0]}-{zones_list[1]}"
                if return_name is True:
                    return zones
                else:
                    return connection

    def is_available_link_full(self, zone_1: Zone, zone_2: Zone,
                               start_time: int, end_time: int,
                               global_state: dict[str, dict[tuple[str, float],
                                                            int]]) -> bool:

        # Trouver la connexion
        connection: Connection = self.get_connection(zone_1.name, zone_2.name,
                                                     False)

        if connection is None:
            return False

        # Vérifier chaque tour du déplacement
        for t in range(start_time, end_time):
            edge_key = tuple(sorted([zone_1.name, zone_2.name])) + (t,)
            if global_state['edges'].get(edge_key, 0) >= \
                    connection.get_capacity():
                return False
        return True

    def update_states(self, path: list[list[Any]],
                      global_state: dict[str, dict[tuple[str, float], int]]
                      ) -> None:

        for i in range(len(path) - 1):
            time_a, zone_a = path[i]
            time_b, zone_b = path[i + 1] if '-' not in path[i + 1][1] else \
                path[i + 2]

            # 1. Zone de départ : occupée uniquement au temps de départ
            global_state['nodes'][(zone_a, time_a)] = \
                global_state['nodes'].get((zone_a, time_a), 0) + 1

            # 2. Lien : occupé pendant tout le déplacement
            for t in range(int(time_a), int(time_b)):
                edge_key = tuple(sorted([zone_a, zone_b])) + (t,)
                global_state['edges'][edge_key] = \
                    global_state['edges'].get(edge_key, 0) + 1

        # Dernière zone à l'arrivée
        last_time, last_zone = path[-1]
        key = (last_zone, last_time)
        global_state['nodes'][key] = global_state['nodes'].get(key, 0) + 1

    def get_zone(self, name: str) -> Any:
        for zone in self.__zones:
            if zone.name == name:
                return zone
