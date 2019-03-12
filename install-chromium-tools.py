#!/usr/bin/python3.6

import argparse
import argcomplete
import sys
import os

def get_folder():
    return os.path.dirname(os.path.realpath(__file__))

def get_runnable_scripts():
    os.listdir(get_folder())

    return [file for file in os.listdir(get_folder()) if not '.' in file and os.path.isfile(file)]

def make_scripts_executable():
    folder = get_folder()
    for name in os.listdir(folder):
        path = os.path.join(folder, name)

        if '.' in name: continue
        if os.path.isdir(path): continue

        if os.access(path, os.X_OK): continue

        print("Making", name, "executable")
        os.system(f'chmod +x {name}')
        print("Done!")


def install_completions(args):
    bash_config = ''
    with open(args.bash_config) as f:
        bash_config = f.read()

    print("Updating script completions file...")
    scripts = get_runnable_scripts()
    with open(args.completions_file, 'w') as f:
        for script in scripts:
            f.write(f'eval "$(register-python-argcomplete {script})"\n')
    print("Updated!")
    
    include = f'source {args.completions_file}'
    if not include in bash_config:
        print("Adding completions to bash")
        with open(args.bash_config, 'a+') as f:
            f.write(f'\n#Install chromium tools auto completions\n{include}\n')
        print("Added!")


def install_scripts(args):
    folder = get_folder()

    path = os.environ['PATH']
    if folder in path:
        print("Scripts already in path!")
        return

    with open(args.bash_config, 'a+') as f:
        f.write(f'\n#Add chromium tools to path\nexport PATH="$PATH:{folder}"\n')

    print(f'Added {folder} to $PATH')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Install Chromium Scripts.")

    parser.add_argument('--no-completions', action='store_true')
    parser.add_argument('--bash-config', default=os.path.join(os.getenv('HOME'), '.bashrc'))
    parser.add_argument('--completions-file', default=f'{get_folder()}/.bash_completions')

    argcomplete.autocomplete(parser)
    args = parser.parse_args(sys.argv[1:])

    install_scripts(args)
    make_scripts_executable()

    if not args.no_completions:
        install_completions(args)

