import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from pyrustic.view import View
from primes.misc.events import Events


class CentralView(View):
    def __init__(self, master, com=None):
        super().__init__()
        self._master = master
        self._com = com
        self._body = None
        self._count = 0
        self._computation_ended = tk.BooleanVar(value=False)
        self._computation_is_success = False
        self._chars_by_line = 0
        self._line_width = 69
        self._setup()

    def display(self, number):
        if number is None:
            if self._computation_ended.get() is False:
                self._body.wait_variable(self._computation_ended)
            if self._computation_is_success is True:
                cache = ("Successfully generated",
                         "{}".format(self._count),
                         "prime{}".format("s" if self._count > 1 else ""))
                message = " ".join(cache)
            elif self._computation_is_success is False:
                message = "Generation interrupted"
            else:
                message = "An error occurred !"
            self._write("\n\n", message)
            self._com.pub(Events.gui_stop_displaying)
            return
        self._count += 1
        self._write(number, " ")

    def stop(self, happy_end):
        self._computation_is_success = happy_end
        self._computation_ended.set(True)

    def clear(self):
        self._count = 0
        self._computation_ended.set(False)
        self._computation_is_success = None
        self._body.config(state="normal")
        self._body.delete("1.0", "end")
        self._body.config(state="disabled")
        self._chars_by_line = 0

    def _setup(self):
        if not self._com:
            return
        # on host compute prime
        consumer = (lambda event, data, self=self:
                    self.display(data))
        self._com.sub(Events.host_compute_prime, consumer)
        # on host end computation
        consumer = (lambda event, data, self=self:
                    self.stop(data))
        self._com.sub(Events.host_stop_computation, consumer)
        # on user click clear
        consumer = (lambda event, data, self=self:
                    self.clear())
        self._com.sub(Events.user_click_clear, consumer)

    def _on_build(self):
        self._body = ScrolledText(self._master,
                                  wrap="word",
                                  width=self._line_width,
                                  height=18,
                                  padx=10, pady=10,
                                  state="disabled")

    def _on_display(self):
        pass

    def _on_destroy(self):
        pass

    def _write(self, *text):
        self._body.config(state="normal")
        for item in text:
            item = str(item)
            self._insert_breakline(self._body, item)
            self._body.insert("end", item)
        self._body.config(state="disabled")
        self._body.yview_moveto(1.0)

    def _insert_breakline(self, widget, word):
        len_word = len(word)
        if len_word + self._chars_by_line > self._line_width:
            widget.insert("end", "\n")
            self._chars_by_line = len_word
        else:
            self._chars_by_line += len_word

if __name__ == "__main__":
    root = tk.Tk()
    CentralView(root).build_pack(expand=1, fill=tk.BOTH)
    root.mainloop()
