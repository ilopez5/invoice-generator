#!/bin/python3
import time

# colors
_blue   = '\033[38;5;39m'
_yellow = '\033[38;5;226m'
_white  = '\033[m'

class ProgressBar():
    def __init__(self, width=30, pad=30, color=True):
        self.label     = str()
        self.stages    = 0
        self._progress = 0
        self._width    = width
        self._pad      = pad
        self._start    = time.perf_counter()
        self._current  = self._start
        self._color    = color

    def begin(self, label, stages):
        # reset if past usage was incomplete
        if self._progress:
            self.end()
        self.label  = label
        self.stages = stages
        print(self, end='\r')

    def checkpoint(self):
        assert(self.stages > 0)
        assert(self._progress < self.stages)
        self._current = time.perf_counter()
        self._progress += 1
        print(self, end="\r" if self._progress < self.stages else '')

    def end(self):
        self.label     = str()
        self.stages    = 0
        self._progress = 0
        self._start    = time.perf_counter()
        self._current  = self._start
        print()

    def _get_label(self):
        if self._color:
            return _yellow + self.label + _white
        return self.label

    def _get_bar(self, size):
        if self._color:
            return _blue + '#'*size + _white
        return '#'*size

    def __str__(self):
        # determine chunk size
        length = self._width // self.stages
        if self._width % self.stages != 0:
            length += 1
        
        # determine final size for bar
        size    = min(self._progress * length, self._width)
        prefix  = self._get_label() + '.' * (self._pad - len(self.label))
        used    = self._get_bar(size)
        free    = ' ' * (self._width - size)
        elapsed = round(self._current - self._start, 2)
        return f"{prefix}[{used}{free}] {elapsed:.2f}s"

if __name__ == '__main__':
    pass
