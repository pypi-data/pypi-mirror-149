import importlib
import os
import pickle
import subprocess
import threading
import tkinter as tk
import webbrowser
from enum import Enum
from functools import partial
from itertools import zip_longest
from tkinter import *
from tkinter import ttk

from lwdia.locale import _
from lwdia.widgets.areabase import AreaBase
from lwdia.widgets.common import get_default_text, get_default_text_menu


class ExampleType(Enum):
    EVENT = 0
    CONTROL = 1
    ACTION = 2
    LOOK = 3
    SOUND = 4
    LISTEN = 5
    CALCULATION = 6
    DRAW = 7
    VARIABLE = 8
    FUNCTION = 9
    MUSIC = 10
    READ = 11
    TRANSLATION = 12


class ExampleArea(AreaBase):
    def __init__(self, win, width=None):
        super().__init__(win, width)
        self.x0 = None
        self.x1 = None
        self.example_text = None
        self.example_text_sbar = None
        self.content_height = 0

    def get_content_height(self, height=0):
        return self.content_height

    def update_example_text(self, _type):
        pass

    def add_widgets(self):
        self.example_text = get_default_text(self.root)
        self.example_text.insert(1.0, "asfhkajsfa\nhslkajkffhjklafLFJKL")
        self.example_text.configure(state="disabled")
        self.example_text_menu = get_default_text_menu(
            self.root, self.example_text
        )

        self.top_btns = [
            ttk.Button(
                self.root,
                text=_("Event"),
                command=lambda: self.update_example_text(ExampleType.EVENT),
            ),
            ttk.Button(
                self.root,
                text=_("Control"),
                command=lambda: self.update_example_text(ExampleType.CONTROL),
            ),
            ttk.Button(
                self.root,
                text=_("Action"),
                command=lambda: self.update_example_text(ExampleType.ACTION),
            ),
            ttk.Button(
                self.root,
                text=_("Look"),
                command=lambda: self.update_example_text(ExampleType.LOOK),
            ),
            ttk.Button(
                self.root,
                text=_("Sound"),
                command=lambda: self.update_example_text(ExampleType.SOUND),
            ),
            ttk.Button(
                self.root,
                text=_("Listen"),
                command=lambda: self.update_example_text(ExampleType.LISTEN),
            ),
            ttk.Button(
                self.root,
                text=_("Calc"),
                command=lambda: self.update_example_text(
                    ExampleType.CALCULATION
                ),
            ),
            ttk.Button(
                self.root,
                text=_("Draw"),
                command=lambda: self.update_example_text(ExampleType.DRAW),
            ),
            ttk.Button(
                self.root,
                text=_("Variable"),
                command=lambda: self.update_example_text(ExampleType.VARIABLE),
            ),
            ttk.Button(
                self.root,
                text=_("Func"),
                command=lambda: self.update_example_text(ExampleType.FUNCTION),
            ),
            ttk.Button(
                self.root,
                text=_("Music"),
                command=lambda: self.update_example_text(ExampleType.MUSIC),
            ),
            ttk.Button(
                self.root,
                text=_("Read"),
                command=lambda: self.update_example_text(ExampleType.READ),
            ),
            ttk.Button(
                self.root,
                text=_("Trans"),
                command=lambda: self.update_example_text(
                    ExampleType.TRANSLATION
                ),
            ),
        ]

    def get_x0(self):
        return 0

    def get_x1(self):
        return self.win.get_w_width(of=3)

    def place(self):
        super().place()
        self.example_text.place(
            x=0,
            y=self.top_btns_height,
            width=self.get_width() - self._scrollbar.winfo_width(),
            height=self.get_scrollbar_height(),
        )

    def config(self):
        super().config()
        self.example_text.config(yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self.example_text.yview)
