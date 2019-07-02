import os
import json

def get_installation_folder():
    return os.path.dirname(os.path.realpath(__file__))

def get_executables_lazy(configuration):
    if not configuration: configuration = 'Default'

    folder_path = f'out/{configuration}'
    if not os.path.exists(folder_path): return ['chrome']

    for name in os.listdir(folder_path):
        path = f'{folder_path}/{name}'
        if not os.path.isfile(path):
            continue
        if not os.access(path, os.X_OK): continue

        yield name


def get_executables(configuration=None):
    return list(get_executables_lazy(configuration))


def get_configurations():
    if not os.path.exists('out/'):
        return ['Default']

    return os.listdir('out/')


def load_config():
    config_path = os.path.join(get_installation_folder(), 'config.json')
    with open(config_path) as f:
        json_string = f.read()
        return json.loads(json_string)
