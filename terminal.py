##
# -*- coding: utf-8 -*-
# terminal.py, A cross platform Terminal wrapper for CLI
##
import sys
import os
from select import select
##
try:
    import colorama
except ModuleNotFoundError:
    try:
        import pip
        pip.main('install', 'colorama')
    except ModuleNotFoundError:
        print('Required module: colorama')
        sys.exit()

if os.name == 'nt':
    import msvcrt  # WINDOWS
##


class IO:
    _backspace = chr(8)
    _return = chr(13)
    _newline = chr(10)

    def __init__(self):
        colorama.init()
        self.pos = lambda x, y: '\x1b[%d;%dH' % (y, x)
        self.cursor_pos = (0, 0)
        self.clear = '\033[2J\033[1;1f'
        self.right = colorama.Cursor.FORWARD
        self.down = colorama.Cursor.DOWN
        self.left = colorama.Cursor.BACK
        self.up = colorama.Cursor.UP
        self.bordered = False
        self.streams = {
            'main': ['']
        }
        print(self.clear)

    @property
    def resolution(self):
        return tuple(os.get_terminal_size())

    def kbhit(self):
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []

    def getch(self):
        if os.name == 'nt':
            return msvcrt.getch().decode()
        else:
            return sys.stdin.read(1)

    def stream_get(self, stream='main', till_last=''):
        out = ''
        for i in reversed(self.streams[stream]):
            if i is till_last:
                break
            out += i
        if till_last:
            self.streams[stream].append(till_last)
        return ''.join(reversed(out))

    def backspace(self, stream='main', amount=1):
        if len(self.streams[stream]) > 1:
            target = self.streams[stream][-1]
            # tail = self.streams[stream][-2] if len(self.streams[stream]) > 2 else None
            if target == '\n':
                return
            else:
                print(self.left() + ' ' + self.left(), end='')
                del self.streams[stream][-1]

    def clean_line(self):
        cols, rows = self.resolution
        padding = ('║' if self.bordered else '')
        print('\r' + padding + ' '*(cols-3) + self.left(cols-3), end='')

    def mv_cursor(self, x, y):
        print(self.pos(x, y), end='')

    def print(self, *args, **kwargs):
        args = (str(_) for _ in args)

        stream = kwargs.get('stream', 'main')
        if stream not in self.streams:
            self.streams[stream] = ['']

        end = kwargs.get('end', '')
        x = kwargs.get('x', None)
        y = kwargs.get('y', None)

        if x and y:
            self.mv_cursor(x, y)

        if not self.bordered:
            for char in args:
                print(char, end=end)
                self.streams[stream].append(char)
                if end:
                    self.streams[stream].append(end)
        else:
            for char in args:
                if char is self._newline:
                    print('\n', end=end)
                elif self.streams[stream][-1] is self._newline:
                    print(self.right() + char, end=end)
                else:
                    print(char, end=end)
                self.streams[stream].append(char)
                if end:
                    self.streams[stream].append(end)


class Border(IO):
    def __init__(self):
        super().__init__()
        cols, rows = self.resolution

        self.bordered = False
        self.border_chars = list('╔╗╚╝═║╠╣')
        self.top = '╔'+'═'*(cols-3)+'╗'+'\n'
        self.bottom = '╚'+'═'*(cols-3)+'╝'
        self.wall = '║'+' '*(cols-3)+'║'+'\n'
        self.wall_break = '╠'+'═'*(cols-3)+'╣'+'\n'
        self.border()

    def border(self):
        if not self.bordered:
            cols, rows = self.resolution
            for row in range(0, rows):
                if row == 0:
                    print(self.top, end='')
                elif row == rows-1:
                    print(self.bottom, end='')
                elif row == rows-3:
                    print(self.wall_break, end='')
                else:
                    print(self.wall, end='')
            print(self.up() + self.left(cols-2), end='')
            self.bordered = True

    @property
    def input_line(self):
        if not self.bordered:
            self.border

        cols, rows = self.resolution
        return (2, rows-2)
