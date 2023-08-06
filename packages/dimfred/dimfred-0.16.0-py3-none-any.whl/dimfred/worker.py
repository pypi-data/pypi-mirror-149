import threading as th


class Queue(list):
    def __init__(self):
        super().__init__()
        self._notify = th.Condition()

    def wait(self):
        with self._notify:
            self._notify.wait()

    def append(self, value):
        super().append(value)
        with self._notify:
            self._notify.notify()


class Worker(th.Thread):
    def __init__(self, name="Worker"):
        self._queue = Queue()
        super().__init__(name=name, target=self._task)
        self.start()

    def add(self, action, *args, **kwargs):
        self._queue.append((action, args, kwargs))

    def _task(self):
        while True:
            if not self._queue:
                self._queue.wait()

            action, args, kwargs = self._queue.pop(0)
            action(*args, **kwargs)
