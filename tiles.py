from itertools import combinations
from random import randint

MUL = 2

COLS   = 5
LINES  = 5
SPACES = 15
MULT   = 2
LEFT   = 1
RIGHT  = 2
UP     = 3
DOWN   = 4


tbl = [ [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
      ]

def addRandom(tbl):
    ret = tbl
    found = False
    #FIX ME! :)
    cnt = 0
    while not found and cnt < 10000:
        l = randint(0, LINES-1)
        c = randint(0, COLS-1)
        cnt += 1
        if ret[l][c] == 0:
            ret[l][c] = MUL ** randint(1,2)
            found = True
    if not found:
        return False, ret
    return True, ret


def swapTblOrientation(l):
    ret = []
    for lN in range(0,len(l)):
        ret += [ [row[lN] for row in l] ]
    return ret

def combine2InSequence(l):
    if len(l) < 2: return l
    ret = []
    lastValue = None
    for v in l:
        if lastValue is None:
            lastValue = v
        else:
            ret += [ (lastValue, v) ]
            lastValue = v
    return ret

def drawTable(tbl):
    centerString = "{:^"+str(SPACES)+"}"
    ret = ("_"*SPACES+"_")*COLS+"\n"
    for linhas in tbl:
        for cel in linhas:
            if cel > 0:
                ret += centerString.format(cel)+"|"
            else:
                ret += centerString.format("")+"|"
        ret += "\n"+("_"*SPACES+"|")*COLS+"\n"
    return ret


def pushLine(line):
    #push values right
    linePushed = [y for y in line if y != 0]
    ret = []

    #do we have at least two values?
    if len(linePushed) >= 2:
        # now do some calculations
        # for every equal consecutive value, sum it
        didSum = False
        lastValue = None
        for (v1, v2) in combine2InSequence(linePushed):
            if v1 == v2 and not didSum:
                ret += [v1+v2]
                didSum = True
            else:
                if not didSum:
                    ret += [v1]
                didSum = False
            lastValue = v2
        if not didSum:
            ret += [lastValue]
    else:
        ret = linePushed
    #fill values left
    for _ in range(len(line)-len(ret)):
        ret.insert(0, 0)
    return ret


def move(tbl, direction):
    ret = []
    if direction in (LEFT, RIGHT):
        for line in tbl:
            if direction == RIGHT:
                ret += [ pushLine(line) ]
            elif direction == LEFT:
                ret += [ list(reversed(pushLine(
                                list(reversed(line))))) ]
    elif direction in (UP, DOWN):
        tbl = swapTblOrientation(tbl)
        for line in tbl:
            if direction == DOWN:
                ret += [ pushLine(line) ]
            elif direction == UP:
                ret += [ list(reversed(pushLine(
                                list(reversed(line))))) ]
        ret = swapTblOrientation(ret)
    return ret


import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,0,"Hit 'q' to quit")
#print(drawTable(tbl))

key = ''
while key != ord('q'):
    stdscr.addstr(4,0, drawTable(tbl))
    found, tbl = addRandom(tbl)
    if not found:
        stdscr.addstr(2,0, 'GAME OVER BITCH')
        stdscr.getch()
        break


    stdscr.addstr(4,0, drawTable(tbl))
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_LEFT: 
            tbl = move(tbl, LEFT)
            break
        elif key == curses.KEY_RIGHT: 
            tbl = move(tbl, RIGHT)
            break
        elif key == curses.KEY_DOWN: 
            tbl = move(tbl, DOWN)
            break
        elif key == curses.KEY_UP: 
            tbl = move(tbl, UP)
            break
        elif key == ord('q'):
            break

curses.endwin()