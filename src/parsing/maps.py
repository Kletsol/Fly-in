from typing import Any, Optional
import time


class ConfigError(Exception):
    """A custom configuration error type"""
    pass


class MapError(Exception):
    """A custom map error type"""
    pass


class ZoneError(Exception):
    """A custom zone error type"""
    pass


class ConnectionError(Exception):
    """A custom connection error type"""
    pass


def get_parsed_map(path: str) -> dict[str, Any]:
    """A method that takes every line of the input file,
    parses it depending on the type of content and returns the parsed config

    Args:
        path (str): The path to the input file

    Raises:
        ValueError: Any error related to the value or the type of a variable
        ConfigError: Any error related to the general configuration
        MapError: Any error related to the map itself
        ZoneError: Any error related to a zone
        ConnectionError: Any error related to a connection
        FileNotFoundError: Any error related to a file not found

    Returns:
        dict[str, Any]: The parsed config
    """
    try:
        with open(path, "r") as file:
            raw_config = file.readlines()
    except Exception as e:
        raise ValueError(f"[ERROR]: {e}")
    try:
        start_count = 0
        end_count = 0
        line_count = 1
        comm_count = 0
        drones_count = 0
        nodes: list[dict[Any, Any]] = []
        connections: list[dict[Any, Any]] = []
        for line in raw_config:

            # Ignore comments and empty lines
            if line.startswith(('#', '\n')):
                comm_count += 1
                continue

            elif not line.startswith(('nb_drones: ',
                                      'start_hub: ',
                                      'end_hub: ',
                                      'hub: ',
                                      'connection:')):
                raise ConfigError(f"\033[0;31mLine {line_count + comm_count}"
                                  " - [ERROR]: Invalid data "
                                  f"'{line.rstrip("\n")}'\033[0;0m")

            elif '#' in line:
                line = line.split('#')[0].rstrip(' ')

            # Nb_drones
            elif line.startswith('nb_drones'):
                drones_count += 1
                if drones_count > 1:
                    raise ConfigError("[ERROR]: duplicated nb_drones in file")
                try:
                    drones = get_drones(line)
                except Exception as e:
                    raise Exception(f"\033[0;31mLine {line_count + comm_count}"
                                    f" - {e}\033[0;0m")
                if len(drones) > 1000:
                    print("\033[0;33m[WARNING]: An excessive number of drones "
                          "may overload the computer and cause an interminable"
                          " wait time, as the computer is not powerful enough."
                          " If you wish to avoid this, please close the "
                          "program within 50 seconds.\033[0;0m")
                    try:
                        time.sleep(42)
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt()

            elif drones_count < 1:
                raise ConfigError("[ERROR]: no nb_drones found in file. Please"
                                  " make sure it is present and written on the"
                                  " first line ")

            # Start
            elif line.startswith(('start_hub', 'end_hub', 'hub')):
                if line.startswith('start_hub:'):
                    start_count += 1
                    if start_count > 1:
                        raise MapError("[ERROR]: Too many start hubs in map")
                elif line.startswith('end_hub:'):
                    end_count += 1
                    if end_count > 1:
                        raise MapError("[ERROR]: Too many end hubs in map")
                try:
                    if '[' in line:
                        splitted_line = line.split("[")
                        caracs = splitted_line[0].strip(' ').split(' ')
                        metadata = splitted_line[1].rstrip(']\n').split(' ')
                        valid_metadata = verify_metadata(metadata, "zone")
                        if line.startswith(('start_hub', 'end_hub')):
                            if 'max_drones' in valid_metadata and\
                                    valid_metadata['max_drones'] < len(drones):
                                raise ZoneError("[ERROR]: insufficent space "
                                                "for all drones")
                        nodes.append(get_zone(nodes, caracs, valid_metadata))
                    else:
                        nodes.append(get_zone(nodes, line.split(' ')))
                except (Exception, MapError, ZoneError, ConfigError) as e:
                    raise ZoneError(f"\033[0;31mLine {line_count + comm_count}"
                                    f" - {e}\033[0;0m")

            # Connections
            elif line.startswith('connection'):
                try:
                    if '[' in line:
                        splitted_line = line.split("[")
                        caracs = splitted_line[0].strip(' ').split(' ')
                        metadata = splitted_line[1].rstrip(']\n').split(' ')
                        new_metadata = verify_metadata(metadata, "connection")
                        connections.append(
                            get_connection(nodes, connections,
                                           caracs, new_metadata))
                    else:
                        connections.append(
                            get_connection(nodes, connections,
                                           line.split(' ')))
                except (Exception, ConnectionError) as e:
                    raise ConnectionError(f"\033[0;31mLine "
                                          f"{line_count + comm_count}"
                                          f" - {e}\033[0;0m")

            # Other cases
            else:
                raise ConfigError(f"\033[0;31mLine {line_count + comm_count}"
                                  "- [ERROR]: Unknown area type\033[0;0m")

            line_count += 1

    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR]: map file not found in {path}")
    if start_count < 1:
        raise MapError("[ERROR]: missing start_hub zone in file")
    if end_count < 1:
        raise MapError("[ERROR]: missing end_hub zone in file")
    config = {'drones': drones,
              'nodes': nodes,
              'connections': connections}
    return config


