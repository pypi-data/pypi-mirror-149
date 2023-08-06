"""
Colored terminal/console output.

Ref:
--------
https://stackabuse.com/how-to-print-colored-text-in-python/
"""

import sys
from datetime import datetime
from enum import IntEnum
from typing import Literal


class Style(IntEnum):
    """Text style."""
    NORMAL = 0
    BOLD = 1
    LIGHT = 2
    ITALICIZED = 3
    UNDERLINED = 4
    BLINK = 5


class TextColor(IntEnum):
    """Text color."""
    UNSET = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37


class BgColor(IntEnum):
    """Background color."""
    UNSET = 0
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47


_RESET = '\033[0m'
_TO = Literal['stdout', 'stderr']


class ColoredConsole:
    """Colored console output."""

    @staticmethod
    def set(style: Style = Style.NORMAL, color: TextColor = TextColor.UNSET, bg: BgColor = BgColor.UNSET, to: _TO = 'stdout'):
        """
        Set color. Should call :method:`unset` manually to recover.

        Ref
        ------
        * \\033[<style>;<color>;<bg>m
        * \\033[<style>;<color>m (bg==BgColor.UNSET)
        """
        std = sys.stdout if to == 'stdout' else sys.stderr
        vs = [style.value, color.value, bg.value]
        # the last one cannot be 0
        for i in range(len(vs)-1, -1, -1):
            if vs[i] != 0:
                break
            if vs[i] == 0:
                vs.pop(i)
        std.write(f'\033[{";".join([str(i) for i in vs])}m')

    @staticmethod
    def unset(to: _TO = 'stdout'):
        """Recover console settings."""
        std = sys.stdout if to == 'stdout' else sys.stderr
        std.write(_RESET)

    @staticmethod
    def print(info: str, prefix: str = '', style: Style = Style.NORMAL, color: TextColor = TextColor.UNSET, bg: BgColor = BgColor.UNSET, to: _TO = 'stdout'):
        ColoredConsole.set(style, color, bg, to)
        std = sys.stdout if to == 'stdout' else sys.stderr
        std.write(f'{prefix}{info}')
        ColoredConsole.unset(to)
        std.write('\n')

    @staticmethod
    def debug(info: str, prefix=f'DEBUG{datetime.now().isoformat()}: ',):
        ColoredConsole.print(info, prefix, style=Style.LIGHT)

    @staticmethod
    def info(info):
        """Normal colored information."""
        print(info)

    @staticmethod
    def success(info, emoji: str = '✅ '):
        ColoredConsole.print(info, emoji if emoji else '',
                             color=TextColor.GREEN)

    @staticmethod
    def warn(info, emoji: str = '⚠️  '):
        ColoredConsole.print(info, emoji if emoji else '',
                             color=TextColor.YELLOW)

    @staticmethod
    def error(info, emoji: str = '❌ '):
        ColoredConsole.print(info, emoji if emoji else '',
                             color=TextColor.RED, to='stderr')


if __name__ == '__main__':
    ColoredConsole.debug('This is a debug.')
    ColoredConsole.success('This is a success.')
    ColoredConsole.warn('This is a warning.')
    ColoredConsole.error('This is a error.')
