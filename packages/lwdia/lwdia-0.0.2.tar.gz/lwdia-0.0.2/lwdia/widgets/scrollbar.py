import importlib
import os
import pickle
import subprocess
import threading
import tkinter as tk
import webbrowser
from functools import partial
from itertools import zip_longest
from tkinter import *
from tkinter import ttk

from lwdia.locale import _
from lwdia.settings import *


def get_default_scrollbar(root):
    return Scrollbar(
        root,
        orient=VERTICAL,
    )
