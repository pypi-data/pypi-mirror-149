import importlib
import os

project_path = os.path.abspath(os.path.dirname(__file__))


def spend():
    from lwdia import ready

    ready.go()
    pass
