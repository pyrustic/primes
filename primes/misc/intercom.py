from primes.misc.events import Events


class Intercom:
    def __init__(self, app, com, threadom, host):
        self._app = app
        self._com = com
        self._threadom = threadom
        self._host = host
        self._qid = None
        self._setup()

    def _setup(self):
        self._com.sub(None, consumer=self._dispatch)

    def _dispatch(self, sequence, data):
        sequences = \
            {
                Events.user_submit_number: self._on_user_submit_number,
                Events.gui_stop_displaying: self._on_gui_stop_displaying,
                Events.user_click_stop: self._on_user_click_stop,
                Events.user_click_exit: self._on_user_click_exit
            }
        handler = sequences.get(sequence, None)
        if handler:
            handler(data)

    def _on_user_submit_number(self, data):
        queue = self._threadom.q()
        target = self._host.compute
        target_args = (data, queue)
        # run computation in a new thread
        consumer = (lambda data, self=self:
                        self._com.pub(Events.host_stop_computation, data))
        self._threadom.run(target, target_args=target_args,
                           consumer=consumer)
        # consume the data pushed into the queue by the computation thread
        consumer = (lambda data, self=self:
                        self._com.pub(Events.host_compute_prime, data))
        self._qid = self._threadom.consume(queue, consumer=consumer)

    def _on_gui_stop_displaying(self, data):
        self._threadom.stop(self._qid)
        self._qid = None

    def _on_user_click_stop(self, data):
        self._host.stop()

    def _on_user_click_exit(self, data):
        self._app.exit()
