import os

def get_executables_lazy():
	for name in os.listdir('out/Default'):
		path = f'out/Default/{name}'
		if not os.path.isfile(path): continue
		if not os.access(path, os.X_OK): continue

		yield name
def get_executables():
    return list(get_executables_lazy())

def get_configurations():
	return os.listdir('out/')