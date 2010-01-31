#!/usr/bin/python

# make an API to get next battle time and time remaining, and then have main loop query those

from dateutil.parser import *
from dateutil.relativedelta import *
from datetime import *
from time import sleep
from sys import argv, exit, stdout


class GameTimer(object):
    ESC = chr(27)
    _game_seed = 0
    _next_game = 0

    def __init__(self, next):
        ng = "".join(next)
        if ng[0] == '+':
            hr = mn = 0
            try:
                (hr, mn) = ng[1:].split(":")
            except ValueError:
                mn = ng[1:]
            self._game_seed = datetime.now() + relativedelta(hours=int(hr), minutes=int(mn))
        else:
            self._game_seed = parse(ng)

        # Make specific times apply to the future only
        if relativedelta(self._game_seed, datetime.now()).minutes < 0:
            self._game_seed = self._game_seed + relativedelta(days=1)


    def calc_next_game(self):
        if (self._game_seed < datetime.now()):
            self._game_seed = self._game_seed + relativedelta(hours=2, minutes=30)
            print '''
DEBUG: adding game time
Current time: %s
Game seed: %s
Next game: %s
''' % (datetime.now(), self._game_seed, self._next_game)
        self._next_game = self._game_seed


    def __str__(self):
        self.calc_next_game()
        next = relativedelta(self._next_game, datetime.now())
        return "Next Wintergrasp is at %s (%s)" % (self._next_game.strftime("%I:%M %p"), (str(next.hours) + " hours, " + str(next.minutes) + " minutes, " + str(next.seconds) + " seconds"))


if __name__ == "__main__":
    if len(argv) < 2:
        print '''
Usage: "%s <TIME>" or "%s +<TIME>"

Specify time as "10:15 PM" or "+1 hour 10 minutes"/"+1:10" (uses fairly intelligent parsing for time specifications)
''' % (argv[0], argv[0])
        exit(1)

    gt = GameTimer(argv[1:])
    w = stdout.write

    while True:
        w(gt.ESC + '[1K')
        w(gt.ESC + '[0E')
        w(gt.ESC + '[s')
        w(gt.ESC + '[u')
        w(str(gt))
        stdout.flush()
        sleep(1)
