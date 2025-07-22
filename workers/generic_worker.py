from typing import Callable, Any
from PySide6.QtCore import QObject, Signal, QRunnable


class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)


class GenericWorker(QRunnable):
    def __init__(self, fn: Callable[..., Any], *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
