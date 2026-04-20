from src import get_parsed_map


def main():
    try:
        config = get_parsed_map("maps/medium/02_circular_loop.txt")
        for drone in config['drones']:
            print(drone)
        for zone in config['nodes']:
            print(zone)
        for connection in config['connections']:
            print(connection)
    except Exception as e:
        print(e)


main()
