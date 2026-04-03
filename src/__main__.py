from src import ValidZone, ValidConnection, get_parsed_map


def main():
    try:
        zones, connections = get_parsed_map("maps/easy/01_linear_path.txt")
        print(zones)
        print(connections)
    except Exception as e:
        print(e)


main()
