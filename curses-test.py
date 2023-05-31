#! /usr/bin/env python3
#meant to help me learn crs
import curses as crs
import time

stdscr = crs.initscr()


def mainscr(stdscr):
    crs.curs_set(False)
    stdscr.nodelay(True)
    crs.init_pair(1, crs.COLOR_BLUE, crs.COLOR_BLACK)
    crs.init_pair(2, crs.COLOR_RED, crs.COLOR_BLUE)

    
    stdscr.clear()
    stdscr.addstr(2, 2, 'hello\u25a0\u25a0')
    stdscr.addstr(3, 8, '\u25a0')
    stdscr.addstr('weuw', crs.color_pair(1))
    stdscr.addstr(5, 5, '\u3000'); stdscr.addstr('\u3000', crs.color_pair(2))
    stdscr.addstr(6, 5, '\u3000\u3000\u3000', crs.color_pair(2))
    stdscr.addstr(8, 5, '\u0020'); stdscr.addstr('\u0020', crs.color_pair(2))
    stdscr.addstr(9, 5, '\u0020\u0020\u0020', crs.color_pair(2))

    
    
    stdscr.refresh()
    time.sleep(2)
    
    stdscr.clear()
    stdscr.addstr(5, 5, 'goodbye')
    stdscr.refresh()
    time.sleep(1)
    #stdscr.clear()
    
    
    while True:
        try:
            w = stdscr.getkey()
            stdscr.addstr(str(w))
            stdscr.refresh()
        except crs.error:
            pass
        time.sleep(0.1)

crs.wrapper(mainscr)
''' manual init and close
crs.noecho() # turns of automatic echoing of keys
crs.cbreak() # detects input without return key
stdscr.keypad(True) # handles special keys instead of letting
                    #the program handle escape sequences

crs.nocbreak()
stdscr.keypad(False)
crs.echo()
crs.endwin()
'''
