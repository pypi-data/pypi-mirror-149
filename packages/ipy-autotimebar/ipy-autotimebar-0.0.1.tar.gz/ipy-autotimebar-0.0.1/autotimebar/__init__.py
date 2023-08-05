from __future__ import print_function

from ._version import version as __version__

from time import strftime, localtime
import threading
import time
import ipywidgets as widgets
from time import monotonic
from IPython.core.magics.execution import _format_time as format_delta
from IPython.display import display

try:
    from time import monotonic
except ImportError:
    from monotonic import monotonic


def format_timestamp(struct_time):
    timestamp = strftime('%Y-%m-%d %H:%M:%S %z', struct_time)
    # add colon in %z (for datetime.fromisoformat, stackoverflow.com/q/44836581)
    return '{}:{}'.format(timestamp[:-2], timestamp[-2:])


class LineWatcher:
    """Class that implements a time depends on if you use ipython or jupyter notebooks.

    Notes
    -----
    * Register the `start` and `stop` methods with the IPython events API.
    """
    __slots__ = ['start_time', 'timestamp', 'finished', 'timebar', 'thread', 'if_notebook']

    @staticmethod
    def in_notebook():
        """Check checking if the library is used in jupyter notebook"""
        try:
            from IPython import get_ipython
            if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
                return False
        except ImportError:
            return False
        except AttributeError:
            return False
        return True

    def start(self):
        self.timestamp = localtime()
        self.start_time = monotonic()
        self.if_notebook = self.in_notebook()
        self.finished = False
        if self.if_notebook:
            self.timebar = widgets.Label(value='0s')
            self.thread = threading.Thread(target=self.update_timebar)
            display(self.timebar)
            self.thread.start()

    def update_timebar(self):
        """Update Label time bar until cell end."""
        while self.finished == False:
            time.sleep(0.01)
            current = monotonic()
            self.timebar.value = f"time: {format_delta(current - self.start_time)}"

    def stop(self):
        delta = monotonic() - self.start_time
        self.finished = True
        time.sleep(0.01)
        result = f'time: {format_delta(delta)} (started: {format_timestamp(self.timestamp)})'
        if self.if_notebook:
            self.timebar.value = result
            return
        print(result)


timer = LineWatcher()
start = timer.start
stop = timer.stop


def load_ipython_extension(ip):
    start()
    ip.events.register('pre_run_cell', start)
    ip.events.register('post_run_cell', stop)


def unload_ipython_extension(ip):
    ip.events.unregister('pre_run_cell', start)
    ip.events.unregister('post_run_cell', stop)