def get_drones(line: str) -> list[dict[str, str]]:
    """A method that takes a line, extracts the number of drones
    and creates a list of drone IDs

    Args:
        line (str): The line to process

    Raises:
        MapError: No number of drones found
        MapError: Number of drones not an int
        MapError: Number of drones not positive

    Returns:
        list[dict[str, str]]: A list of drone IDs
    """
    data = line.split(' ')
    if len(data) < 2:
        raise MapError("[ERROR]: No number of drones found")

    # Int and value verification
    try:
        nb_drones = int(data[1])
    except ValueError:
        raise MapError("[ERROR]: Number of drones must be an int")
    if nb_drones <= 0:
        raise MapError("[ERROR]: Number of drones must be positive")

    # ID and localisation application
    drones = []
    for i in range(1, nb_drones + 1):
        id = 'D' + str(i)
        drones.append({'id': id})

    return drones


def get_zone(prev_zones: list[Any], line: list[str],
             metadata: Optional[dict[Any, Any]] = None) -> \
                dict[str, Any]:
    """A method that, for a line defining a zone, parses it and returns all
    the data organised in a dict

    Raises:
        ZoneError: Too many arguments in line
        ZoneError: Not enough arguments in line
        ZoneError: invalid character '-' in zone name
        ZoneError: name already taken
        ValueError: Coordinates not of type int

    Returns:
        dict[str, Any]: A dict containing the zone's data
    """
    if len(line) > 4:
        raise ZoneError("[ERROR]: Too many arguments in line. Please make "
                        "sure each argument is separated by a space, and "
                        "no space is used in an argument")
    elif len(line) < 4:
        raise ZoneError("[ERROR]: Not enough arguments in line. Please make "
                        "sure each argument is separated by a space")

    # Name availability
    for zone in prev_zones:
        if '-' in line[1]:
            raise ZoneError("[ERROR]: invalid character '-' in zone name "
                            f"'{line[1]}'")
        if line[1] == zone['name']:
            raise ZoneError(f"[ERROR]: name '{line[1]}' already taken")

    # Int verification
    try:
        x_coord = int(line[2])
        y_coord = int(line[3])
    except ValueError:
        raise ValueError("[ERROR]: Coordinates have to be of type int")

    return {'zone_type': line[0].rstrip(':'),
            'name': line[1],
            'x_coord': x_coord,
            'y_coord': y_coord,
            'metadata': metadata}


def get_connection(prev_zones: list[Any],
                   prev_connections: list[Any],
                   line: list[str],
                   metadata: Optional[dict[Any, Any]] = None) -> \
                    dict[str, Any]:
    """A method that, for a line defining a connection, parses it and returns
    all the data organised in a dict

    Raises:
        ConnectionError: Duplicated connection
        ConnectionError: Inexistent linked zone

    Returns:
        dict[str, Any]: A dict containing the connection's data
    """

    # Duplication check
    linked_zones = line[1].rstrip('\n').split('-')
    for connection in prev_connections:
        if linked_zones[0] in connection['linked_zones'] and\
                linked_zones[1] in connection['linked_zones']:
            raise ConnectionError("[ERROR]: Duplicated connections "
                                  "are not allowed")

    # Existing zones check
    available_zones = []
    for zone in prev_zones:
        available_zones.append(zone['name'])
    if linked_zones[0] not in available_zones or\
            linked_zones[1] not in available_zones:
        raise ConnectionError("[ERROR]: linked zone doesn't exist")

    return {'linked_zones': linked_zones,
            'metadata': metadata}


def verify_metadata(metadata: list[str], area_type: str) -> dict[str, Any]:
    """A method that takes the line's metadata (zone or connection), and
    parses it depending on the type of the line

    Args:
        metadata (list[str]): The extracted metadata
        area_type (str): The type of the line (zone or connnection)

    Raises:
        ConfigError: Invalid metadata block
        ZoneError: Invalid metadata block
        ZoneError: Invalid zone type
        ZoneError: Invalid color
        MapError: Duplicated metadata
        ConnectionError: Invalid metadata block
        ConfigError: Capacity value not a positive int
        ConfigError: Capacity value not a positive int

    Returns:
        dict[str, Any]: The validated metadata
    """
    output: dict[str, str | int] = {}
    current_data_types = []
    for raw_data in metadata:
        data = raw_data.split('=')
        if len(data) < 2:
            raise ConfigError(f"[ERROR]: invalid metadata block {data}")
        output.update({data[0]: data[1]})
        if area_type == 'zone':
            if data[0] not in ['zone', 'color', 'max_drones']:
                raise ZoneError(f"[ERROR]: invalid metadata block '{data[0]}'")
            if data[0] == 'zone':
                if data[1] not in ['normal', 'blocked',
                                   'restricted', 'priority']:
                    raise ZoneError(f"[ERROR]: invalid zone type '{data[1]}'")
            if data[0] == 'color':
                if not data[1].isalpha():
                    raise ZoneError(f"[ERROR]: invalid color '{data[1]}' "
                                    "- colors must be single-word strings")
            if data[0] not in current_data_types:
                current_data_types.append(data[0])
            else:
                raise MapError(f"[ERROR]: duplicated metadata '{data[0]}'")
        if area_type == 'connection':
            if data[0] not in ['max_link_capacity']:
                raise ConnectionError("[ERROR]: invalid metadata block "
                                      f"'{data[0]}'")
        if data[0] == 'max_drones' or data[0] == 'max_link_capacity':
            try:
                value = int(data[1])
                if value < 1:
                    raise ConfigError("[ERROR]: capacity value "
                                      "must be positive int")
                output.update({data[0]: value})
            except ValueError:
                raise ConfigError("[ERROR]: capacity value "
                                  "must be positive int")
    return output
