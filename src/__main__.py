from src import get_parsed_map, Visualizer, Zone, Connection, Drone, PathFinder


def main():
    zones = []
    links = []
    drones = []
    try:
        config = get_parsed_map("maps/challenger/01_the_impossible_dream.txt")
        print("\n=== DRONES ===\n")
        for drone in config['drones']:
            drones.append(Drone(drone['id'], drone['place']))
        print("\n=== ZONES ===\n")
        for zone in config['nodes']:
            zones.append(Zone(zone))
        print("\n=== CONNECTIONS ===\n")
        for connection in config['connections']:
            links.append(Connection(connection))
        for zone in zones:
            if zone.type == 'start_hub':
                start = zone
            if zone.type == 'end_hub':
                end = zone
        pathfinder = PathFinder(start, end, zones, links, drones)
        pathfinder.initiate_drones()
        schedule = pathfinder.process()
        visualizer = Visualizer(zones, links, schedule)
        visualizer.on_execute()
    except Exception as e:
        print(e)


main()
