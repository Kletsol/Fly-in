import glob
import heapq
from multiprocessing import Value

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

    def initiate_dict(self, global_state):
        for zone in self.__zones:
            global_state['nodes'].update({(0, zone.name): 0})
        return global_state

    # def process(self):
    #     zones_state: dict[int, dict[str, int]] = {}
    #     links_state: dict[int, dict[str, int]] = {}
    #     for drone in self.__drones:
    #         print("--------------------")
    #         # chercher le chemin le plus court
    #         path = self.dijkstra_space_time(zones_state, links_state)
    #         # path = self.dijkstra(zones_state, links_state)
    #         if path:
    #             print(path)
    #             self.update_states(zones_state, links_state, path)
    #         else:
    #             print(f"[ERROR]: Drone {drone.get_id()} could not find a path")
    #             continue
    #         # print(path)

    def process(self):
        global_state = {
            'nodes': {},  # (zone, t) -> nb_drones
            'edges': {}  # (u, v, t) -> nb_drones
        }
        final_schedules = {}

        # global_state = self.initiate_dict(global_state)
        for drone in self.__drones:
            # 1. Calculer le chemin via Dijkstra Espace-Temps
            path, arrival_time = self.dijkstra_space_time(global_state)
            if path:
                # 2. Mettre à jour les contraintes pour les drones suivants
                self.update_states(path, global_state)
                final_schedules[drone] = path
                for data in final_schedules.items():
                    print(data)
            else:
                print(f"[ERROR]: Drone {drone.get_id()} could not find a path")
        # for drone, path in final_schedules.items():
        #     print(drone)
        #     print(path)
        return final_schedules

    def dijkstra_space_time(self, global_state):
        """
        - start_node: Nom de la zone de départ
        - end_node: Nom de la zone d'arrivée
        - start_time: Temps auquel le drone commence son trajet
        - constraints: Dict ou Set contenant les réservations des drones précédents 
                    ex: {(zone, temps): occupation, (zone_a, zone_b, temps): occupation}
        - graph_data: Dictionnaire contenant les capacités et types de zones
        """

        # Priority Queue: (coût_total, temps_actuel, zone_actuelle, chemin_parcouru)
        queue = [(0, 1, self.start.name, [[0, self.start.name]])]
        visited = set()  # (zone, temps)

        while queue:
            cost, turn, current_zone_name, path = heapq.heappop(queue)

            if current_zone_name == self.end.name:
                return path, turn  # On a trouvé le chemin le plus rapide

            if (current_zone_name, turn) in visited:
                continue
            visited.add((current_zone_name, turn))

            current_zone = self.get_zone(current_zone_name)
            # --- EXPLORATION DES VOISINS (Mouvements + Attente) ---
            # 1. Attendre sur place (toujours possible si capacité respectée)
            next_zones = current_zone.get_next_zones(self.__zones, self.__connections) + [current_zone]

            for next_zone in next_zones:
                # Calcul du temps d'arrivée selon le type de zone
                travel_time = next_zone.get_cost()
                arrival_time = turn + travel_time

                # Vérification des contraintes de capacité
                if self.is_available_zone(next_zone, arrival_time, global_state):
                    new_cost = cost + travel_time
                    heapq.heappush(queue, (new_cost, arrival_time, next_zone.name, path + [[new_cost, next_zone.name]]))

                if self.is_available_zone(next_zone, arrival_time, global_state):
                    new_cost = cost + travel_time
                    heapq.heappush(queue, (new_cost, arrival_time, next_zone.name, path + [[new_cost, next_zone.name]]))

        return None, None

    @staticmethod
    def get_total_cost(path: list):
        total = 0
        for zone in path:
            total += zone.get_cost()
        return total

    def is_available_zone(self, zone, turn, global_state) -> bool:
        current_occupancy = global_state['nodes'].get((zone.name, turn), 0)
        if current_occupancy >= zone.get_capacity():
            return False
        return True

    def is_available_link(self, zone_1, zone_2, turn, global_state) -> bool:
        for link in self.__connections:
            if zone_1.name in link.get_linked_zones() and zone_2.name in link.get_linked_zones():
                connection = link
        current_occupancy = global_state['edges'].get((zone_1.name, zone_2.name, turn), 0)
        if current_occupancy >= connection.get_capacity():
            return False
        return True

    def get_zone(self, name):
        for zone in self.__zones:
            if zone.name == name:
                return (zone)

    def update_states(self, path, global_state):
        for i in range(len(path)):
            arrival_time, zone_name = path[i]
            if i + 1 < len(path):
                departure_time = path[i + 1][0]
                for t in range(int(arrival_time), int(departure_time) + 1):
                    node_key = (zone_name, t)
                    global_state['nodes'][node_key] = global_state['nodes'].get(node_key, 0) + 1
            else:
                node_key = (zone_name, arrival_time)
                global_state['nodes'][node_key] = global_state['nodes'].get(node_key, 0) + 1
            if i > 0:
                prev_time, prev_zone_name = path[i - 1]
                edge_key = (prev_zone_name, zone_name, prev_time)
                global_state['edges'][edge_key] = global_state['edges'].get(edge_key, 0) + 1
        # print(global_state)

    # def get_path(self, start_name: str, end_state: tuple[str, int], previous: dict[tuple[str, int], tuple[str, int]]) -> dict[int, str]:
    #     """Reconstruct the full turn-to-position path by back-tracking.

    #     Handles both single-turn moves and two-turn restricted-zone
    #     transitions by inserting an intermediate ``'hub1-hub2'`` entry.

    #     Args:
    #         start_name (str): Name of the start node (backtracking stops
    #             here).
    #         end_state (tuple[str, int]): ``(node_name, turn)`` of the goal
    #             state.
    #         previous (dict): Predecessor map built during the search.

    #     Returns:
    #         dict[int, str]: Complete path from turn 0 to the goal.
    #     """

    #     path: dict[int, str] = {}

    #     curr_name, curr_turn = end_state
    #     while curr_name != start_name:
    #         path[curr_turn] = curr_name
    #         prev_name, prev_turn = previous[(curr_name, curr_turn)]
    #         if curr_turn - prev_turn == 2:
    #             path[curr_turn - 1] = f"{prev_name}-{curr_name}"
    #         else:
    #             while curr_turn - prev_turn != 1:
    #                 curr_turn -= 1
    #                 path[curr_turn] = curr_name
    #         curr_name, curr_turn = prev_name, prev_turn

    #     while curr_turn > 0:
    #         path[curr_turn] = curr_name
    #         curr_turn -= 1
    #     path[0] = start_name
    #     return {k: path[k] for k in sorted(path)}

        # for turn, zone in path.items():
        #     turn_state = zones_state.setdefault(turn, {})
        #     turn_state[zone] = turn_state.get(zone, 0) + 1
        #     if turn > 0 and "-" in zone:
        #         link_occ = links_state.setdefault(turn, {})
        #         link_occ[zone] = link_occ.get(zone, 0) + 1
        #     elif turn > 0 and "-" not in zone:
        #         prev_name = path.get(turn - 1, "")
        #         if (
        #             prev_name
        #             and prev_name != zone
        #             and "-" not in prev_name
        #         ):
        #             link_occ = links_state.setdefault(turn, {})
        #             lk = f"{prev_name}-{zone}"
        #             link_occ[lk] = link_occ.get(lk, 0) + 1


    # def dijkstra(self, zones_state, links_state) -> tuple:
        #     path: dict[tuple[str, int], float] = {}
        #     previous: dict[tuple[str, int], tuple[str, int]] = {}
        #     queue = [(0, 0, self.start.name)]
        #     visited = set()

        #     while queue:
        #         cost, turn, current_zone_name = heapq.heappop(queue)

        #         if (current_zone_name, turn) in path:
        #             if cost > path[(current_zone_name, turn)]:
        #                 continue

        #         current_zone = self.get_zone(current_zone_name)
        #         if current_zone == self.end:
        #             return self.get_path(self.start.name, (current_zone.name, turn), previous)

        #         if turn > self.max_time:
        #             continue

        #         if (current_zone, turn) in visited:
        #             continue

        #         for next_zone in current_zone.get_next_zones(self.__zones, self.__connections):
        #             if (next_zone == current_zone or next_zone in visited):
        #                 continue
        #             move_cost = next_zone.get_cost()
        #             arrival_time = turn + move_cost
        #             if not self.is_available_zone(next_zone, arrival_time, zones_state):
        #                 continue
        #             if not self.is_available_link(current_zone, next_zone, turn, links_state):
        #                 continue
        #             new_cost = cost + move_cost
        #             if new_cost < path.get((next_zone.name, arrival_time), float('inf')):
        #                 path[(next_zone.name, arrival_time)] = new_cost
        #                 previous[(next_zone.name, arrival_time)] = (current_zone.name, turn)
        #                 heapq.heappush(queue, (new_cost, arrival_time, next_zone.name))
        #                 visited.add((current_zone, turn))

        #         wait_time = turn + 1
        #         if self.is_available_zone(current_zone, wait_time, zones_state):
        #             new_cost = cost + 1
        #             if new_cost < path.get((current_zone.name, wait_time), float('inf')):
        #                 path[(current_zone.name, wait_time)] = new_cost
        #                 previous[(current_zone.name, wait_time)] = (current_zone.name, turn)
        #                 heapq.heappush(queue, (new_cost, wait_time, current_zone.name))

        #     return {}