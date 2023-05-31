#! /usr/bin/env python3
import sys, csv, curses, playsound
import datetime as dt
from time import sleep, time
from threading import Thread, Semaphore
from random import randint
#import modul as md

#md.check_and_install('playsound')

def sb_append(date, name, score):
    nume_fisier = 'score.csv'
    rand_nou = [date, name, score]
    
    with open(nume_fisier, 'a', newline='') as fisier_csv:
        scriitor_csv = csv.writer(fisier_csv)
        scriitor_csv.writerow(rand_nou)

def leaderb():
    nume_fisier = 'score.csv'
    
    with open(nume_fisier, 'r') as fisier_csv:
        cititor_csv = csv.reader(fisier_csv)
        urmatorul = cititor_csv  # Ignorăm antetul
        
        clasament = sorted(cititor_csv, key=lambda x: int(x[2]), reverse=True)
        primii_zece = clasament[:10]
        
        return primii_zece
'''
# Exemplu de utilizare
clasament = leaderb()
for pozitie, jucator in enumerate(clasament, start=1):
    print(f"Locul {pozitie}: {jucator}")
'''
tick_wait = Semaphore()


def tick():
    while True:
        sleep(0.015)
        tick_wait.release()

tick_thread = Thread(target=tick)

def music():
    while True:
        playsound.playsound('korobeiniki_lofi.mp3')
        
music_thread = Thread(target=music)

