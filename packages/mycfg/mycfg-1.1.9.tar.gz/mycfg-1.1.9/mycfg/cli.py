import argparse
import os
import pathlib
import shutil
import stat

from mycfg import lib, const, meta
from colorama import Fore

from mycfg.error import PackageManagerError
from mycfg.state import State

SUCCESS = f"{Fore.GREEN}\u2713"
FAILURE = f"{Fore.RED}\u274c"


def set_pm(args):
    meta.set("package_manager", args.pm)
    meta.save()
    print(f"{SUCCESS} Set{Fore.RESET} {args.pm}{Fore.GREEN} as the system package manager")


def add_pm(args):
    meta.append("package_managers", args.pm)
    meta.save()
    print(f"{SUCCESS} Added{Fore.RESET} {args.pm}{Fore.GREEN} as a backup package manager")


def rm_pm(args):
    meta.remove("package_managers", args.pm)
    meta.save()
    print(f"{SUCCESS} Removed{Fore.RESET} {args.pm}{Fore.GREEN} as a backup package manager")


def set_env(args):
    meta.set("environment", args.env)
    meta.save()
    print(f"{SUCCESS} Set{Fore.RESET} {args.env}{Fore.GREEN} as the system environment")


def load(args):
    if meta.get("environment") not in State.config.get("environments", {}):
        return print(f"{FAILURE} Invalid environment set")
    try:
        lib.load()
    except PackageManagerError as e:
        if e.not_set:
            print(
                f"{FAILURE} No package manager set. Choose a package manager with{Fore.RESET} mycfg set-pm <package-manager>")
        elif e.missing_command:
            print(
                f"{FAILURE} Selected package manager missing {e.missing_command} command. Set it in the config file.{Fore.RESET}")
        elif e.missing_package:
            print(
                f"{FAILURE} No entry for package {Fore.RESET} {e.missing_package}{Fore.RED}. Set it in the config file.{Fore.RESET}")
    print(f"{SUCCESS} Loaded Configuration!{Fore.RESET}")


def save(args):
    if meta.get("environment") not in State.config.get("environments", {}):
        return print(f"{FAILURE} Invalid environment set")
    lib.save()
    print(f"{SUCCESS} Saved configuration!{Fore.RESET}")


def clone(args):
    url = lib.get_repo_url(args.repo)
    if url is None:
        return print(f"{FAILURE} Invalid URL{Fore.RESET}")
    shutil.rmtree(const.MYCFG_CONFIG_DIR)
    if lib.sh(f"git clone {url} {const.MYCFG_CONFIG_DIR.resolve()}") == 0:
        print(f"{SUCCESS} Cloned dotfiles repository!{Fore.RESET}")

def backup(args):
    dir = const.BACKUP_DIR.joinpath(args.name)
    shutil.copytree(const.DOTFILES_SAVE_DIR, dir)
    print(f"{SUCCESS} Saved backup to ${dir.relative_to(const.HOME)}{Fore.RESET}")

def init(args):
    lib.write_file(const.MYCFG_CONFIG_DIR.joinpath(".gitignore"), "\n".join(const.DEFAULT_GIT_IGNORE))
    lib.sh(f"git init {const.MYCFG_CONFIG_DIR.resolve()}")
    print(f"{SUCCESS} Initialised empty repository!{Fore.RESET}")


def cd(args):
    os.chdir(const.MYCFG_CONFIG_DIR)
    lib.sh(os.environ["SHELL"])


def mkscript(args):
    path = const.CUSTOM_SCRIPT_DIR.joinpath(pathlib.Path(args.name))
    path.touch()
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    print(f"{SUCCESS} Created script {Fore.RESET}{args.name}")


parser = argparse.ArgumentParser()
sub_parser = parser.add_subparsers()

load_parser = sub_parser.add_parser("load", help="Load the saved configuration onto your system")
load_parser.set_defaults(func=load)

save_parser = sub_parser.add_parser("save", help="Save your system's configuration to the repo")
save_parser.set_defaults(func=save)

clone_parser = sub_parser.add_parser("clone", help="Clone a dotfiles repository. Overwrites existing repoistory.")
clone_parser.add_argument("repo", type=str)
clone_parser.set_defaults(func=clone)

backup_parser = sub_parser.add_parser("backup", help="Back Up dotfiles directory")
backup_parser.add_argument("name", type=str)
backup_parser.set_defaults(func=backup)

init_parser = sub_parser.add_parser("init", help="Initialise mycfg")
init_parser.set_defaults(func=init)

set_pm_parser = sub_parser.add_parser("set-pm", help="Set the package manager to use on the current system")
set_pm_parser.add_argument("pm", type=str)
set_pm_parser.set_defaults(func=set_pm)

add_pm_parser = sub_parser.add_parser("add-pm", help="Add a backup package manager")
add_pm_parser.add_argument("pm", type=str)
add_pm_parser.set_defaults(func=add_pm)

rm_pm_parser = sub_parser.add_parser("rm-pm", help="Remove a backup package manager")
rm_pm_parser.add_argument("pm", type=str)
rm_pm_parser.set_defaults(func=rm_pm)

set_env_parser = sub_parser.add_parser("set-env", help="Set the environment of the current system")
set_env_parser.add_argument("env", type=str)
set_env_parser.set_defaults(func=set_env)

cd_parser = sub_parser.add_parser("cd",
                                  help="cd to the configuration directory. Spawns a new shell in the target directory.")
cd_parser.set_defaults(func=cd)

mk_script_parser = sub_parser.add_parser("mkscript", help="Create a custom script")
mk_script_parser.add_argument("name")
mk_script_parser.set_defaults(func=mkscript)


def main():
    lib.ensure_config_files()
    lib.load_config_file()
    meta.load_meta()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
