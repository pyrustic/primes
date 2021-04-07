from pyrustic.threadom import Threadom
from primes.misc.events import Events
from primes.core.primes_generator import PrimesGenerator


class MainHost:

    def __init__(self, app, com):
        self._app = app
        self._com = com
        self._threadom = Threadom(self._app.root)
        self._primes_generator = PrimesGenerator()
        self._qid = None
        self._setup()

    def _setup(self):
        self._com.event_handler(self)

    def _on_user_submit_number(self, event, data):
        queue = self._threadom.q()
        target = self._primes_generator.compute
        target_args = (data, queue)
        # run computation in a new thread
        consumer = (lambda data, self=self:
                        self._com.pub(Events.core_end_computation, data))
        self._threadom.run(target, target_args=target_args,
                           consumer=consumer)
        # consume the data pushed into the queue by the computation thread
        consumer = (lambda data, self=self:
                        self._com.pub(Events.host_send_prime, data))
        self._qid = self._threadom.consume(queue, consumer=consumer)

    def _on_gui_end_displaying(self, event, data):
        self._threadom.stop(self._qid)
        self._qid = None

    def _on_user_click_stop(self, event, data):
        self._primes_generator.stop()

    def _on_user_click_exit(self, event, data):
        self._app.exit()
