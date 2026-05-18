import heapq
from src import Zone, Connection, Drone, BaseAlgorithm
from typing import Any


class Dijkstra(BaseAlgorithm):
    def __init__(self, start: Zone, end: Zone, zones: list[Zone],
                 connections: list[Connection], drones: list[Drone]) -> None:
        self.start = start
        self.end = end
        self.__zones = zones
        self.__connections = connections
        self.__drones = drones
        self.max_time = 2000
        self.algorithm = Dijkstra

    def process(self, global_state: dict[str, dict[
            tuple[str, float], int]]
    ) -> tuple[list[list[Any]], float] | tuple[None, None]:
        """The main part of the Dijkstra algorithm, where a given drone finds
        his path depending on the global_state's reservations

        Args:
            global_state (dict[str, dict[ tuple[str, float], int]]): A dict
            that stores, for each turn, the occupancy of all zones and edges

        Returns:
            tuple[list[list[Any]], float] | tuple[None, None]: The path the
            drone found, or None if he couldn't find a path
        """
        queue = [(0.0, 0, 0.0, self.start.name, [[0, self.start.name]])]
        visited: dict[tuple[Any, float], tuple[float, int]] = {}

        while queue:
            cost, benefit, turn, curr_zone_name, path = heapq.heappop(queue)

            if turn > self.max_time:
                continue

            if curr_zone_name == self.end.name:
                return path, turn  # Return the fastest path

            key = (curr_zone_name, turn)
            if key in visited:
                if visited[key] <= (cost, benefit):
                    continue
            visited[key] = (cost, benefit)

            current_zone: Zone = self.get_zone(curr_zone_name)

            # Exploration of the neighboring zones
            next_zones = current_zone.get_next_zones(self.__zones,
                                                     self.__connections)

            wait_turn = turn + 1
            if self.is_available_zone(current_zone, wait_turn, global_state):
                new_cost = cost + 1
                new_benefit = benefit + current_zone.get_priority_benefit()
                heapq.heappush(queue, (new_cost, new_benefit, wait_turn,
                                       curr_zone_name, path +
                                       [[wait_turn, curr_zone_name]]))

            for next_zone in next_zones:
                # Arrival_time calculation
                travel_time = next_zone.get_cost()
                if travel_time == float('inf'):
                    continue
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
                new_benefit = benefit + next_zone.get_priority_benefit()

                heapq.heappush(queue,
                               (new_cost, new_benefit, arrival_time,
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
        """A method that checks a zone's capacity and occupancy at a given time

        Args:
            zone (Zone): The zone to check
            turn (float): The turn to take into account
            global_state (dict[str, dict[tuple[str, float], int]]): The dict
            where the occupancy is stored

        Returns:
            bool: True if the zone is available, else False
        """
        current_occupancy = global_state['nodes'].get((zone.name, turn), 0)
        capacity = zone.get_capacity()
        if zone.type in ['start_hub', 'end_hub']:
            capacity = len(self.__drones)
        if current_occupancy < capacity:
            return True
        return False

    def get_connection(self, prev_zone: str, next_zone: str,
                       return_name: bool) -> Any:
        """A method that, for two given zones, returns the connection
        between them or it's name (depending on 'return_name' value)

        Args:
            prev_zone (str): One of the zones to process
            next_zone (str): The other zone to process
            return_name (bool): True or False depending on whether we
            want to obtain the name of the connection or the object itself

        Returns:
            Any: The name of the connection if return_name is True, else
            the object connection
        """
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
        """A method that checks a connection's capacity and occupancy at a
        given time

        Args:
            zone_1 (Zone): The zone the drone is on
            zone_2 (Zone): The zone the drone is heading towards
            start_time (int): The current turn
            end_time (int): The turn at which the drone must arrive on zone_2
            global_state (dict[str, dict[tuple[str, float], int]]): The dict
            where the occupancy is stored

        Returns:
            bool: True if the connection is available, else False
        """

        # Find the connection
        connection: Connection = self.get_connection(zone_1.name, zone_2.name,
                                                     False)

        if connection is None:
            return False

        # Check availability for each turn of the movement
        for t in range(start_time, end_time):
            edge_key = tuple(sorted([zone_1.name, zone_2.name])) + (t,)
            if global_state['edges'].get(edge_key, 0) >= \
                    connection.get_capacity():
                return False
        return True

    def get_zone(self, name: str) -> Any:
        """A getter that takes the name of a zone and returns the
        corresponding object 'Zone'

        Args:
            name (str): The name of the zone to find

        Returns:
            Any: The corresponding object 'Zone'
        """
        for zone in self.__zones:
            if zone.name == name:
                return zone
