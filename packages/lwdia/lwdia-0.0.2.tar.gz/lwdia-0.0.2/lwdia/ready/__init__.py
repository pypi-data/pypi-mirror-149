import importlib
import os
import pickle
import subprocess
import threading
import webbrowser
from functools import partial
from itertools import zip_longest

from lwdia.locale import _
from lwdia.widgets.mainwindow import MainWindow


def go():
    MainWindow().mainloop()
    pass
