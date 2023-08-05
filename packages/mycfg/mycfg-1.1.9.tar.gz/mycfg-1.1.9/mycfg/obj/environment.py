from mycfg import parser


class Environment:

    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg
        # print(name, cfg)

        self.group_names = cfg.get("groups", [])
        self.groups = [parser.parse_group(z) for z in self.group_names]

        self.default_package_manager = cfg.get("default-package-manager", None)
