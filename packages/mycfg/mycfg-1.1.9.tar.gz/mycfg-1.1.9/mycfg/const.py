import pathlib
import re

HOME = pathlib.Path.home()
CONFIG_DIR = HOME.joinpath(pathlib.Path(".config"))

MYCFG_CONFIG_DIR = CONFIG_DIR.joinpath(pathlib.Path("mycfg"))
META_FILE = MYCFG_CONFIG_DIR.joinpath(pathlib.Path("meta.json"))
CONFIG_FILE = MYCFG_CONFIG_DIR.joinpath(pathlib.Path("config.yml"))
DOTFILES_SAVE_DIR = MYCFG_CONFIG_DIR.joinpath(pathlib.Path("dotfiles"))
CUSTOM_SCRIPT_DIR = MYCFG_CONFIG_DIR.joinpath(pathlib.Path("scripts"))
BACKUP_DIR = MYCFG_CONFIG_DIR.joinpath(pathlib.Path("backups"))
URL_REGEX = re.compile(
    r"https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*)")

IGNORE_PATTERNS = ['.git']

DEFAULT_CONFIG_CONTENT = {
    "include": "",
    "units": {},
    "groups": {},
    "environments": {},
    "packages": {},
    "package-managers": {},
}

DEFAULT_GIT_IGNORE = ["meta.json", "backups/"]

PATH_VARIABLES = {
    "$HOME": HOME,
    "$MYCFG_CONFIG": MYCFG_CONFIG_DIR,
}
