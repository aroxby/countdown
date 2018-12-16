#!/usr/bin/env python
import sys
import datetime
from time import sleep

TDZ = datetime.timedelta(0)

def fix_td_len(tds):
    if len(tds) == 7:
        tds += '.000000'
    return tds

def update(duration, remaining, file, width=100, overwrite=True):
    width -= 2
    tds = fix_td_len('{}'.format(remaining))
    frac = remaining / duration
    pro_rem = int(frac * width)
    pro_com = width - pro_rem
    perc = int(100 * (1 - frac))
    progress = '[' + '=' * pro_com + '-' * pro_rem + ']'
    end = '\r' if overwrite else '\n'
    
    print('{} {} ({}%) '.format(tds, progress, perc), file=file, flush=True, end='\r')

def countdown(seconds, file):
    duration = datetime.timedelta(seconds=seconds)
    end = datetime.datetime.now() + duration
    remaining = end - datetime.datetime.now()
    while remaining >= TDZ:
        update(duration, remaining, file)
        sleep(0.1)
        remaining = end - datetime.datetime.now()
    update(duration, TDZ, file, overwrite=False)

def main(argv):
    if len(argv)!=2:
        print("Usage: ./main.py seconds", file=sys.stderr)
    else:
        time = int(argv[1])
        countdown(time, sys.stdout)

if __name__ == '__main__':
    main(sys.argv)