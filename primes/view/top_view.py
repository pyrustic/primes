import tkinter as tk
from pyrustic.view import View
from primes.misc.events import Events


class TopView(View):

    def __init__(self, master, com):
        super().__init__()
        self._master = master
        self._com = com
        self._body = None
        self._strvar = tk.StringVar(value="Welcome friend !")
        self._computation_ended = tk.BooleanVar(value=False)
        self._count = 0
        self._computation_is_success = False
        self._setup()

    def _setup(self):
        # on host compute prime
        consumer = (lambda event, data, self=self:
                    self._on_host_compute_prime(data))
        self._com.sub(Events.host_send_prime, consumer)
        # on core end computation
        consumer = (lambda event, data, self=self:
                    self._on_core_end_computation(data))
        self._com.sub(Events.core_end_computation, consumer)
        # on gui end displaying
        consumer = (lambda event, data, self=self:
                    self._on_gui_end_display())
        self._com.sub(Events.gui_end_displaying, consumer)
        # on user click clear
        consumer = (lambda event, data, self=self:
                    self._on_user_click_clear())
        self._com.sub(Events.user_click_clear, consumer)

    def _on_build(self):
        self._body = tk.Label(self._master,
                              textvariable=self._strvar)

    def _on_host_compute_prime(self, data):
        if data is None:
            return
        self._count += 1
        text = "Processing... {} prime{}"
        text = text.format(self._count, "s" if self._count > 1 else "")
        self._strvar.set(text)

    def _on_core_end_computation(self, happy_end):
        self._computation_is_success = happy_end
        self._computation_ended.set(True)

    def _on_gui_end_display(self):
        if self._computation_ended.get() is False:
            self._body.wait_variable(self._computation_ended)
        if self._computation_is_success is True:
            cache = ("Successfully generated",
                     "{}".format(self._count),
                     "prime{} !".format("s" if self._count > 1 else ""))
            message = " ".join(cache)
        elif self._computation_is_success is False:
            message = "Generation interrupted"
        else:
            message = "An error occurred !"
        self._strvar.set(message)

    def _on_user_click_clear(self):
        self._count = 0
        self._strvar.set("")
        self._computation_ended.set(False)
        self._computation_is_success = None
