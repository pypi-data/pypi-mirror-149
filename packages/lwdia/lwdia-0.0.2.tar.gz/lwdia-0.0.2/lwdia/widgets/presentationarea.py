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
from lwdia.widgets.areabase import AreaBase


class PresentationArea(AreaBase):
    def __init__(self, win, width=None):
        super().__init__(win, width)
        self.x0 = 2 * self._width
        self.x1 = 3 * self._width

    def get_x0(self):
        return 2 * self.win.get_w_width(of=3)

    def get_x1(self):
        return 3 * self.win.get_w_width(of=3)

    def place(self):
        super().place()
