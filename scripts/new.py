import os

def newest(path):

    files = os.listdir(path)

    paths = [os.path.join(path, basename) for basename in files]

    return max(paths, key=os.path.getctime)