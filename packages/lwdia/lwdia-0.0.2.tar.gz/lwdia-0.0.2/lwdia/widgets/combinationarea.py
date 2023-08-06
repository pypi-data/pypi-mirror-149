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
from lwdia.widgets.common import get_default_text, get_default_text_menu


class CombinationArea(AreaBase):
    def __init__(self, win, width=None):
        super().__init__(win, width)
        self.x0 = self._width
        self.x1 = 2 * self._width

    def combination_text_bind_tab(self, event):
        self.combination_text.insert(
            self.combination_text.index(tk.INSERT), 4 * " "
        )
        return "break"

    def add_widgets(self):
        self.top_btns = [
            ttk.Button(self.root, text=_("Run")),
            ttk.Button(self.root, text=_("Refresh")),
        ]
        self.combination_text = get_default_text(self.root)
        self.combination_text.bind("<Tab>", self.combination_text_bind_tab)
        self.combination_text_menu = get_default_text_menu(
            self.root, self.combination_text
        )

    def get_x0(self):
        return self.win.get_w_width(of=3)

    def get_x1(self):
        return 2 * self.win.get_w_width(of=3)

    def place(self):
        super().place()
        self.combination_text.place(
            x=self.get_x0(),
            y=self.top_btns_height,
            width=self.get_width_without_scrollbar(),
            height=self.get_scrollbar_height(),
        )

        self.combination_text.config(yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self.combination_text.yview)
