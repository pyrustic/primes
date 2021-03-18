import tkinter as tk
from pyrustic.view import View
from pyrustic.widget.toast import Toast
from pyrustic.widget.confirm import Confirm
from primes.misc.events import Events

class FooterView(View):
    def __init__(self, master, com=None):
        super().__init__()
        self._master = master
        self._com = com
        self._body = None
        self._button_start = None
        self._strvar_button = tk.StringVar(value="Start")
        self._strvar_number = tk.StringVar()
        self._entry_number = None
        self._toast = None
        self._setup()

    def _setup(self):
        consumer = lambda event, data, self=self: self._set_button_clear()
        self._com.sub(Events.gui_stop_displaying, consumer)

    def _on_build(self):
        self._body = tk.Frame(self._master)
        # footer left
        footer_left = self._layout_footer_left(self._body)
        footer_left.pack(side=tk.LEFT)
        # footer right
        footer_right = self._layout_footer_right(self._body)
        footer_right.pack(side=tk.RIGHT)

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _layout_footer_left(self, master):
        frame = tk.Frame(master)
        # entry number
        self._entry_number = tk.Entry(frame,
                                width=20,
                                textvariable=self._strvar_number)
        self._entry_number.pack(side=tk.LEFT)
        handler = lambda event: self._on_click_start()
        self._entry_number.focus_set()
        # button start/stop/clear
        self._button_start = tk.Button(frame,
                                 textvariable=self._strvar_button,
                                 command=self._on_click_start)
        self._button_start.pack(side=tk.LEFT, padx=2)
        return frame

    def _layout_footer_right(self, master):
        button_exit = tk.Button(master,
                                text="Exit",
                                command=self._on_click_exit)
        button_exit.pack()
        return button_exit

    def _on_click_start(self):
        number = self._check_number()
        if not number:
            self._strvar_number.set("")
            return
        if not self._com:
            return
        self._entry_number.config(state="readonly")
        self._set_button_stop()
        self._com.pub(Events.user_submit_number, number)

    def _on_click_stop(self):
        self._button_start.config(state="disabled")
        self._toast = Toast(self._body, message="Wait...",
                            duration=None)
        self._com.pub(Events.user_click_stop)

    def _on_click_clear(self):
        self._entry_number.config(state="normal")
        self._strvar_number.set("")
        self._com.pub(Events.user_click_clear)
        self._set_button_start()

    def _on_click_exit(self):
        message = "\nLeaving this cool app...\n"
        confirm = Confirm(self._body, title="Confirmation",
                          message=message)
        confirm.wait_window()
        if confirm.ok:
            self._com.pub(Events.user_click_exit)

    def _check_number(self):
        number = self._strvar_number.get()
        try:
            number = int(number)
        except Exception:
            message = "Only digit is allowed"
            Toast(self._body, message=message)
            number = None
        if number is not None and number <= 1:
            message = "Please enter a greater number"
            Toast(self._body, message=message)
            number = None
        return number

    def _set_button_start(self):
        self._strvar_button.set("Start")
        self._button_start.config(command=self._on_click_start)

    def _set_button_stop(self):
        self._strvar_button.set("Stop")
        self._button_start.config(command=self._on_click_stop)

    def _set_button_clear(self):
        if self._toast:
            self._toast.destroy()
            self._toast = None
        self._strvar_button.set("Clear")
        self._button_start.config(state="normal",
                                  command=self._on_click_clear)


if __name__ == "__main__":
    root = tk.Tk()
    FooterView(root).build_pack(fill=tk.X)
    root.mainloop()
