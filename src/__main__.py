from src import get_parsed_map


def main():
    try:
        config = get_parsed_map("maps/hard/02_capacity_hell.txt")
        print("\n=== DRONES ===\n")
        for drone in config['drones']:
            print(drone)
        print("\n=== ZONES ===\n")
        for zone in config['nodes']:
            print(zone)
        print("\n=== CONNECTIONS ===\n")
        for connection in config['connections']:
            print(connection)
    except Exception as e:
        print(e)


main()
