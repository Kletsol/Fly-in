from src import get_parsed_map, Visualizer, Zone, Connection


def main():
    zones = []
    links = []
    try:
        config = get_parsed_map("maps/custom/Eternal_Tower_of_Doom.txt")
        print("\n=== DRONES ===\n")
        for drone in config['drones']:
            print(drone)
        print("\n=== ZONES ===\n")
        for zone in config['nodes']:
            zones.append(Zone(zone))
            print(zones[-1].get_coords())
            print(zones[-1].get_rgb())
        print("\n=== CONNECTIONS ===\n")
        for connection in config['connections']:
            links.append(Connection(connection))
            print(connection)
    except Exception as e:
        print(e)
    visualizer = Visualizer(zones, links, None)
    visualizer.on_execute()


main()
