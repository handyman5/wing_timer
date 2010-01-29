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
    _now = 0

    def __init__(self, next):
        self._now = datetime.now()
        ng = "".join(next)
        if ng[0] == '+':
            (hr, mn) = ng[1:].split(":")
            self._game_seed = self._now + relativedelta(hours=int(hr), minutes=int(mn))
        else:
            self._game_seed = parse(ng)

        if relativedelta(self._game_seed, self._now).minutes < 0:
            self._game_seed = self._game_seed + relativedelta(days=1)


    def calc_next_game(self):
        self._now = datetime.now()
        if relativedelta(self._game_seed, self._now).minutes > 0:
            self._next_game = self._game_seed
        else:
            self._game_seed = self._game_seed + relativedelta(hours=2, minutes=30)
            self.calc_next_game()


    def __str__(self):
        self.calc_next_game()
        next = relativedelta(self._next_game, self._now)
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
        w(gt.ESC + '[2K')
        w(gt.ESC + '[u')
        w(gt.ESC + '[s')
        w(str(gt))
        stdout.flush()
        sleep(1)
