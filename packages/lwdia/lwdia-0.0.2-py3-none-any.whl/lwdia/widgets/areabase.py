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
from lwdia.widgets.scrollbar import get_default_scrollbar


class AreaBase:
    def __init__(self, win, width=None, set_widgets=True):
        self.win = win
        self.root = self.win.root
        self._width = width or self.win.scr_widthof6
        self._height = self.win.get_height()
        self._scrollbar = None
        self.x0 = 0
        self.x1 = 0
        self.top_btns = []
        self.top_btns_height = 0

        if set_widgets:
            self.set_widgets()

    def place_btns_top_default(self):
        btn_x = self.get_x0()
        btn_y = 0
        all_btns_height = 0
        oneline = True
        for btn in self.top_btns:
            btn_width = btn.winfo_width()
            btn_height = btn.winfo_height()
            if (self.get_x1() - self.get_scrollbar_width()) > (
                btn_x + btn_width
            ):
                btn.place(x=btn_x, y=btn_y)
            else:
                oneline = False
                btn_x = self.get_x0()
                btn_y += btn_height
                btn.place(x=btn_x, y=btn_y)
                all_btns_height = btn_y + btn_height
            btn_x += btn_width
        if oneline:
            first_btn = self.top_btns[0]
            all_btns_height = first_btn.winfo_height()
        self.top_btns_height = all_btns_height

    def set_widgets(self):
        self.set_scrollbar()

    def set_scrollbar(self, sbar=None):
        if sbar:
            self._scrollbar = sbar
            return
        self._scrollbar = get_default_scrollbar(self.root)

    def get_scrollbar_width(self):
        return self._scrollbar.winfo_width()

    def get_width(self):
        return self.get_x1() - self.get_x0()

    def get_width_without_scrollbar(self):
        return self.get_width() - self.get_scrollbar_width()

    def get_height(self):
        return self.win.get_w_height()

    def get_x0(self):
        return self.x0

    def get_x1(self):
        return self.x1

    def add_widgets(self):
        pass

    def get_scrollbar_x(self):
        return self.get_x1() - self.get_scrollbar_width()

    def get_scrollbar_y(self):
        return self.top_btns_height

    def get_scrollbar_height(self):
        return self.get_height() - self.top_btns_height

    def place(self, show_scrollbar=True):
        if len(self.top_btns) > 0:
            self.place_btns_top_default()
        if show_scrollbar:
            self._scrollbar.place(
                x=self.get_scrollbar_x(),
                y=self.get_scrollbar_y(),
                height=self.get_scrollbar_height(),
            )

    def config(self):
        self.place()
