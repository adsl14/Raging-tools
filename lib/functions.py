from lib.packages import os, stat


def del_rw(name_method, path, error):
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)

    return name_method, error
