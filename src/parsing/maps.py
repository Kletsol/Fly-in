from typing import Any, Optional


class ConfigError(Exception):
    pass


class MapError(Exception):
    pass


class ZoneError(Exception):
    pass


class ConnectionError(Exception):
    pass


def get_parsed_map(path: str) -> dict[str, Any]:
    try:
        with open(path, "r") as file:
            raw_config = file.readlines()
        start_count = 0
        end_count = 0
        line_count = 1
        comms_count = 0
        nodes = []
        connections = []
        for line in raw_config:

            # Ignore comments and empty lines
            if line.startswith(('#', '\n')):
                comms_count += 1
                continue

            elif '#' in line:
                line = line.split('#')[0].rstrip(' ')

            # Nb_drones
            elif line.startswith('nb_drones'):
                try:
                    drones = get_drones(line)
                except Exception as e:
                    raise Exception(f"Line {line_count + comms_count} - {e}")

                if line_count > 1:
                    raise ConfigError("[ERROR]: nb_drones has to be"
                                      "on first line")

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
                except Exception as e:
                    raise Exception(f"Line {line_count + comms_count} - {e}")

            # Connections
            elif line.startswith('connection'):
                try:
                    if '[' in line:
                        splitted_line = line.split("[")
                        caracs = splitted_line[0].strip(' ').split(' ')
                        metadata = splitted_line[1].rstrip(']\n').split(' ')
                        metadata = verify_metadata(metadata, "connection")
                        connections.append(
                            get_connection(nodes, connections,
                                           caracs, metadata))
                    else:
                        connections.append(
                            get_connection(nodes, connections,
                                           line.split(' ')))
                except Exception as e:
                    raise Exception(f"Line {line_count + comms_count} - {e}")

            # Other cases
            else:
                raise ConfigError(f"Line {line_count + comms_count}"
                                  "- [ERROR]: Unknown area type")

            line_count += 1

    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR]: map file not found in {path}")
    config = {'drones': drones,
              'nodes': nodes,
              'connections': connections}
    return config


def get_drones(line: str) -> list:
    data = line.split(' ')
    if len(data) < 2:
        raise MapError("[ERROR]: No number of drones found")

    # Int and value verification
    try:
        nb_drones = int(data[1])
    except ValueError:
        raise MapError("[ERROR]: Number of drones must be an int")
    if nb_drones < 0:
        raise MapError("[ERROR]: Number of drones must be positive")

    # ID and localisation application
    drones = []
    for i in range(1, nb_drones + 1):
        id = 'D' + str(i)
        drones.append({'id': id,
                       'place': None})

    return drones


def get_zone(prev_zones: list, line: list[str],
             metadata: Optional[list[str]] = None) -> dict:
    if len(line) != 4:
        raise ZoneError("[ERROR]: Invalid count of arguments in line")

    # Name availability
    for zone in prev_zones:
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


def get_connection(prev_zones: list, prev_connections: list, line: list[str],
                   metadata: Optional[list[str]] = None) -> dict:

    # Duplication check
    linked_zones = line[1].rstrip('\n').split('-')
    for connection in prev_connections:
        if linked_zones[0] in connection['linked_zones'] and\
                linked_zones[1] in connection['linked_zones']:
            raise ConnectionError("[ERROR]: Duplicated connections"
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


def verify_metadata(metadata: list[str], area_type: str) -> dict:
    output = {}
    for data in metadata:
        data = data.split('=')
        output.update({data[0]: data[1]})
        if area_type == 'zone':
            if data[0] not in ['zone', 'color', 'max_drones']:
                raise MapError(f"[ERROR]: invalid metadata block '{data[0]}'")
            if data[0] == 'zone':
                if data[1] not in ['normal', 'blocked',
                                   'restricted', 'priority']:
                    raise MapError(f"[ERROR]: invalid zone type '{data[1]}'")
        if area_type == 'connection':
            if data[0] not in ['max_link_capacity']:
                raise MapError(f"[ERROR]: invalid metadata block '{data[0]}'")
        if data[0] == 'max_drones' or data[0] == 'max_link_capacity':
            try:
                value = int(data[1])
                if value < 0:
                    raise ConfigError("[ERROR]: capacity value "
                                      "must be positive int")
                output.update({data[0]: value})
            except ValueError:
                raise ConfigError("[ERROR]: capacity value "
                                  "must be positive int")
    return output
