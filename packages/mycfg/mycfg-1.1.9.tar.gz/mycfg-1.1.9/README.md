# MyCfg - A basic dotfiles manager.

### MyCfg is very simple and has few features compared with many other dotfile managers. It is designed for my specific use-case.

## Installation:
`python3 -m pip install mycfg`

## Usage:
### Setup:
- Initialise a dotfiles repository: `mycfg init`
or:
Clone an existing dotfiles repository: `mycfg clone github:pjones123`

- Enter your dotfiles directory: `mycfg cd`
- Customise your config by editing `config.yml`
- Set the environment for your current system: `mycfg set-env <environment>`
- Set the package manager for your current system: `mycfg set-pm <package-manager>`

### Load the saved configuration onto your system: `mycfg load`
### Save your system's configuration to the dotfiles repository: `mycfg save`
### Create a new custom script in `~/.config/mycfg/scripts`: `mycfg mkscript <name>`

## config file:
Your MyCfg configuration exists at `~/.config/mycfg/config.yml`
You can enter this directory with `mycfg cd`

The main objects that can be set in the config file:

- units: These are single, self-contained packages of software.
- groups: These are collections of related units.
- environments: collections of units and groups that make up an entire system environment. Each MyCfg installation can be linked to only one environment.

### configuration file format:
```yaml
units:
    zsh:
        files:
            - .zshrc # file paths are relative to $XDG_HOME
        requires-package: list of required packages. Packages are installed according to the packages section.
        install-command: command to be run once to install
        save-scripts-pre: list of scripts to be run before copying the files, each time a save occurs. Names should be relative to ~/.config/mycfg/scripts
        save-scripts-post: same as save-scripts-pre, but run after files are copied
        load-scripts-pre: same as save-scripts-pre, but run on load
        load-scripts-post: same as load-scripts-post, but run after files are copied

groups:
    shell:
        units: # list of units for this groups
            - zsh
        groups:
            - groups can require other groups

environments:
    desktop: # A complete collection of configurations required for this environments
        units:
            - can require units
        groups: 
            - and groups
        default-package-manager: choose a default package manager for this environment


packages:
    zsh:
        apt: zsh
        pacman: zsh
        default: command to run if no package manager matches

package-managers:
    pacman:
        install: sudo pacman -S
        remove: sudo pacman -R
    apt:
        install: sudo apt install
        remove: sudo apt remove

```

### Example:
An example usage can be found in [my dotfiles repository](https://github.com/pjones123/dotfiles)
