from src import get_parsed_map, parse_arguments, Visualizer, Zone, \
    Connection, Drone, PathFinder
from pathlib import Path


def main():
    zones = []
    links = []
    drones = []
    try:
        args = parse_arguments()
        input = Path(args.input_file)
        if input.suffix != '.txt':
            raise ValueError("[ERROR]: input file has to be a .txt file")

        config = get_parsed_map(input)

        for drone in config['drones']:
            drones.append(Drone(drone['id'], drone['place']))

        for zone in config['nodes']:
            zones.append(Zone(zone))

        for connection in config['connections']:
            links.append(Connection(connection))

        start = None
        end = None
        for zone in zones:
            if zone.type == 'start_hub':
                start = zone
            if zone.type == 'end_hub':
                end = zone

        pathfinder = PathFinder(start, end, zones, links, drones)
        schedule = pathfinder.process()

        visualizer = Visualizer(zones, links, schedule)
        visualizer.on_execute()

        with open("logs.txt", 'w') as file:
            for turn, data in visualizer.logs:
                file.write(f"Turn {turn}:{data.split(':')[1]}\n\n")

    except PermissionError:
        print("\033[0;31m[ERROR]: permission denied for input file\033[0;0m")
    except Exception as e:
        print(f"\033[0;31m{e}\033[0;0m")


if __name__ == '__main__':
    main()
