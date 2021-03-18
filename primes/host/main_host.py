import time


class MainHost:
    def __init__(self):
        self._cache = True
        self._processing = False

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, val):
        self._cache = val

    def compute(self, number, queue):
        if self._processing:
            return
        self._processing = True
        count = 0
        for prime in self._primes_generator(number):
            count += 1
            if not self._processing:
                self._stop_computation(queue)
                return False
            queue.put(prime)
            time.sleep(0.01)
        self._stop_computation(queue)
        return True

    def stop(self):
        self._processing = False

    def _primes_generator(self, number):
        for num in range(number + 1):
            if num <= 1:
                continue
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                yield num

    def _stop_computation(self, queue):
        queue.put(None)
        self._processing = False
