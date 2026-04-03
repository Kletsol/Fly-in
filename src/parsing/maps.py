from pydantic import BaseModel, model_validator


class MapError(Exception):
    pass


class ZoneError(Exception):
    pass


class ConnectionError(Exception):
    pass


class ValidZone(BaseModel):
    zone_type: str
    name: str
    x_coord: int
    y_coord: int
    metadata: list[str]

    @model_validator(mode='after')
    def validate(self) -> "ValidZone":
        allowed_types = ['start_hub:', 'end_hub:', 'hub:']
        if self.zone_type not in allowed_types:
            raise MapError(f"[ERROR]: Invalid zone type {self.zone_type}")
        return self


class ValidConnection(BaseModel):
    linked_zones: str
    metadata: list[str]

    @model_validator(mode='after')
    def validate(self) -> "ValidConnection":
        try:
            self.linked_zones.split('-')
        except Exception:
            raise MapError("[ERROR]: Invalid connection: expected <name1>-"
                           f"<name2>, got {self.linked_zones}")
        return self


def get_parsed_map(path: str) -> tuple[list[ValidZone], list[ValidConnection]]:
    try:
        with open(path, "r") as file:
            data = file.readlines()
        nodes = []
        connections = []
        for line in data:
            print(line)
            args = line.split(' ')
            print(args)
            if args[0].startswith('#') or args[0].startswith('\n') or line == '':
                continue
            elif line.startswith('nb_drones'):
                print("Work in progress here")
            elif args[0] == 'connection:':
                if args[2]:
                    connections.append(
                        ValidConnection(linked_zones=args[1],
                                        metadata=args[2])
                    )
                else:
                    connections.append(
                        ValidConnection(linked_zones=args[1])
                    )
            else:
                nodes.append(
                    ValidZone(zone_type=args[0],
                              name=args[1],
                              x_coord=args[2],
                              y_coord=args[3],
                              metadata=args[4].split(' '))
                )
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR]: map file not found in {path}")
    return nodes, connections
