import tkinter as tk
from pyrustic.view import View
from pyrustic.com import Com
from pyrustic.threadom import Threadom
from primes.view.central_view import CentralView
from primes.view.footer_view import FooterView
from primes.misc.intercom import Intercom
from primes.host.main_host import MainHost


class MainView(View):
    def __init__(self, app):
        super().__init__()
        self._app = app
        self._master = app.root
        self._body = None
        self._com = None
        self._main_host = None
        self._threadom = None
        self._transom = None
        self._setup()

    def _setup(self):
        self._main_host = MainHost()
        self._com = Com(tk=self._master)
        self._threadom = Threadom(self._master)
        self._intercom = Intercom(self._app,
                                  self._com,
                                  self._threadom,
                                  self._main_host)

    def _on_build(self):
        self._body = tk.Frame(self._master)
        # central view
        central_view = CentralView(self._body,
                                   self._com)
        central_view.build_pack(fill=tk.BOTH, expand=1)
        # footer view
        footer_view = FooterView(self._body, self._com)
        footer_view.build_pack(side=tk.BOTTOM, fill=tk.X,
                               padx=2, pady=2)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass
