#!/usr/bin/env python
import sys
import datetime
from time import sleep

TDZ = datetime.timedelta(0)

def fix_td_len(tds):
    if len(tds) == 7:
        tds += '.000000'
    return tds

def update(duration, remaining, file, width=100, overwrite=True, headstart=0):
    width -= 2
    headstart /= 100.
    tds = fix_td_len('{}'.format(remaining))

    frac = 1- (remaining / duration)
    out_of = 1 - headstart
    frac *= out_of
    frac += headstart
    perc = int(100 * frac)
    pro_com = int(frac * width)
    pro_rem = width - pro_com

    progress = '[' + '=' * pro_com + '-' * pro_rem + ']'
    end = '\r' if overwrite else '\n'
    print_kwargs = {'file': file, 'flush': True, 'end': end}
    print('{} {} ({}%)'.format(tds, progress, perc), **print_kwargs)

def countdown(seconds, start, file):
    duration = datetime.timedelta(seconds=seconds)
    end = datetime.datetime.now() + duration
    remaining = end - datetime.datetime.now()
    while remaining >= TDZ:
        update(duration, remaining, file, headstart=start)
        sleep(0.1)
        remaining = end - datetime.datetime.now()
    update(duration, TDZ, file, overwrite=False)

def main(argv):
    if len(argv) not in [2, 3]:
        print("Usage: ./main.py seconds [start%]", file=sys.stderr)
    else:
        time = int(argv[1])
        if len(argv) > 2:
            start = int(argv[2])
        else:
            start = 0
        countdown(time, start, sys.stdout)

if __name__ == '__main__':
    main(sys.argv)