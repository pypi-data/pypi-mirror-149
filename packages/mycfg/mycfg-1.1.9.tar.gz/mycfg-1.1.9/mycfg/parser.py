from mycfg.state import State
from mycfg.obj import unit, group, environment


def parse_unit(unit_name):
    if unit_name not in State.unit_mapping:
        State.unit_mapping[unit_name] = unit.Unit(unit_name, State.config["units"][unit_name])
    return State.unit_mapping[unit_name]


def parse_group(group_name):
    if group_name not in State.group_mapping:
        State.group_mapping[group_name] = group.Group(group_name, State.config["groups"][group_name])
    return State.group_mapping[group_name]


def parse_units(units):
    unit_mapping = dict()
    for unt in units:
        unit_mapping[unt] = parse_unit(unt)
    return unit_mapping


def parse_groups(groups):
    group_mapping = dict()
    for grp in groups:
        group_mapping[grp] = parse_group(grp)
    return group_mapping


def parse_environments(environments):
    env_mapping = dict()
    for env in environments:
        env_mapping[env] = environment.Environment(env, environments[env])
    return env_mapping
