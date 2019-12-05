#!/usr/bin/python3.6

import argparse
import argcomplete
import sys
import os
from utils import get_installation_folder   

def get_runnable_scripts():
    return [file for file in os.listdir(get_installation_folder()) if not '.' in file and os.path.isfile(file)]

def make_scripts_executable():
    folder = get_installation_folder()
    for name in os.listdir(folder):
        path = os.path.join(folder, name)

        if '.' in name: continue
        if os.path.isdir(path): continue

        if os.access(path, os.X_OK): continue

        print("Making", name, "executable")
        os.system(f'chmod +x {name}')
        print("Done!")

def install_startup_tasks(args):
    # Add goma to startup.
    os.system(f'ln -s ./start_goma {os.getenv("HOME")}/.config/autostart-scripts/start_goma')

def install_tasks():
    # Every day, update the compile commands.
    os.system('(crontab -l 2>/dev/null; echo "0 0 * * * update-compile-commands") | crontab -')

def install_completions(args):
    bash_config = ''
    with open(args.bash_config) as f:
        bash_config = f.read()

    print("Updating script completions file...")
    scripts = get_runnable_scripts()
    with open(args.completions_file, 'w') as f:
        f.write('#!bin/bash')
        for script in scripts:
            f.write(f'eval "$(register-python-argcomplete {script})"\n')
    print("Updated!")

    include = f'source {args.completions_file}'
    if not include in bash_config:
        print("Adding completions to bash")
        with open(args.bash_config, 'a+') as f:
            f.write(f'\n#Install chromium tools auto completions\n{include}\n')
        print("Added!")
    os.system(include) # Update completions for current shell


def install_scripts(args):
    folder = get_installation_folder()

    path = os.environ['PATH']
    if folder in path:
        print("Scripts already in path!")
        return

    export = f'export PATH="$PATH:{folder}"'
    with open(args.bash_config, 'a+') as f:
        f.write(f'\n#Add chromium tools to path\n{export}\n')

    os.system(export) # Add to current shell
    print(f'Added {folder} to $PATH')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Install Chromium Scripts.")

    parser.add_argument('--no-completions', action='store_true')
    parser.add_argument('--bash-config', default=os.path.join(os.getenv('HOME'), '.bashrc'))
    parser.add_argument('--completions-file', default=f'{get_installation_folder()}/.bash_completions')

    argcomplete.autocomplete(parser)
    args = parser.parse_args(sys.argv[1:])

    install_scripts(args)
    make_scripts_executable()
    install_completions(args)
    install_tasks()

    if not args.no_completions:
        install_completions(args)

