import os
from pathlib import Path
from functools import cached_property


class UniqueWorker:
    def __init__(self, path):
        self.path = Path(path)
        self.id = str(os.getpid())
        self._set_id()

    def _set_id(self):
        self.path.parents[0].mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

        with open(self.path, "w") as f:
            f.write(self.id)

    @cached_property
    def is_assiged(self):
        with open(self.path, "r") as f:
            assigned_worker = f.read()

        return assigned_worker == self.id


def by_one_worker(worker_pid_path):
    unique_worker = UniqueWorker(worker_pid_path)

    def deco(f):
        def wrapped(*args, **kwargs):
            if not unique_worker.is_assiged:
                return

            return f(*args, **kwargs)

        return wrapped

    return deco

