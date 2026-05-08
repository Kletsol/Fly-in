import heapq


class PathFinder:
    def __init__(self, start, end, zones, connections, drones):
        self.start = start
        self.end = end
        self.__zones = zones
        self.__connections = connections
        self.__drones = drones
        self.output = {}
        self.max_time = 10000

    def initiate_drones(self):
        for drone in self.__drones:
            drone.set_position(self.start.name)

    def process(self):
        global_state = {'nodes': {}, 'edges': {}}
        final_schedule = {}

        for drone in self.__drones:
            drone_name = drone.get_id()
            path, arrival_time = self.dijkstra_space_time(global_state)
            if path:
                print(path)
                self.update_states(path, global_state)
                final_schedule[drone.get_id()] = path
            else:
                print(f"\033[0;31m[ERROR]: Drone {drone.get_id()} could not find a path\033[0;0m")
        print(arrival_time)
        print(drone_name)
        # print(global_state)
        return final_schedule

    def dijkstra_space_time(self, global_state):
        """
        - start_node: Nom de la zone de départ
        - end_node: Nom de la zone d'arrivée
        - start_time: Temps auquel le drone commence son trajet
        - global_state: Dict ou Set contenant les réservations des drones précédents 
                    ex: {(zone, temps): occupation, (zone_a, zone_b, temps): occupation}
        - graph_data: Dictionnaire contenant les capacités et types de zones
        """

        # Priority Queue: (coût_total, temps_actuel, zone_actuelle, chemin_parcouru)
        # wait_time = 0.02
        queue = [(0, 0, self.start.name, [[0, self.start.name]])]
        visited = {}

        while queue:
            cost, turn, current_zone_name, path = heapq.heappop(queue)

            if turn > self.max_time:
                continue

            if current_zone_name == self.end.name:
                return path, turn  # On a trouvé le chemin le plus rapide

            key = (current_zone_name, turn)
            if key in visited:
                if visited[key] <= cost:
                    continue
            visited[key] = cost

            current_zone = self.get_zone(current_zone_name)
            # --- EXPLORATION DES VOISINS (Mouvements + Attente) ---
            # 1. Attendre sur place (toujours possible si capacité respectée)
            next_zones = current_zone.get_next_zones(self.__zones, self.__connections)

            wait_turn = turn + 1
            if self.is_available_zone(current_zone, wait_turn, global_state):
                new_cost = cost + 1
                heapq.heappush(queue, (new_cost, wait_turn, current_zone_name, path + [[wait_turn, current_zone_name]]))

            for next_zone in next_zones:
                # Arrival_time calculation
                travel_time = next_zone.get_cost()
                arrival_time = turn + travel_time

                if not self.is_available_link_full(current_zone, next_zone, turn, arrival_time, global_state):
                    continue

                if not self.is_available_zone(next_zone, arrival_time, global_state):
                    continue

                new_cost = cost + travel_time
                # if arrival_time == turn + 2 and counter is True:
                #     path += [[turn + 1, "test"]]
                #     counter = False

                heapq.heappush(queue, (new_cost, arrival_time, next_zone.name, path + ([[turn + 1, self.get_connection(current_zone_name, next_zone.name, True)], [arrival_time, next_zone.name]] if arrival_time == turn + 2 else [[arrival_time, next_zone.name]])))

        return None, None

    def is_available_zone(self, zone, turn, global_state) -> bool:
        current_occupancy = global_state['nodes'].get((zone.name, turn), 0)
        capacity = zone.get_capacity()
        if zone.type in ['start_hub', 'end_hub']:
            capacity = len(self.__drones)
        if current_occupancy < capacity:
            # print(turn)
            return True
        return False

    def get_connection(self, prev_zone, next_zone, return_name):
        zones = ''
        for connection in self.__connections:
            zones_list = connection.get_linked_zones()
            if prev_zone in zones_list and next_zone in zones_list:
                zones = f"{zones_list[0]}-{zones_list[1]}"
                if return_name is True:
                    return zones
                else:
                    return connection
        return None

    def is_available_link_full(self, zone_1, zone_2, start_time, end_time, global_state):
        # Trouver la connexion
        connection = self.get_connection(zone_1.name, zone_2.name, False)

        if connection is None:
            return False

        # Vérifier chaque tour du déplacement
        for t in range(start_time, end_time):
            edge_key = tuple(sorted([zone_1.name, zone_2.name])) + (t,)
            if global_state['edges'].get(edge_key, 0) >= connection.get_capacity():
                return False
        return True

    def update_states(self, path, global_state):
        for i in range(len(path) - 1):
            time_a, zone_a = path[i]
            time_b, zone_b = path[i + 1] if '-' not in path[i + 1][1] else path[i + 2]

            # 1. Zone de départ : occupée uniquement au temps de départ
            global_state['nodes'][(zone_a, time_a)] = global_state['nodes'].get((zone_a, time_a), 0) + 1

            # 2. Lien : occupé pendant tout le déplacement
            for t in range(time_a, time_b):
                edge_key = tuple(sorted([zone_a, zone_b])) + (t,)
                global_state['edges'][edge_key] = global_state['edges'].get(edge_key, 0) + 1

        # Dernière zone à l'arrivée
        last_time, last_zone = path[-1]
        key = (last_zone, last_time)
        global_state['nodes'][key] = global_state['nodes'].get(key, 0) + 1

    def get_zone(self, name):
        for zone in self.__zones:
            if zone.name == name:
                return (zone)