def coreloop():
    
    stdscr = curses.initscr()
    

    #time_last = time() #DEBUG: time meter
    
    def mainscr(stdscr):
        stdscr.clear()
        curses.resize_term(30, 60)
        stdscr.refresh()
        curses.curs_set(False)
        stdscr.nodelay(True)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)#standard
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK) #normal menu
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE) #selected menu
        
        stdscr.clear()
        
        board_offset = 10
        
        step_counter = 0
        move_counter = 0
        grav = 10
        gravity = [0.01667, 0.02101, 0.02697, 0.03525, 0.04694, 0.06361, 0.0879, 0.1236, 0.1775, 0.2598, \
        0.388, 0.59, 0.92, 1.46, 2.36, 3.91, 6.61, 11.43, 20]
        mgrav = 3
        fill_ch = '\uff5c'
        piece_ch = '\u3000'
        
        global level
        global score
        global lines
        level = 1
        score = 0
        lines = 0
        
        global t1
        global t2
        global t3
        global t4
        t1 = [0, 0]
        t2 = [0, 0]
        t3 = [0, 0]
        t4 = [0, 0]
        
        global current_piece
        global current_rotation
        current_piece = ''
        current_rotation = 0
        
        def spawn_piece(force=0):
            global t1, t2, t3, t4, current_piece, current_rotation
            
            if force == 0:
                piece = randint(1, 7)
            else:
                piece = force
            
            if piece == 1: #I
                t1 = [3, 3]
                t2 = [3, 4]
                t3 = [3, 5]
                t4 = [3, 6]
                current_piece = 'I'
                
            elif piece == 2: #O
                t1 = [2, 4]
                t2 = [2, 5]
                t3 = [3, 4]
                t4 = [3, 5]
                current_piece = 'O'
                
            elif piece == 3: #T
                t1 = [2, 4]
                t2 = [3, 3]
                t3 = [3, 4]
                t4 = [3, 5]
                current_piece = 'T'
            
            elif piece == 4: #J
                t1 = [2, 3]
                t2 = [3, 3]
                t3 = [3, 4]
                t4 = [3, 5]
                current_piece = 'J'
            
            elif piece == 5: #L
                t1 = [2, 5]
                t2 = [3, 3]
                t3 = [3, 4]
                t4 = [3, 5]
                current_piece = 'L'
                
            elif piece == 6: #S
                t1 = [2, 4]
                t2 = [2, 5]
                t3 = [3, 3]
                t4 = [3, 4]
                current_piece = 'S'
                
            else: #Z
                t1 = [2, 3]
                t2 = [2, 4]
                t3 = [3, 4]
                t4 = [3, 5]
                current_piece = 'Z'
                
            current_rotation = 0
            '''
            def spawn_piece():
            global t1
            global t2
            global t3
            global t4
            
            t1 = [2, 4]
            t2 = [3, 3]
            t3 = [3, 4]
            t4 = [3, 5]
            '''
        
        global board
        board = []
        for i in range(24):
            board.append([[],[],[],[],[],[],[],[],[],[]])
            
        #print(board)
        
        for i in range(24):
            for j in range(10):
                board[i][j] = [fill_ch, 1]
        #print(board)
        
        
        stdscr.move(0, 0)
        for i in range(len(board)): #print empty board
            stdscr.move(i, board_offset)
            for j in board[i]:
                stdscr.addch(j[0], curses.color_pair(j[1]))
        #PIECES
        #[y, x, color]
        
        
        
            
        def t_down():     
            rsh()
            
            try:
                if board[t1[0]+1][t1[1]][1] == 3 or \
                t1[0] == 23\
                or board[t2[0]+1][t2[1]][1] == 3 \
                or t2[0] == 23\
                or board[t3[0]+1][t3[1]][1] == 3 \
                or t3[0] == 23\
                or board[t4[0]+1][t4[1]][1] == 3 \
                or t4[0] == 23:
                    solidify()
                    sweep()
                    spawn_piece()
                
                else:
                    t1[0] += 1
                    t2[0] += 1
                    t3[0] += 1
                    t4[0] += 1
            except IndexError:
                solidify()
                sweep()
                spawn_piece()
                
        def t_right():
            rsh()

            if t1[1] == 9 or t2[1] == 9 or t3[1] == 9 or t4[1] == 9 \
            or board[t1[0]][t1[1]+1][1] == 3 \
            or board[t2[0]][t2[1]+1][1] == 3 \
            or board[t3[0]][t3[1]+1][1] == 3 \
            or board[t4[0]][t4[1]+1][1] == 3:
                pass
            else:
                t1[1] += 1
                t2[1] += 1
                t3[1] += 1
                t4[1] += 1
        
        def t_left():
            rsh()
            

            if t1[1] == 0 or t2[1] == 0 or t3[1] == 0 or t4[1] == 0 \
            or board[t1[0]][t1[1]-1][1] == 3 \
            or board[t2[0]][t2[1]-1][1] == 3 \
            or board[t3[0]][t3[1]-1][1] == 3 \
            or board[t4[0]][t4[1]-1][1] == 3:
                pass
                
            else:
                t1[1] -= 1
                t2[1] -= 1
                t3[1] -= 1
                t4[1] -= 1
        
        
        def solidify():
            board[t1[0]][t1[1]] = [piece_ch, 3]
            board[t2[0]][t2[1]] = [piece_ch, 3]
            board[t3[0]][t3[1]] = [piece_ch, 3]
            board[t4[0]][t4[1]] = [piece_ch, 3]
            global mode
            count = 0
            
            for i in range(4): #check for end of game condition
                count = 0
                for j in range(10):
                    if board[i][j][1] != 1:
                        count += 1
            if count != 0:
                for i in range(24):
                    for j in range(10):
                        board[i][j] = [fill_ch, 1]
                mode = 2
                #print(mode)
            count = 0
        
        def rsh():
            board[t1[0]][t1[1]] = [fill_ch, 1]
            board[t2[0]][t2[1]] = [fill_ch, 1]
            board[t3[0]][t3[1]] = [fill_ch, 1]
            board[t4[0]][t4[1]] = [fill_ch, 1]
        
        def collision_check(r1, r2, r3, r4):
            rsh()

            try:
                if not(r1[1] == 10 or r2[1] == 10 or r3[1] == 10 or r4[1] == 10 \
                or r1[1] < 0 or r2[1] < 0 or r3[1] < 0 or r4[1] < 0 \
                or board[r1[0]][r1[1]][1] == 3 \
                or board[r2[0]][r2[1]][1] == 3 \
                or board[r3[0]][r3[1]][1] == 3 \
                or board[r4[0]][r4[1]][1] == 3):
                    global t1, t2, t3, t4
                    t1 = list(r1)
                    t2 = list(r2)
                    t3 = list(r3)
                    t4 = list(r4)
                    return True
            except IndexError:
                t_down()
                return False

 
        def rotate():
            global t1, t2, t3, t4, current_piece, current_rotation
            if current_piece == 'I':
                if current_rotation == 0:
                    r1 = list([t1[0]-1, t1[1]+1])
                    r2 = list(t2)
                    r3 = list([t3[0]+1, t3[1]-1])
                    r4 = list([t4[0]+2, t4[1]-2])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 1
                        
                else:
                    r1 = list([t1[0]+1, t1[1]-1])
                    r2 = list(t2)
                    r3 = list([t3[0]-1, t3[1]+1])
                    r4 = list([t4[0]-2, t4[1]+2])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 0
            
            elif current_piece == 'T':
                if current_rotation == 0:
                    r1 = list([t1[0]+1, t1[1]+1])
                    r2 = list([t2[0]-1, t2[1]+1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]-1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 1
                        
                elif current_rotation == 1:
                    r1 = list([t1[0]+1, t1[1]-1])
                    r2 = list([t2[0]+1, t2[1]+1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]-1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 2
                
                elif current_rotation == 2:
                    r1 = list([t1[0]-1, t1[1]-1])
                    r2 = list([t2[0]+1, t2[1]-1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]+1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 3
                
                elif current_rotation == 3:
                    r1 = list([t1[0]-1, t1[1]+1])
                    r2 = list([t2[0]-1, t2[1]-1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]+1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 0
            
            elif current_piece == 'J':
                if current_rotation == 0:
                    r1 = list([t1[0], t1[1]+2])
                    r2 = list([t2[0]-1, t2[1]+1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]-1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 1
                
                elif current_rotation == 1:
                    r1 = list([t1[0]+2, t1[1]])
                    r2 = list([t2[0]+1, t2[1]+1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]-1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 2
                        
                elif current_rotation == 2:
                    r1 = list([t1[0], t1[1]-2])
                    r2 = list([t2[0]+1, t2[1]-1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]+1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 3
                        
                elif current_rotation == 3:
                    r1 = list([t1[0]-2, t1[1]])
                    r2 = list([t2[0]-1, t2[1]-1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]+1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 0
                        
            elif current_piece == 'L':
                if current_rotation == 0:
                    r1 = list([t1[0]+2, t1[1]])
                    r2 = list([t2[0]-1, t2[1]+1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]-1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 1
                
                elif current_rotation == 1:
                    r1 = list([t1[0], t1[1]-2])
                    r2 = list([t2[0]+1, t2[1]+1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]-1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 2
                        
                elif current_rotation == 2:
                    r1 = list([t1[0]-2, t1[1]])
                    r2 = list([t2[0]+1, t2[1]-1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]+1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 3
                        
                elif current_rotation == 3:
                    r1 = list([t1[0], t1[1]+2])
                    r2 = list([t2[0]-1, t2[1]-1])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]+1])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 0
            
            elif current_piece == 'S':
                if current_rotation == 0:
                    r1 = list([t1[0], t1[1]])
                    r2 = list([t2[0], t2[1]-2])
                    r3 = list([t3[0]-2, t3[1]])
                    r4 = list([t4[0], t4[1]])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 1
                else:
                    r1 = list([t1[0], t1[1]])
                    r2 = list([t2[0], t2[1]+2])
                    r3 = list([t3[0]+2, t3[1]])
                    r4 = list([t4[0], t4[1]])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 0
            
            elif current_piece == 'Z':
                if current_rotation == 0:
                    r1 = list([t1[0]-1, t1[1]+2])
                    r2 = list([t2[0], t2[1]])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]-1, t4[1]])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 1
                else:
                    r1 = list([t1[0]+1, t1[1]-2])
                    r2 = list([t2[0], t2[1]])
                    r3 = list([t3[0], t3[1]])
                    r4 = list([t4[0]+1, t4[1]])
                    if collision_check(r1, r2, r3, r4):
                        current_rotation = 0
        
        def sweep():
            global level, score, lines
            
            rows = []
            
            for i in range(24):
                count = 0
                for j in range(10):
                    if board[i][j][1] == 3:
                        count += 1
                if count == 10:
                    rows.append(i)
                count = 0
            
            lr = len(rows)
            if lr == 1:
                score += 100*level
            elif lr == 2:
                score += 300*level
            elif lr ==3:
                score += 500*level
            elif lr >= 4:
                score += 800*level
                
            lines += lr
            
            if lines >= 10:
                level += 1
                lines -= 10
                
            
            
            count = 0
            while len(rows) != 0:
                row = max(rows)+count
                
                for i in range(10):
                    board[row][i] = [fill_ch, 1]
                
                for i in range(row, 0, -1): 
                    board[i] = list(board[i-1])
                
                #for i in range(len(board)): #draw board
                #    stdscr.move(i, board_offset)
                #    
                #    for j in board[i]:
                #        stdscr.addch(j[0], curses.color_pair(j[1]))
                #        stdscr.refresh()
                        
                rows.pop(rows.index(row-count))
                count += 1

        spawn_piece()
        
        #!------------------------------------------ GAME VARIABLES
        level_select = 1
        
        global mode
        mode = 0 #0 menu, 1 game, 2 game over, 3 score,
        mode_sw = 0
        menu = 0
        
        while True: #--------------- MAIN LOOP
            '''
            try:
                w = stdscr.getkey()
                stdscr.addstr(str(w))
                stdscr.refresh()
            except curses.error:
                pass
            '''
            if mode != mode_sw:
                stdscr.clear()
                
            if mode == 0:
                mode_sw = 0
                l = [5, 4, 4, 4]
                stdscr.clear()
                while mode == 0:
                    tick_wait.acquire()
                    stdscr.move(0, 0)
                    stdscr.addstr(4, 10, '/' + '-' * 39 + '\\')
                    stdscr.addstr(5, 10, '|  _____  ____   _____   /|   _   /---| |')
                    stdscr.addstr(6, 10, '|   \\|/   |       \\|/   ( |   |   |     |')
                    stdscr.addstr(7, 10, '|    |    |---     |     \\|   |   \\---\\ |')
                    stdscr.addstr(8, 10, '|    |    |        |     /|   |       | |')
                    stdscr.addstr(9, 10, '|    |    \\---     |    / |   ^   |---/ |')
                    #stdscr.addstr(10, 10, '|                                       |')
                    stdscr.addstr(10, 10, '\\' + '-'*39 + '/')
                    stdscr.addstr(13, 14, '1. Play!', curses.color_pair(l[0]))
                    stdscr.addstr(15, 14, '2. Starting level: {} '.format(str(level_select)), curses.color_pair(l[1]))
                    stdscr.addstr(17, 14, '3. Hall of fame', curses.color_pair(l[2]))
                    #stdscr.addstr(19, 14, '4. Credits', curses.color_pair(l[3]))
                    stdscr.addstr(19, 14, '4. Quit', curses.color_pair(l[-1]))
                    try:
                        w = stdscr.getkey()
                        if w == 'KEY_UP' and l[0] != 5:
                            i = l.index(5)
                            l[i] = 4
                            l[i-1] = 5
                        elif w == 'KEY_DOWN' and l[-1] != 5:
                            i = l.index(5)
                            l[i] = 4
                            l[i+1] = 5
                        elif w == '\n' or w == '\r' or w == 'KEY_RIGHT':
                            if l[0] == 5:
                                mode = 1
                            elif l[1] == 5:
                                if level_select < 10:
                                    level_select += 1
                            elif l[2] == 5:
                                mode = 3
                            #elif l[3] == 5:
                                #pass
                            elif l[-1] == 5:
                                sys.exit()
                        elif w == 'KEY_LEFT' and l[1] == 5 and level_select > 1:
                            level_select -= 1
                    
                                
                    except curses.error:
                        pass
                    stdscr.refresh()
                
            elif mode == 1:
                stdscr.clear()
                level = level_select
                while mode == 1:
                    tick_wait.acquire()

                    stdscr.move(0, 0)
                        
                    #spawn_piece()
                    
                    board[t1[0]][t1[1]] = [piece_ch, 2]
                    board[t2[0]][t2[1]] = [piece_ch, 2]
                    board[t3[0]][t3[1]] = [piece_ch, 2]
                    board[t4[0]][t4[1]] = [piece_ch, 2]
                    
                    #stdscr.clear()
                    for i in range(len(board)): #draw board
                        stdscr.move(i, board_offset)
                        
                        for j in board[i]:
                            if i < 4:
                                stdscr.addch(piece_ch, curses.color_pair(1))
                            else:
                                stdscr.addch(j[0], curses.color_pair(j[1]))
                            stdscr.refresh()
                    
                    #grav = 10
                    if level < 14:
                        grav = 1/gravity[level-1]
                    elif level >= 14:
                        grav = 1/gravity[13]

                    if step_counter >= grav:
                        stdscr.addstr(8, 40, 'Level:......{}'.format(str(level)))
                        stdscr.addstr(10, 40, 'Score:......{}'.format(str(score)))
                        t_down()
                        step_counter -= grav
                        #stdscr.addstr(10, 40, str(t1)) #DEBUG tetromino position
                        #stdscr.addstr(11, 40, str(t2))
                        #stdscr.addstr(12, 40, str(t3))
                        #stdscr.addstr(13, 40, str(t4))
                        #stdscr.addstr(14, 40, str(board[(t3[0]+1)][t3[1]][1]))
                    else:
                        step_counter += 1
                    
                    if move_counter == mgrav:
                        try:
                            w = stdscr.getkey()
                            if w == 'KEY_RIGHT':
                                t_right()
                            elif w == 'KEY_LEFT':
                                t_left()
                            elif w == 'KEY_DOWN':
                                t_down()
                            elif w == 'KEY_UP':
                                rotate()
                            elif w == '\'': #DEBUG stop
                                sleep(2000)
                            curses.flushinp()
                        except curses.error:
                            pass
                        move_counter = 0
                    else:
                        move_counter += 1
                 
                
            elif mode == 2:
                stdscr.clear()
                stdscr.addstr(8, 10, '/' + 18*'-' + '\\')
                stdscr.addstr(9, 10, '|' + 18 * ' ' + '|')
                stdscr.addstr(10, 10, '|' + '    Game Over!    |')
                stdscr.addstr(11, 10, '|' + 18 * ' ' + '|')
                stdscr.addstr(12, 10, '|' + '    Score: {}    '.format(score))
                stdscr.addstr(12, 29, '|')
                stdscr.addstr(13, 10, '|' + 18 * ' ' + '|')
                stdscr.addstr(14, 10, '|' + 18 * ' ' + '|')
                stdscr.addstr(15, 10, '|' + ' Enter your name: |')
                stdscr.addstr(16, 10, '|' + 18 * ' ' + '|')
                stdscr.addstr(17, 10, '|' + 18 * ' ' + '|')
                stdscr.addstr(17, 11, 18*' ', curses.color_pair(5))
                stdscr.move(17, 11)
                sleep(1.5)
                curses.flushinp()
                
                writtentext = []
                
                while mode == 2:
                    tick_wait.acquire()
                    try:
                        #curses.flushinp()
                        w = stdscr.getkey()
                        if w == '\n' or w == '\r':
                            s = ''.join(writtentext)
                            sb_append(str(dt.datetime.now()), s, score)
                            mode = 0
                            
                        elif w == 'KEY_BACKSPACE':
                            stdscr.addstr(17, stdscr.getyx()[1]-1, ' ', curses.color_pair(5))
                            stdscr.move(17, stdscr.getyx()[1]-1)
                            writtentext.pop(-1)
                            
                        else:
                            stdscr.addstr(str(w), curses.color_pair(5))
                            writtentext.append(w)
                            

                    except curses.error:
                        pass
                    stdscr.refresh()
        
            elif mode == 3:
                stdscr.clear()
                stdscr.addstr(8, 10, 'High Scores:')
                
                while mode == 3:
                    tick_wait.acquire()
                    hs = leaderb()
                    n = 9
                    for i in range(len(hs)):
                        stdscr.addstr(n, 10, '{}. {}: {}'.format(str(n-8), str(hs[i][1]), str(hs[i][2])))
                        n += 1
                     
                    try:
                        #curses.flushinp()
                        w = stdscr.getkey()
                        if w == '\n' or w == '\r':
                            mode = 0
                            

                    except curses.error:
                        pass
                    stdscr.refresh()
    

            stdscr.refresh()
            
                
            #tick_wait.acquire() #always last statement; wait for next tick
        
             
    curses.wrapper(mainscr)
    
    '''
    while True:
        #----------------------------------------  DEBUG: time meter
        #print(time())
        timedif = time() - time_last
        #print('timedif = ' + str(timedif))
        if str(timedif)[:5] != '0.200' and str(timedif)[:5] != '0.199':
            print(str(timedif)[:5])
        time_last = time()
        #<---------------------------------------> END DEBUG
        
        
        
        tick_wait.acquire() #always last statement; wait for next tick
    '''
core_thread = Thread(target=coreloop)

tick_thread.start()
music_thread.start()
core_thread.start()
