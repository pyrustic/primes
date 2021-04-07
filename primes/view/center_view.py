import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from pyrustic.view import View
from primes.misc.events import Events


class CenterView(View):
    def __init__(self, master, com):
        super().__init__()
        self._master = master
        self._com = com
        self._body = None
        self._count = 0
        self._chars_by_line = 0
        self._line_width = 69
        self._setup()

    def display(self, number):
        if number is None:
            self._com.pub(Events.gui_end_displaying)
            return
        self._count += 1
        self._write(number, " ")

    def clear(self):
        self._count = 0
        self._body.config(state="normal")
        self._body.delete("1.0", "end")
        self._body.config(state="disabled")
        self._chars_by_line = 0

    def _setup(self):
        # on host compute prime
        consumer = (lambda event, data, self=self:
                    self.display(data))
        self._com.sub(Events.host_send_prime, consumer)
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
    CenterView(root).build_pack(expand=1, fill=tk.BOTH)
    root.mainloop()
