# from ..parser import parse_unit, parse_group
from mycfg import parser


class Group:

    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg

        self.unit_names = cfg.get("units", [])
        self.group_names = cfg.get("groups", [])

        self.units = [parser.parse_unit(z) for z in self.unit_names]
        self.groups = [parser.parse_group(z) for z in self.group_names]

    def get_all_units(self, visited_groups):
        units = self.units
        for group in self.groups:
            if group.name in visited_groups:
                continue
            visited_groups.append(group.name)
            units.extend(group.get_all_units(visited_groups))
        return units
