from src import Drone
from typing import Any


class Simulation:
    def __init__(self, drones: list[Drone], algorithm) -> None:
        self.__drones = drones
        self.algorithm = algorithm

    def simulate(self) -> dict[str, list[list[Any]]]:
        global_state: dict[str, dict[tuple[str, float], int]] = \
            {'nodes': {}, 'edges': {}}
        final_schedule = {}

        for drone in self.__drones:
            path, arrival_time = self.algorithm.process(global_state)
            if path:
                self.update_states(path, global_state)
                final_schedule[drone.get_id()] = path
            else:
                raise Exception(f"\033[0;31m[ERROR]: Drone {drone.get_id()}"
                                " could not find a path\033[0;0m")
        return final_schedule

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
