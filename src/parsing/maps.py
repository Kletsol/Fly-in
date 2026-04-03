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
        allowed_types = ['start_hub', 'end_hub', 'hub']
        if self.zone_type not in allowed_types:
            raise MapError(f"[ERROR]: Invalid zone type {self.zone_type}")


class ValidConnection(BaseModel):
    linked_zones: str

    @model_validator(mode='after')
    def validate(self) -> "ValidConnection":
        try:
            zones = self.linked_zones.split('-')
        except Exception:
            raise MapError


def get_parsed_map(path: str) -> ValidMap:
    try:
        with open(path, "r") as file:
            data = file.read()
        nodes = []
        connections = []
        for line in data:
            args = line.split(' ')
            if args[0] == 'connection':
                connections.append()
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
