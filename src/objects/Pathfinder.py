from src import Drone
from typing import Any


class Simulation:
    """A class to execute the simulate the paths of each drone, using
    the selected algorithm"""
    def __init__(self, drones: list[Drone], algorithm: Any) -> None:
        """Initiates the simulation with a list of drones and the
        algorithm to use

        Args:
            drones (list[Drone]): A list containing all the drones to move
            algorithm (Any): The defined algorithm
        """
        self.__drones = drones
        self.algorithm = algorithm

    def simulate(self) -> dict[str, list[list[Any]]]:
        """The core method of our pathfinding. Takes every drone on by one,
        processes it through the algorithm, and returns a final_schedule
        containing a path for each drone.

        Raises:
            Exception: Raises an error if a drone didn't find a valid path

        Returns:
            dict[str, list[list[Any]]]: A dict containing the whole schedule,
            for every drone at every turn
        """
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
        """A method called after every path found, to update the global state
        of zones and connections

        Args:
            path (list[list[Any]]): The last path found by the algorithm
            global_state (dict[str, dict[tuple[str, float], int]]): The dict
            where the occupancy is stored
        """

        for i in range(len(path) - 1):
            time_a, zone_a = path[i]
            time_b, zone_b = path[i + 1] if '-' not in path[i + 1][1] else \
                path[i + 2]

            # Current zone
            global_state['nodes'][(zone_a, time_a)] = \
                global_state['nodes'].get((zone_a, time_a), 0) + 1

            # Link
            for t in range(int(time_a), int(time_b)):
                edge_key = tuple(sorted([zone_a, zone_b])) + (t,)
                global_state['edges'][edge_key] = \
                    global_state['edges'].get(edge_key, 0) + 1

        # Last zone
        last_time, last_zone = path[-1]
        key = (last_zone, last_time)
        global_state['nodes'][key] = global_state['nodes'].get(key, 0) + 1
