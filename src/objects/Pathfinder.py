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

    def process(self):
        global_state = {'nodes': {}, 'edges': {}}
        final_schedule = {}

        for drone in self.__drones:
            path, arrival_time = self.dijkstra_space_time(global_state)
            if path:
                self.update_states(path, global_state)
                final_schedule[drone.get_id()] = path
            else:
                print(f"\033[0;31m[ERROR]: Drone {drone.get_id()} could not find a path\033[0;0m")
        print(arrival_time)
        return final_schedule

    # def dijkstra_space_time(self, global_state):
    #     """
    #     - start_node: Nom de la zone de départ
    #     - end_node: Nom de la zone d'arrivée
    #     - start_time: Temps auquel le drone commence son trajet
    #     - constraints: Dict ou Set contenant les réservations des drones précédents 
    #                 ex: {(zone, temps): occupation, (zone_a, zone_b, temps): occupation}
    #     - graph_data: Dictionnaire contenant les capacités et types de zones
    #     """

    #     # Priority Queue: (coût_total, temps_actuel, zone_actuelle, chemin_parcouru)
    #     queue = [(0, 1, self.start.name, [[0, self.start.name]])]
    #     visited = set()  # (zone, temps)

    #     while queue:
    #         cost, turn, current_zone_name, path = heapq.heappop(queue)

    #         if current_zone_name == self.end.name:
    #             return path, turn  # On a trouvé le chemin le plus rapide

    #         if (current_zone_name, turn) in visited:
    #             continue
    #         visited.add((current_zone_name, turn))

    #         current_zone = self.get_zone(current_zone_name)
    #         # --- EXPLORATION DES VOISINS (Mouvements + Attente) ---
    #         # 1. Attendre sur place (toujours possible si capacité respectée)
    #         next_zones = current_zone.get_next_zones(self.__zones, self.__connections) + [current_zone]

    #         for next_zone in next_zones:
    #             can_pass = True
    #             # Arrival_time calculation
    #             travel_time = 1 if next_zone.name == current_zone_name else next_zone.get_cost()
    #             arrival_time = turn + travel_time

    #             # Capacity constraints verification
    #             if not self.is_available_zone(next_zone, turn, global_state):
    #                 can_pass = False

    #             if next_zone.name != current_zone_name:
    #                 if not self.is_available_link(current_zone, next_zone, turn, global_state):
    #                     can_pass = False

    #             for t in range(turn + 1, arrival_time):
    #                 if not self.is_available_zone(next_zone, t, global_state):
    #                     can_pass = False
    #                 if not self.is_available_zone(next_zone, arrival_time, global_state):
    #                     can_pass = False

    #             if can_pass:
    #                 heapq.heappush(queue, (arrival_time, arrival_time, next_zone.name, path + [[cost, next_zone.name]]))

    #     return None, None

    def dijkstra_space_time(self, global_state):
        # Priority Queue: (arrival_time, zone_name, path)
        queue = [(0, self.start.name, [(0, self.start.name)])]
        visited = set()

        while queue:
            current_time, current_zone_name, path = heapq.heappop(queue)

            if (current_zone_name, current_time) in visited:
                continue
            visited.add((current_zone_name, current_time))

            if current_zone_name == self.end.name:
                return path, current_time

            current_zone = self.get_zone(current_zone_name)
            neighbors = current_zone.get_next_zones(self.__zones, self.__connections)
            neighbors.append(current_zone)  # waiting

            for next_zone in neighbors:
                travel_time = next_zone.get_cost() if next_zone != current_zone else 1
                arrival_time = current_time + travel_time

                # Vérification capacité zone à l'arrivée
                if not self.is_available_zone(next_zone, arrival_time, global_state):
                    continue

                # Vérification capacité zone pendant le déplacement
                for t in range(current_time + 1, arrival_time):
                    if not self.is_available_zone(next_zone, t, global_state):
                        break
                else:
                    # Vérification capacité lien (si déplacement)
                    if next_zone != current_zone:
                        if not self.is_available_link_full(current_zone, next_zone, current_time, arrival_time, global_state):
                            continue

                    new_path = path + [(arrival_time, next_zone.name)]
                    heapq.heappush(queue, (arrival_time, next_zone.name, new_path))

        return None, None

    def is_available_zone(self, zone, turn, global_state) -> bool:
        current_occupancy = global_state['nodes'].get((zone.name, turn), 0)
        if current_occupancy >= zone.get_capacity():
            return False
        return True
    
    def is_available_link_full(self, zone_1, zone_2, start_time, end_time, global_state):
        # Trouver la connexion
        connection = None
        for link in self.__connections:
            if zone_1.name in link.get_linked_zones() and zone_2.name in link.get_linked_zones():
                connection = link
                break

        if connection is None:
            return False

        # Vérifier chaque tour du déplacement
        for t in range(start_time, end_time):
            if global_state['edges'].get((zone_1.name, zone_2.name, t), 0) >= connection.get_capacity():
                return False

        return True

    def update_states(self, path, global_state):
        for i in range(len(path) - 1):
            time_a, zone_a = path[i]
            time_b, zone_b = path[i + 1]

            # Réserver la zone pendant toute la durée
            for t in range(time_a, time_b):
                key = (zone_a, t)
                global_state['nodes'][key] = global_state['nodes'].get(key, 0) + 1

            # Réserver le lien pendant toute la durée du déplacement
            for t in range(time_a, time_b):
                edge_key = (zone_a, zone_b, t)
                global_state['edges'][edge_key] = global_state['edges'].get(edge_key, 0) + 1

        # Dernière zone à l'arrivée
        last_time, last_zone = path[-1]
        key = (last_zone, last_time)
        global_state['nodes'][key] = global_state['nodes'].get(key, 0) + 1

    # def is_available_link(self, zone_1, zone_2, turn, global_state) -> bool:
    #     for link in self.__connections:
    #         if zone_1.name in link.get_linked_zones() and zone_2.name in link.get_linked_zones():
    #             connection = link
    #     current_occupancy = global_state['edges'].get((zone_1.name, zone_2.name, turn), 0)
    #     if current_occupancy >= connection.get_capacity():
    #         return False
    #     return True

    def get_zone(self, name):
        for zone in self.__zones:
            if zone.name == name:
                return (zone)

    # def update_states(self, path, global_state):
    #     for i in range(len(path)):
    #         arrival_time, zone_name = path[i]
    #         if i + 1 < len(path):
    #             departure_time = path[i + 1][0]
    #             for t in range(arrival_time, departure_time):
    #                 node_key = (zone_name, t)
    #                 global_state['nodes'][node_key] = global_state['nodes'].get(node_key, 0) + 1
    #                 next_zone_name = path[i + 1][1]
    #                 edge_key = (zone_name, next_zone_name, t)
    #                 global_state['edges'][edge_key] = global_state['edges'].get(edge_key, 0) + 1

    #         else:
    #             node_key = (zone_name, arrival_time)
    #             global_state['nodes'][node_key] = global_state['nodes'].get(node_key, 0) + 1
