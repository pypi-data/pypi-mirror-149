import pathlib
import subprocess

import json
import yaml
import re

from mycfg import meta, const
from mycfg.error import PackageManagerError
from mycfg.state import State
from mycfg.parser import parse_environments


def ensure_list(item) -> list:
    if isinstance(item, str):
        return [item]
    return item


def list_diff(a, b):
    return [z for z in a if z not in b]


def sh(cmd):
    return subprocess.call(cmd, shell=True)


def sh_in(_dir, cmd):
    return subprocess.call(cmd, cwd=_dir, shell=True)


def exec_script(script_name):
    return sh_in(const.CUSTOM_SCRIPT_DIR, str(const.CUSTOM_SCRIPT_DIR.joinpath(pathlib.Path(script_name)).resolve()))


def read_file(path: pathlib.Path) -> str:
    with open(path, 'r') as f:
        return f.read()


def write_file(path: pathlib.Path, content: str):
    with open(path, 'w') as f:
        f.write(content)


def get_repo_url(string: str):
    if const.URL_REGEX.match(string):
        return string
    if any(map(string.startswith, ["gh:", "github:"])):
        parts = string.split(":")[1].split("/")
        username = parts[0]
        repo_name = parts[1] if len(parts) > 1 else "dotfiles"
        return f"https://github.com/{username}/{repo_name}"
    else:
        return None


def replace_path_variables(path: str) -> str:
    for k, v in const.PATH_VARIABLES.items():
        path = path.replace(k, v)
    return path


def load_config_file():
    re.match(r"^#include: (.+)((,)(.+))*", "")
    content = re.sub("^#include: (.+)",
                     lambda m: "\n".join(
                         [read_file(pathlib.Path(replace_path_variables(z))) for z in m.group(1).split(",")]),
                     read_file(const.CONFIG_FILE))
    file = yaml.full_load(content)
    State.config = file


def ensure_config_files():
    const.MYCFG_CONFIG_DIR.mkdir(exist_ok=True)
    const.DOTFILES_SAVE_DIR.mkdir(exist_ok=True)
    const.CUSTOM_SCRIPT_DIR.mkdir(exist_ok=True)
    if not const.META_FILE.exists():
        const.META_FILE.write_text(json.dumps(meta.default_meta))
    if not const.CONFIG_FILE.exists():
        const.CONFIG_FILE.write_text(yaml.dump(const.DEFAULT_CONFIG_CONTENT))


def install_pkg(pkg):
    pm = meta.get("package_manager")
    pms = meta.get("package_managers")
    for x in pms:
        if pm is not None:
            break
        pm = x
    if pm is None:
        pm = State.config.get(State.meta.get("environment")).get("default-package-manager", None)
    if pm is None:
        pkg_cfg = State.config.get("packages", {}).get("pkg", {})
        if default := pkg_cfg.get("default", None) is not None:
            sh(default)
        raise PackageManagerError(not_set=True)
    install_cmd = State.config.get("package-managers").get(pm).get("install")
    if install_cmd is None:
        raise PackageManagerError(missing_command="install")
    pkg_cfg = State.config.get("packages", {}).get(pkg, {})
    pkg_name = pkg_cfg.get(pm, pkg_cfg.get("default", None))
    if pkg_name == "none":
        return
    if pkg_name is None:
        raise PackageManagerError(missing_package=pkg)
    sh(f"{install_cmd} {pkg_name}")


def load():
    environment = State.meta.get("environment")
    env_mapping = parse_environments(State.config["environments"])
    env = env_mapping[environment]
    visited_units = []
    units = []
    for group in env.groups:
        units.extend(group.get_all_units(visited_units))
    for unit in units:
        unit.load()


def save():
    environment = State.meta.get("environment")
    env_mapping = parse_environments(State.config["environments"])
    env = env_mapping[environment]
    visited_units = []
    units = []
    for group in env.groups:
        units.extend(group.get_all_units(visited_units))
    for unit in units:
        unit.save()
