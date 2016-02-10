# coding: utf-8

import time
import math
import random

from snaffle import snaffle


def main():
    # ctx = snaffle_threading.init()
    snf = snaffle.Snaffle()

    cmd = ''
    i = 0
    while i < 1000000:
        x = i % 500
        y = 200 + math.sin(i / 100) * 100
        i += 1
        cmd += "ctx.fillRect({0}, {1}, 1, 1); ".format(x, y)
        if i % 500 == 0:
            color = "ctx.fillStyle = 'rgb({0}, {1}, {2})'; ".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            snf.send_script(color + cmd)
            cmd = ''
            print(i)

    snf.shutdown()


if __name__=='__main__':
    main()
