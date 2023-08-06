import sys
from os import path

this_dir = path.abspath(path.join(path.dirname("__file__")))
api_dir = path.abspath(path.join(path.dirname("__file__"),   'eisenradio/api'))
home_dir = path.abspath(path.join(path.dirname("__file__"),  'eisenradio/eisenhome'))
utils_dir = path.abspath(path.join(path.dirname("__file__"), 'eisenradio/eisenutils'))
instance_dir = path.abspath(path.join(path.dirname("__file__"), 'eisenradio/instance'))
lib_dir = path.abspath(path.join(path.dirname("__file__"),   'eisenradio/lib'))
sys.path.append(path.abspath(this_dir))
sys.path.append(path.abspath(api_dir))
sys.path.append(path.abspath(home_dir))
sys.path.append(path.abspath(utils_dir))
sys.path.append(path.abspath(instance_dir))
sys.path.append(path.abspath(lib_dir))

from eisenradio import create_app_dev
port = 6060


def wsgi_app_dev(a_port):
    """
    DEV
    app.py imports this def; can create multiple instances of flask app on various ports
    tell flask app the port num, so all functions are happy
    """
    app = create_app_dev(a_port)
    # app = create_app_dev(a_port, 'test')    # recreates a test db on each app start
    return app


if __name__ == "__main__":
    wsgi_app_dev(port).run(host='localhost', port=port)
