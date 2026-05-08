from src import get_parsed_map, Visualizer, Zone, Connection, Drone, PathFinder
from pathlib import Path


def main():
    zones = []
    links = []
    drones = []
    try:
        input_file = 'maps/challenger/01_the_impossible_dream.txt'
        input = Path(input_file)
        if input.suffix == '.txt':
            config = get_parsed_map(input)
        else:
            raise ValueError("[ERROR]: input file has to be a .txt file")
        for drone in config['drones']:
            drones.append(Drone(drone['id'], drone['place']))
        for zone in config['nodes']:
            zones.append(Zone(zone))
        for connection in config['connections']:
            links.append(Connection(connection))
        for zone in zones:
            if zone.type == 'start_hub':
                start = zone
            if zone.type == 'end_hub':
                end = zone
        pathfinder = PathFinder(start, end, zones, links, drones)
        schedule = pathfinder.process()
        visualizer = Visualizer(zones, links, schedule)
        visualizer.on_execute()
    except PermissionError:
        print("\033[0;31m[ERROR]: permission denied for input file\033[0;0m")
    except Exception as e:
        print(f"\033[0;31m{e}\033[0;0m")


main()
