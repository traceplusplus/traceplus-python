import os

def environ_as_bool(name, default=False):
    flag = os.environ.get(name, default)
    if default is None or default:
        try:
            flag = not flag.lower() in ['off', 'false', '0']
        except AttributeError:
            pass
    else:
        try:
            flag = flag.lower() in ['on', 'true', '1']
        except AttributeError:
            pass
    return flag

