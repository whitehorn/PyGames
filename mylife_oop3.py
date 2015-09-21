# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:08:10 2015

@author: SHABA
"""

import Tkinter as tk
from random import randint
import random
import copy

from time import sleep


class Board():
    '''
    '''
    def __init__(self, size=10, time_st=0.1, boardtype='Bordered'):

        self.N = size
        self.time_st = time_st
        self.boardtype = boardtype
        self.cells = {}
        self.POLE = {}
        self.OLDPOLE = {}
        self.GRANDPOLE = {}
        self.bdic = {}
        self.new_board()


    def new_board(self):

        self.root = tk.Tk()
#        self.root.geometry('640x640') #%d+%d+%d' % (640, 640, 10, 10))
        self.root.title('LIFE 1.0')
#        self.root.geometry('%dx%d%+d%+d' % (500, 500, 500, 0))

        self.cell_size = 10
        
        self.width = self.N*self.cell_size

        self.life = 'green'
        self.death = 'black'
        self.life = 'black'
        self.death = 'white'

        self.nums = tk.IntVar()
        self.nums.set(0)

        self.loop = tk.IntVar()
        self.loop.set(1)

        self.alive = tk.IntVar()
        self.alive.set(0)

        self.root.title('LIFE 1.0')
        self.slab = tk.Label(self.root, width=50, text='Score')
        self.slab.pack(side=tk.TOP)

#        img = tk.PhotoImage("pix2.gif")
#        print img
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.width,
                                bg=self.death)
        self.canvas.pack()

#        self.canvas.bind('<B1-Motion>', self.redraw)
        self.canvas.bind('<ButtonPress-1>', self.redraw)
        self.canvas.bind('<ButtonPress-3>', self.redraw)
        

        for i in xrange(self.N):
            for j in xrange(self.N):
                pos = (i, j)
                self.POLE[pos] = False
                x1 = 1 + self.cell_size*j
                y1 = 1 + self.cell_size*i
                x2 = self.cell_size + self.cell_size*j - 1
                y2 = self.cell_size + self.cell_size*i - 1
                                
                rect = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                    outline='grey', width=1, fill=self.death,
                                                    tag=pos)
                self.canvas.itemconfig(rect, state=tk.NORMAL) #, state=HIDDEN, tags=('hid','0'))


                self.cells[pos] = [rect, False]
        
        self.sbut = tk.Button(self.root, width=self.N, text='RANDOM', command=self.brandom)
#        self.sbut.pack(side=tk.LEFT)
        self.sbut.pack(fill=tk.Y)

        self.tbut = tk.Button(self.root, width=self.N, text='FIGURES', command=self.figures)
#        self.tbut.pack(side=tk.BOTTOM)
        self.tbut.pack(fill=tk.Y)

        
        self.rbut = tk.Button(self.root, width=self.N, text='RUN', command=self.run) #,
#                         state=tk.DISABLED)
#        self.rbut.pack(side=tk.RIGHT, fill=tk.Y)
        self.rbut.pack(fill=tk.Y)

        self.root.mainloop()

    
    def redraw(self, event):
    
#        print event.x, event.y
        jj = int(event.x / self.cell_size)
        ii = int(event.y / self.cell_size)
        pos = (ii, jj)

        if event.num == 1:
            color = self.life
            self.cells[pos][-1] = True
        elif event.num == 3:
            color = self.death
            self.cells[pos][-1] = False

        self.canvas.itemconfig(self.cells[pos][0], fill=color)


    def brandom(self):
    
        t = 0
        for i in xrange(self.N):
            for j in xrange(self.N):
                pos = (i, j)
                self.cells[pos][-1] = bool(randint(False, True))

                if self.cells[pos][-1]:
                    t += 1
                    color = self.life
                else:
                    color = self.death
                self.canvas.itemconfig(self.cells[pos][0], fill=color) 
    
        self.alive.set(str(t))
        self.rbut.config(state=tk.NORMAL)
        self.tbut.config(text='FIGURE')       
        self.slab.config(text='Generation %s. There are %s creatures' % (self.loop.get(),
                                                                    self.alive.get()))

    def clear(self):
    
        for i in xrange(self.N):
            for j in xrange(self.N):
                pos = (i, j)
                self.cells[pos][-1] = False
                self.canvas.itemconfig(self.cells[pos][0], fill=self.death)


    def figures(self):
    
        if(self.N % 2 != 0):
            XY = self.N + 1
            XY = (self.N + 1)/2
        else:
            XY = self.N/2
    
        
        self.clear()
        
        figdic = {'Glider': [(XY-1, XY-1), (XY, XY-1), (XY+1, XY-1), 
                             (XY+1, XY),
                             (XY, XY+1)],
                  'Tank_E': [(XY-1, XY-1), (XY+1, XY-1), 
                           (XY-1, XY), (XY, XY), (XY+1, XY),
                             (XY, XY+1)],
                  'Tank_S': [(XY-1, XY-1), (XY-1, XY+1), 
                           (XY, XY-1), (XY, XY), (XY, XY+1),
                             (XY+1, XY)],
                  'Tank_N': [(XY+1, XY+1), (XY+1, XY-1), 
                           (XY, XY-1), (XY, XY), (XY, XY+1),
                             (XY-1, XY)],
                  'Cat': [],

                  'R-pentamino' : [(XY, XY-1), 
                                   (XY-1, XY), (XY, XY), (XY+1, XY),
                                   (XY+1, XY+1)],
                   'O-pentamino' : [(XY, XY-2), (XY, XY-1), (XY, XY), 
                                    (XY, XY+1), (XY, XY+2)]}
    
#        self.root.update()
        key = random.choice(figdic.keys())
        coors = figdic[key]
        t = 0
        for pos in coors:
            self.cells[pos][-1] = True
            self.canvas.itemconfig(self.cells[pos][0], fill=self.life)
            t += 1
        
        self.alive.set(str(t))
        self.rbut.config(state=tk.NORMAL)
        self.tbut.config(text=key)
        self.slab.config(text='Generation %s. There are %s creatures' % (self.loop.get(),
                                                                    self.alive.get()))

#    def gui_quit(self):

    def board_type(self, pos):
        '''
        '''
        self.neibs = []
        for i in xrange(-1, 2, 1):
            posx = pos[0] + i
            for j in xrange(-1, 2, 1):
                posy = pos[-1] + j

                if self.boardtype == 'Bordered':
                    if((posx < 0 or posy < 0) or ((posx > self.N-1 or posy > self.N-1))):
                        pass
                    else:
                        self.neibs.append((posx, posy))
                            
                elif self.boardtype == 'Tor':
                    if posx < 0:
                        posx = self.N-1
                    elif posx > self.N-1:
                        posx = 0                
        
                    if posy < 0:
                        posy = self.N-1
                    elif posy > self.N-1:
                        posy = 0
        
                    self.neibs.append((posx, posy))
            
    
    def dead_or_alive(self, pos):
    

        self.board_type(pos)

#                posy = pos[-1] + j
#                if((posx < 0 or posy < 0) or ((posx > self.N-1 or posy > self.N-1))):
#                    continue
#                else:
#                    neibs.append((posx, posy))
    
        self.neibs.remove(pos)
        neib = 0
        for i in self.neibs:
            if self.OLDPOLE[i]:
                neib += 1
    
        if (self.OLDPOLE[pos]):
            if(neib == 2 or neib == 3):
                state = True
            else:
                state = False
        else:
            if(neib == 3):
                state = True
            else:
                state = False
    
        return state
    
    
    def run(self):
       
        self.sbut.config(text='QUIT', command=lambda: self.root.destroy())
        self.rbut.config(state=tk.DISABLED)
        self.tbut.config(state=tk.DISABLED)
    
        game = True
        while(game):
            t = 0
            self.loop.set(int(self.loop.get()) + 1)
            for i in xrange(self.N):
                for j in xrange(self.N):
                    pos = (i, j)
                    self.POLE[pos] = self.cells[pos][-1]
            
            self.OLDPOLE = copy.deepcopy(self.POLE)

            if(int(self.loop.get()) % 2 == 0):
                self.GRANDPOLE = copy.deepcopy(self.POLE)
        

            for i in xrange(self.N):
                for j in xrange(self.N):
                    pos = (i, j)
                    self.cells[pos][-1] = self.dead_or_alive(pos)
                    self.POLE[pos] = self.cells[pos][-1]

                    if self.cells[pos][-1]:
                        color = self.life
                        t += 1
                    else:
                        color = self.death
                    self.canvas.itemconfig(self.cells[pos][0], fill=color)  

            self.alive.set(t)
            msg = 'Generation %s. There are %s creatures' % (self.loop.get(),
                                                             self.alive.get())
            self.slab.config(text=msg)
    
            self.root.update()
            sleep(self.time_st)
    
            if(int(self.alive.get()) == 0):
                msg = 'All creatures are dead!'
                self.slab.config(text='GAME OVER %s' % msg)
                self.tbut.config(state=tk.NORMAL, text='RESTART', command=self.restart)
                game = False
    
    
            elif(self.OLDPOLE == self.POLE):
                msg = 'in %s generations. Still alive %s creatures' % (self.loop.get(), self.alive.get())
                
                self.slab.config(text='GAME OVER %s' % msg)
                self.tbut.config(state=tk.NORMAL, text='RESTART', command=self.restart)

                game = False
    
            elif(self.GRANDPOLE == self.POLE):
                msg = 'Generation %s reaches a stable form of life for %s creatures' % (self.loop.get(), self.alive.get())
                self.slab.config(text='GAME OVER %s' % msg)
                self.rbut['state'] = tk.DISABLED
                self.tbut.config(state=tk.NORMAL, text='RESTART', command=self.restart)
                game = False

    def restart(self):
        

        self.clear()

        msg = 'Select initial colony'
        self.slab.config(text='%s' % msg)

        self.sbut.config(text='RANDOM', state=tk.NORMAL, command=self.brandom)
        self.tbut.config(text='FIGURES', state=tk.NORMAL, command=self.figures)
        self.rbut.config(text='RUN LIFE', state=tk.NORMAL, command=self.run)

        self.loop.set(1)
        self.alive.set(0)

def create_board(pos):

   #    time_st = float(tsize.get())*0.05    
#    size = int(bsize.get())
    bsize = pos[0]
    tsize = pos[1]
    boardtype = pos[-1]

    s = bsize.get()
    spd = [0.3, 0.2, 0.15, 0.1, 0.05, 0.025]
    t = spd[tsize.get()]
    b = boardtype.get()

    print bsize, tsize
    Board(s, t, b)


def new_game():

    main = tk.Tk()
    main.title('LIFE 1.1')
#    main.geometry('%dx%d%+d%+d' % (200, 300, 0, 0))

    slab = tk.Label(main, text="Conway's Game of Life \n\n\n BOARD SIZE")
    slab.pack()

    bsize = tk.IntVar()
    bsize.set(17)
    tsize = tk.IntVar()
    tsize.set(3)

    bslider = tk.Scale(main, orient='horiz', from_=10, to=100, variable=bsize)
    bslider.pack()
    tlab = tk.Label(main, text='GAME SPEED')
    tlab.pack()
    tslider = tk.Scale(main, orient='horiz', from_=1, to=5, variable=tsize)
    tslider.pack()

    tlab = tk.Label(main, text='GAME TYPE ')
    tlab.pack()

    gtypes = ['Bordered', 'Tor']
    gbut = tk.StringVar()
    gbut.set('Bordered')
    
    for gtype in gtypes:
        rb = tk.Radiobutton(main, text=gtype, variable=gbut, value=gtype)
        rb.pack(anchor=tk.W)

    pos = [bsize, tsize, gbut]

    bbut = tk.Button(main, text='START', command=lambda pos=pos: create_board(pos))
    bbut.pack(side=tk.BOTTOM)

    main.mainloop()

#if __name__ == '__main__':
#    new_game()
