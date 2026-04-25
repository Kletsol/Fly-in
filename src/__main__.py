from src import get_parsed_map, Visualizer, Zone, Connection, Drone, PathFinder


def main():
    zones = []
    links = []
    drones = []
    try:
        config = get_parsed_map("maps/hard/01_maze_nightmare.txt")
        print("\n=== DRONES ===\n")
        for drone in config['drones']:
            drones.append(Drone(drone['id'], drone['place']))
            print(drones[-1].get_id())
            print(drones[-1].get_position())
        print("\n=== ZONES ===\n")
        for zone in config['nodes']:
            zones.append(Zone(zone))
            print(zones[-1].get_coords())
            print(zones[-1].get_rgb())
            print(zones[-1].get_metadata())
        print("\n=== CONNECTIONS ===\n")
        for connection in config['connections']:
            links.append(Connection(connection))
            print(connection)
    except Exception as e:
        print(e)
    for zone in zones:
        if zone.type == 'start_hub':
            start = zone
        if zone.type == 'end_hub':
            end = zone
    print("\n=== PATHFINDING ===\n")
    pathfinder = PathFinder(start, end, zones, links, drones)
    pathfinder.initiate_drones()
    pathfinder.initiate_dict(0)
    pathfinder.process()
    visualizer = Visualizer(zones, links, None)
    visualizer.on_execute()


main()
