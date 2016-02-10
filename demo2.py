# coding: utf-8

import time
import math
import random

from snaffle import snaffle


snf = snaffle.Snaffle(start=False)

def plot(x, y, hit):
    if hit:
        script = "ctx.fillStyle = 'blue'; "
    else:
        script = "ctx.fillStyle = 'red'; "
    script += "ctx.fillRect({0}, {1}, 1, 1); ".format(x * 300, y * 300 + 30)
    snf.send_script(script)


def log(pi, n):
    script = "ctx.fillStyle = 'white'; ctx.fillRect(0, 0, 300, 30); ctx.fillStyle = 'black'; ";
    script += r"ctx.fillText('n = {0}', 12, 12, 300); ".format(n)
    script += r"ctx.fillText('pi = {0}', 12, 24, 300); ".format(pi)
    snf.send_script(script)


def main():
    snf.start()

    ins = 0
    outs = 0

    while True:
        x = random.random()
        y = random.random()
        if math.sqrt(x * x + y * y) <= 1.0:
            ins += 1
            plot(x, y, hit=True)
        else:
            outs += 1
            plot(x, y, hit=False)
        pi = 4 * ins / (ins + outs)
        log(pi, ins + outs)

    snf.shutdown()


if __name__=='__main__':
    main()

