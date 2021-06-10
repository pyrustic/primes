import tkinter as tk
from viewable import Viewable
from diaspora import Diaspora
from primes.view.top_view import TopView
from primes.view.center_view import CenterView
from primes.view.bottom_view import BottomView
from primes.host.main_host import MainHost


class MainView(Viewable):
    def __init__(self, app):
        super().__init__()
        self._app = app
        self._master = app.root
        self._body = None
        self._com = None
        self._main_host = None
        self._setup()

    def _setup(self):
        self._com = Diaspora(tk=self._master)
        self._main_host = MainHost(self._app, self._com)

    def _build(self):
        self._body = tk.Frame(self._master)
        # top view
        top_view = TopView(self._body, self._com)
        top_view.build_pack(anchor="w", padx=2, pady=2)
        # center view
        center_view = CenterView(self._body, self._com)
        center_view.build_pack(fill=tk.BOTH, expand=1)
        # footer view
        bottom_view = BottomView(self._body, self._com)
        bottom_view.build_pack(fill=tk.X, padx=2, pady=2)
