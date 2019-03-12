import os
import json

def get_installation_folder():
    return os.path.dirname(os.path.realpath(__file__))

def get_executables_lazy():
    if not os.path.exists('out/Default'): return ['chrome']

    for name in os.listdir('out/Default'):
        path = f'out/Default/{name}'
        if not os.path.isfile(path):
            continue
        if not os.access(path, os.X_OK): continue

        yield name


def get_executables():
    return list(get_executables_lazy())


def get_configurations():
    if not os.path.exists('out/'):
        return ['Default']

    return os.listdir('out/')


def load_config():
    config_path = os.path.join(get_installation_folder(), 'config.json')
    with open(config_path) as f:
        json_string = f.read()
        return json.loads(json_string)
