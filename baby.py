#!/usr/bin/env python
# coding: utf-8
import json
import sys
import curses
import time
from time import sleep, strftime
from datetime import datetime
from random import randrange
import math
import locale
from threading import Thread
from getpass import getuser

try:
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')


# constants
FILENAME = "baby.json"
SCR_X = 0
SCR_Y = 0
SCR_HEIGHT = 35
SCR_WIDTH = 70
PAD_GUTTER = 30
PAD_HEIGHT = SCR_HEIGHT+2*PAD_GUTTER
PAD_WIDTH = SCR_WIDTH+2*PAD_GUTTER
FRAME_TIME_S = 0.01
DEFAULT_SCORE = 10

FROM_BELOW = 0
FROM_ABOVE = 1
FROM_LEFT = 2
FROM_RIGHT = 3

# data

boystr = [u"$$$$$$\ $$\  $$\ ",
          u"\_$$  _|$$ | $  | ",
          u"  $$ |$$$$$$\\_/ $$$$$$$\        $$$$$$\ ",
          u"  $$ |\_$$  _|  $$  _____|       \____$$\ ",
          u"  $$ |  $$ |    \$$$$$$\         $$$$$$$ | ",
          u"  $$ |  $$ |$$\  \____$$\       $$  __$$ | ",
          u"$$$$$$\ \$$$$  |$$$$$$$  |      \$$$$$$$ | ",
          u"\______| \____/ \_______/        \_______| ",
          u" ",
          u"$$$$$$$\                      $$\ $$\ ",
          u"$$  __$$\                     $$ |$$ | ",
          u"$$ |  $$ | $$$$$$\  $$\   $$\ $$ |$$ | ",
          u"$$$$$$$\ |$$  __$$\ $$ |  $$ |$$ |$$ | ",
          u"$$  __$$\ $$ /  $$ |$$ |  $$ |\__|\__| ",
          u"$$ |  $$ |$$ |  $$ |$$ |  $$ | ",
          u"$$$$$$$  |\$$$$$$  |\$$$$$$$ |$$\ $$\ ",
          u"\_______/  \______/  \____$$ |\__|\__| ",
          u"                    $$\   $$ | ",
          u"                    \$$$$$$  | ",
          u"                     \______/ "]
girlstr = [u"$$$$$$\ $$\  $$\ ",
           u"\_$$  _|$$ | $  | ",
           u"  $$ |$$$$$$\\_/ $$$$$$$\        $$$$$$\ ",
           u"  $$ |\_$$  _|  $$  _____|       \____$$\ ",
           u"  $$ |  $$ |    \$$$$$$\         $$$$$$$ |",
           u"  $$ |  $$ |$$\  \____$$\       $$  __$$ |",
           u"$$$$$$\ \$$$$  |$$$$$$$  |      \$$$$$$$ |",
           u"\______| \____/ \_______/        \_______|",
           u"",
           u" $$$$$$\  $$\           $$\ $$\ $$\ ",
           u"$$  __$$\ \__|          $$ |$$ |$$ |",
           u"$$ /  \__|$$\  $$$$$$\  $$ |$$ |$$ |",
           u"$$ |$$$$\ $$ |$$  __$$\ $$ |$$ |$$ |",
           u"$$ |\_$$ |$$ |$$ |  \__|$$ |\__|\__|",
           u"$$ |  $$ |$$ |$$ |      $$ |",
           u"\$$$$$$  |$$ |$$ |      $$ |$$\ $$\ ",
           u" \______/ \__|\__|      \__|\__|\__|"]

lemlsta = [u"                                _,.            ",
           u"                           _,::' ':)           ",
           u"                         ,'  ::_.-'            ",
           u"                        /::.,\"'               ",
           u"                       :  `:                   ",
           u"                        :   :                  ",
           u"                        \\.:::._               ",
           u"                          `:'   `-.            ",
           u"                            `._..:::.          ",
           u"                               `:::''\\        ",
           u"                                 \\    \\      ",
           u"                                  :::..:       ",
           u"                                  |''::|       ",
           u"                                  ;    |       ",
           u"_                    ______      /::.  ;       ",
           u"\\`-...._,\\   __  _.-':.:. .''-.,''::::/      ",
           u" \\/::::|,/:-':.`':. . .   .  . `.  ';'        ",
           u" :\\ '/ `'.\\::. ..  .             \\ /        ",
           u" :o|/o) _-':.    \\    .  .-'  .   /           ",
           u"  \\_`.,.' `-._.   \\     /.  .    /           ",
           u"   `-' `.     \\.   \\   /. .    ,'            ",
           u"         `._   \\.   \\_/..     /|             ",
           u"          /.`;-->'  / |.    ,'.:               ",
           u"         :. /  /.  /  :.   :\\ .\\             ",
           u"         | /  :.  /    :.  | \\  \\            ",
           u"         ;_\\  |  /     :.  |  `, |            ",
           u"       ,//_`__; /    __.\\  |,-',|;            "]
lemlstb = [u"                                _,.            ",
           u"                           _,::' ':)           ",
           u"                         ,'  ::_.-'            ",
           u"                        /::.,\"'               ",
           u"                       :  `:                   ",
           u"                        :   :                  ",
           u"                        \\.:::._               ",
           u"                          `:'   `-.            ",
           u"                            `._..:::.          ",
           u"                               `:::''\\        ",
           u"                                 \\    \\      ",
           u"                                  :::..:       ",
           u"                                  |''::|       ",
           u"                                  ;    |       ",
           u"_                    ______      /::.  ;       ",
           u"\\`-...._,\\   __  _.-':.:. .''-.,''::::/      ",
           u" \\/::::|,/:-':.`':. . .   .  . `.  ';'        ",
           u" :\\ '/ `'.\\::. ..  .             \\ /        ",
           u" :o|/o) _-':.    \\    .  .-'  .   /           ",
           u"  \\_`.,.' `-._.   \\     /.  .    /           ",
           u"   `-' `.       .   \\   /. .    ,'            ",
           u"         `._-    .   \\_/..     /|             ",
           u"       __ /.`   >'__/    /|.    ,'             ",
           u"     ,:  _::__/_        /  :.   :              ",
           u"   ,/,,/   \\  \\      :  / :.  |              ",
           u"             \\  :    ,'  ;  :.  |,            ",
           u"             ,/_,:  ,,_ /   __.\\ /           "]
dglist = [u"          ▄              ▄ ",
          u"         ▌▒█           ▄▀▒▌",
          u"         ▌▒▒█        ▄▀▒▒▒▐ ",
          u"        ▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐ ",
          u"      ▄▄▀▒░▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐ ",
          u"   ▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▒▌",
          u"  ▐▒▒▒▄▄▒▒▒▒░░░▒▒▒▒▒▒▒▀▄▒▒▒▌",
          u"  ▌░░▌█  ▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▒▐ ",
          u" ▐░░░▒▒▒▒▒▒▒▒▌█  ▒▒░░░▒▒▒▀▄▒▒▌",
          u" ▌░▒▄██▄▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▒▒▌",
          u" ▀▒▀▐▄█▄█▌▄░▀▒▒░░░░░░░░░░▒▒▒▐ ",
          u"▐▒▒▐▀▐▀▒░▄▄▒▄▒▒▒▒▒▒░▒░▒░▒▒▒▒▌",
          u"▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒▒▒░▒░▒░▒▒▐ ",
          u" ▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒░▒░▒░▒░▒▒▒▌",
          u" ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▄▒▒▐ ",
          u"  ▀▄▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▄▒▒▒▒ ",
          u"    ▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀ ",
          u"      ▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀ ",
          u"         ▒▒▒▒▒▒▒▒▒▒▀▀ "]

storklst = [u"             _.--.",
            u"           .-\"`_.--.\   .-.___________ ",
            u"         .\"_-\"`     \\ (  0;------/\\\"'` ",
            u"       ,.\"=___      =)) \\ \\      /  \\   ,==. ",
            u"        `~` .=`~'~)  ( _/ /     /    \\ /  99\\ ",
            u"=`---====\"\"~`\\          _/     /      \\\\c  -_) ",
            u"              `-------\"`      /        \\`) ( ",
            u"                             /             \\ ",
            u"                            (               ) ",
            u"                             '._         _.' ",
            u"                                '-------' " ]

def mk_arch_fn(max_steps, go_right, curvature):
    step_size = math.pi / SCR_WIDTH
    if go_right:
        xdir = 1
    else:
        xdir = -1
    return lambda t, y, x: (y-math.sin(step_size*min(t,max_steps))*curvature,
                            x+xdir*min(t,max_steps))

def mk_appear_fn(max_steps,direction,step_size=1):
    if direction == FROM_BELOW:
        return lambda t, y, x: (y-min(t,max_steps)*step_size, x)
    elif direction == FROM_ABOVE:
        return lambda t, y, x: (y+min(t,max_steps)*step_size, x)
    elif direction == FROM_LEFT:
        return lambda t, y, x: (y, x+min(t,max_steps)*step_size)
    else:
        return lambda t, y, x: (y, x-min(t,max_steps)*step_size)

def shake(t,y,x):
    if t % 2 == 1:
        return (y-1,x)
    else:
        return (y,x)


def doge_saying():
    first_word = ['wow','such','much','so','very']
    second_word = ['mass','responsibility','baby','parenting','newborn','cute','diaper','weight','bundle','pamper','feeding','goochy-goo']
    f = randrange(len(first_word))
    s = randrange(len(second_word))
    if f == 0:
        return first_word[f]
    else:
        return ' '.join((first_word[f],second_word[s]))


def make_mirror_lights(chr1, chr2):
    top = "".join((chr1, " ", chr2, " ") * int(SCR_WIDTH/4))
    bottom = "".join((chr2, " ", chr1, " ") * int(SCR_WIDTH/4))
    mid_a = "".join((chr2, " "*(SCR_WIDTH-4), chr1))
    mid_b = "".join((chr1, " "*(SCR_WIDTH-4), chr2))
    lst = []
    lst.append(top)
    for i in range(0,int((SCR_HEIGHT-2)/2)):
        lst.append(mid_a)
        lst.append(mid_b)
    lst.append(bottom)
    return lst

mirrorlsta = make_mirror_lights(u'♡',u'☺')
mirrorlstb = make_mirror_lights(u'☺',u'♡')


class Sprite(object):

    def __init__(self, parent, strlist, begin_y, begin_x,
                 update_dt, mv_fn=None):
        self.parent = parent
        self.strlist = strlist
        self.begin_y = float(begin_y)
        self.begin_x = float(begin_x)
        self.curr_y = begin_y
        self.curr_x = begin_x
        self.mv_fn = mv_fn
        self.movements = 0
        self.draws = 0
        self.update_dt = update_dt
        self.done = False
        self.callbacks = []
        self.hit = False

    def draw_next(self, seq):
        self.draws += 1
        if self.draws % self.update_dt == 0:
            # move
            if self.mv_fn is not None:
                (y, x) = self.mv_fn(self.movements, self.begin_y, self.begin_x)
                self.curr_y = int(y)
                self.curr_x = int(x)
            self.movements += 1
        for i in range(0, len(self.strlist)):
            self.parent.addstr(int(self.curr_y)+i, int(self.curr_x), self.strlist[i].encode('utf-8'))
        for i in range(0, len(self.callbacks)):
            self.callbacks[i]()


class Sequencer(Thread):
    def __init__(self, stdscr, data):
        Thread.__init__(self)
        self.daemon = True

        self.stdscr = stdscr
        self.data = data
        self.sprites = []
        self.time = 0
        self.done = False
        self.bgpad = curses.newpad(PAD_HEIGHT, PAD_WIDTH)
        self.debug = True
        self.dbgwin = curses.newwin(1, SCR_WIDTH, SCR_Y, SCR_X)
        self.starchr = '.'

        self.sat1 = None
        self.sat2 = None
        self.sat3 = None
        self.stars = None
        self.shaky = None
        self.boy = None
        self.doge = None
        self.such = None
        self.lemur = None
        self.blink1 = None
        self.blink2 = None
        self.mirror = None
        self.stork = None
        self.pew = None
        self.do_check_hit = True
        self.score = DEFAULT_SCORE

        try:
            bday_utc = datetime.strptime(self.data["birth_time_UTC"],
                                         '%Y-%m-%d %H:%M')
            offset = datetime.utcnow() - datetime.now()
            self.bday_local = bday_utc - offset
            self.offset_hours = round((offset.days * 86400 * 10E6 + offset.seconds * 10E6 + offset.microseconds) / (3600.0 * 10E6))
            self.nfirst = self.data["name"]["first"]
            self.nmiddle = self.data["name"]["middle"]
            self.nlast = self.data["name"]["last"]
            self.chinese = None
            if "chinese" in self.data["name"]:
                self.chinese = self.data["name"]["chinese"]
            self.isboy = self.data["is_boy"]
            self.mass_kg = self.data["mass_kg"]
            lbs_total = self.mass_kg/0.45359237
            self.lbs = int(math.floor(lbs_total))
            self.oz = int((lbs_total - self.lbs) * 16)
            self.imperial = self.data["imperial"]
            self.height_cm = self.data["height_cm"]
            self.height_in = self.height_cm * 0.393701

        except KeyError:
            curses.endwin()
            print("Missing or unparseable data in %s!" % FILENAME)
            sys.exit()
        self.start()

    def run(self):
        while not self.done:
            c = self.bgpad.getch()
            if c in (ord('q'), ord('Q')):
                self.done = True
            elif self.time < 650:
                if self.pew is None:
                    self.pew = Sprite(self.bgpad, [u'•'],
                                      PAD_GUTTER+SCR_HEIGHT,
                                      PAD_GUTTER+SCR_WIDTH/2, 5,
                                      mk_appear_fn(SCR_HEIGHT+1,FROM_BELOW))
                    self.sprites.append(self.pew)

    def print_dbg(self, str):
        if self.debug:
            self.dbgwin.addstr(0, 0, str)

    def check_hit(self):
        if self.pew is None:
            return
        for sat in [self.sat1, self.sat2, self.sat3]:
            if sat is not None and not sat.hit and \
               self.pew.curr_y in range(sat.curr_y-1,sat.curr_y+4) and \
               self.pew.curr_x in range(sat.curr_x-1,sat.curr_x+6):
                sat.begin_y = sat.curr_y
                sat.begin_x = sat.curr_x
                sat.movements = 0
                sat.hit = True
                sat.strlist=[' ___ _____      ___',
                             '| _ \ __\ \    / / |',
                             '|  _/ _| \ \/\/ /|_|',
                             '|_| |___| \_/\_/ (_)']
                self.starchr = u'★'
                sat.mv_fn=mk_appear_fn(SCR_HEIGHT+PAD_GUTTER-sat.curr_y+1,FROM_ABOVE)
                self.score = (self.score + (PAD_GUTTER + SCR_HEIGHT - sat.curr_y)) ** 2

    def seq(self):
        #self.print_dbg("%s" % self.time)
        #key = self.stdscr.getch()

        if self.do_check_hit:
            self.check_hit()

        if self.time == 0:
            self.stars = Sprite(self.bgpad, [],
                                PAD_GUTTER, PAD_GUTTER,
                                1, None)
            self.sprites.append(self.stars)
        elif self.time < 100:
            rand_y = randrange(PAD_GUTTER, PAD_GUTTER+SCR_HEIGHT)
            rand_x = randrange(PAD_GUTTER, PAD_GUTTER+SCR_WIDTH)
            add = lambda: self.bgpad.addstr(rand_y, rand_x, self.starchr.encode('utf-8'))
            self.stars.callbacks.append(add)
        elif self.time == 100:
            # add satellite.
            self.sat1 = Sprite(self.bgpad, ['\\', u' ███', '/'],
                               PAD_GUTTER+randrange(5,25), PAD_GUTTER, 6,
                               mk_arch_fn(SCR_WIDTH+4, True, randrange(0,10)))
            self.sprites.append(self.sat1)

        elif self.time == 150:
            # add another satellite
            self.sat2 = Sprite(self.bgpad, ['    /', u'███', '    \\'],
                               PAD_GUTTER+randrange(10,40),
                               PAD_GUTTER+SCR_WIDTH-1,
                               6, mk_arch_fn(SCR_WIDTH+4, False, randrange(0,10)))
            self.sprites.append(self.sat2)
            self.sat3 = Sprite(self.bgpad, ['\\', u' ███', '/'],
                               PAD_GUTTER+randrange(15,30),
                               PAD_GUTTER,
                               6, mk_arch_fn(SCR_WIDTH+4, True, randrange(0,10)))
            self.sprites.append(self.sat3)

        elif self.time == 400:
            self.boy = Sprite(self.bgpad, boystr if self.isboy else girlstr,
                              0, PAD_GUTTER+15,
                              7, mk_appear_fn(36, FROM_ABOVE))
            self.sprites.append(self.boy)
        elif self.time == 650:
            self.do_check_hit = False
            self.stars.done = True
            self.sat1.done = True
            self.sat2.done = True
            self.sat3.done = True
            shakyrowa = u"░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░ "
            shakyrowb = u" ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░  ░"
            shakylist = []
            for row in range(0,SCR_HEIGHT):
                if row % 2 == 1:
                    shakylist.append(shakyrowa)
                else:
                    shakylist.append(shakyrowb)

            self.shaky = Sprite(self.bgpad, shakylist,
                                PAD_GUTTER, PAD_GUTTER,
                                10, shake)
            self.sprites.insert(0,self.shaky)
        elif self.time == 800:
            self.boy.done = True
            self.shaky.done = True
            self.lemur = Sprite(self.bgpad, lemlsta,
                                 PAD_GUTTER-5,
                                 PAD_GUTTER+SCR_WIDTH-10,
                                 20, mk_appear_fn(9, FROM_RIGHT,4))
            self.sprites.append(self.lemur)
        elif self.time > 800 and self.time <= 980:
            if self.time % 20 == 0:
                if self.time % 40 == 0:
                    self.lemur.strlist = lemlsta
                else:
                    self.lemur.strlist = lemlstb
        elif self.time == 981:
            intro = 'INTRODUCING %s %s %s' % (self.nfirst, self.nmiddle, self.nlast)
            if self.chinese is not None:
                intro += ' (%s)' % self.chinese
            add = lambda: self.bgpad.addstr(PAD_GUTTER+SCR_HEIGHT-10,
                                            PAD_GUTTER+10,
                                            intro.encode('utf-8'))

            add2 = lambda: self.bgpad.addstr(PAD_GUTTER+SCR_HEIGHT-8,
                                             PAD_GUTTER+10,
                                             'Born %s (UTC%+d)' % (self.bday_local.strftime("%A, %B %d, at %I:%M %p"), -self.offset_hours))
            self.lemur.callbacks.append(add)
            self.lemur.callbacks.append(add2)
        elif self.time == 1300:
            self.lemur.done = True
            self.doge = Sprite(self.bgpad, dglist,
                               PAD_GUTTER+SCR_HEIGHT, PAD_GUTTER+SCR_WIDTH-28,
                               5, mk_appear_fn(19, FROM_BELOW))
            self.sprites.append(self.doge)

        elif self.time == 1400:
            suchlst = [u"┌───────────────────────────────────────┐",
                       u"│                                       │",
                       u"│                                       │",
                       u"│                                       │",
                       u"│                                       │",
                       u"└──────────────────────────────────╲|───┘"]
            self.such = Sprite(self.bgpad, suchlst,
                               PAD_GUTTER-8, PAD_GUTTER+5,
                               1, mk_appear_fn(20, FROM_ABOVE))
            self.sprites.append(self.such)
        elif self.time == 1440:
            if self.imperial:
                massstr = "%s lbs %s oz " % (self.lbs, self.oz)
                heightstr = "%.1f inches" % self.height_in
            else:
                massstr = "%s kg" % self.mass_kg
                heightstr = "%s cm" % self.height_cm
            add = lambda: self.bgpad.addstr(PAD_GUTTER+14, PAD_GUTTER+12,
                                            "Weighing in at %s" % massstr)
            add2 = lambda: self.bgpad.addstr(PAD_GUTTER+15, PAD_GUTTER+12,
                                             "Height is %s" % heightstr)
            self.such.callbacks.append(add)
            self.such.callbacks.append(add2)
        elif self.time == 1500:
            y = randrange(PAD_GUTTER, PAD_GUTTER+10)
            x = randrange(PAD_GUTTER+1, PAD_GUTTER+SCR_WIDTH-10)
            s1 = doge_saying()
            add = lambda: self.bgpad.addstr(y, x, s1)
            self.doge.callbacks.append(add)
        elif self.time == 1550:
            y = randrange(PAD_GUTTER+SCR_HEIGHT-8, PAD_GUTTER+SCR_HEIGHT-1)
            x = randrange(PAD_GUTTER+1, PAD_GUTTER+SCR_WIDTH-46)
            s2 = doge_saying()
            add = lambda: self.bgpad.addstr(y, x, s2)
            self.doge.callbacks.append(add)
        elif self.time == 1600:
            y = randrange(PAD_GUTTER+20, PAD_GUTTER+SCR_HEIGHT-8)
            x = randrange(PAD_GUTTER+1, PAD_GUTTER+SCR_WIDTH-46)
            s3 = doge_saying()
            add = lambda: self.bgpad.addstr(y, x, s3)
            self.doge.callbacks.append(add)
        elif self.time == 1610:
            self.blink1 = lambda: self.bgpad.addstr(PAD_GUTTER+SCR_HEIGHT-12,
                                                    PAD_GUTTER+SCR_WIDTH-22,
                                                    u"▒▒▒".encode('utf-8'))
            self.blink2 = lambda: self.bgpad.addstr(PAD_GUTTER+SCR_HEIGHT-11,
                                                    PAD_GUTTER+SCR_WIDTH-14,
                                                    u"▒▒▒".encode('utf-8'))
            self.doge.callbacks.append(self.blink1)
            self.doge.callbacks.append(self.blink2)
        elif self.time == 1620:
            self.doge.callbacks.remove(self.blink1)
            self.doge.callbacks.remove(self.blink2)
        elif self.time == 1635:
            self.doge.callbacks.append(self.blink1)
            self.doge.callbacks.append(self.blink2)
        elif self.time == 1645:
            self.doge.callbacks.remove(self.blink1)
            self.doge.callbacks.remove(self.blink2)
        elif self.time == 1700:
            self.doge.done = True
            self.such.done = True
            self.mirror = Sprite(self.bgpad, mirrorlsta,
                                 PAD_GUTTER,
                                 PAD_GUTTER,
                                 1, None)
            self.sprites.append(self.mirror)
        elif self.time > 1700 and self.time <= 2400:
            if self.time == 1701:
                add = lambda: self.bgpad.addstr(PAD_GUTTER+10,
                                                PAD_GUTTER+16,
                                                "Mommy and baby are doing just fine.")
                self.mirror.callbacks.append(add)
            if self.time == 1801:
                add = lambda: self.bgpad.addstr(PAD_GUTTER+12,
                                                PAD_GUTTER+5,
                                                "Daddy is changing diapers and writing silly python programs.")
                self.mirror.callbacks.append(add)
            if self.time == 1901:
                add = lambda: self.bgpad.addstr(PAD_GUTTER+14,
                                                PAD_GUTTER+18,
                                                "WE CAN'T WAIT TO SEE YOU SOON!")
                self.mirror.callbacks.append(add)
            if self.time == 2001:
                self.stork = Sprite(self.bgpad, storklst,
                                    PAD_GUTTER+18,
                                    0, 3, mk_appear_fn(105, FROM_LEFT))
                self.sprites.append(self.stork)
            if self.time % 30 == 0:
                if self.time % 60 == 0:
                    self.mirror.strlist = mirrorlsta
                else:
                    self.mirror.strlist = mirrorlstb
        elif self.time > 2400:
            self.done = True
        self.time += 1

    def draw_next(self):
        self.bgpad.clear()
        self.seq()
        self.sprites = [s for s in self.sprites if not s.done]
        if len(self.sprites) > 0:
            for i in range(0, len(self.sprites)):
                self.sprites[i].draw_next(self)
        self.bgpad.refresh(PAD_GUTTER, PAD_GUTTER, SCR_Y, SCR_X,
                           SCR_HEIGHT, SCR_WIDTH)
        if self.debug:
            self.dbgwin.refresh()
        sleep(FRAME_TIME_S)




### MAIN ROUTINE

if __name__ == '__main__':

    try:
        f = open(FILENAME, "r")
        fdata = json.load(f)
    except IOError:
        print("Cannot find %s in directory!" % FILENAME)
        sys.exit(1)
    except ValueError:
        print("File %s is not parseable!" % FILENAME)
        f.close()
        sys.exit(1)

    stdscr = curses.initscr()
    y, x = stdscr.getmaxyx()
    if y < SCR_HEIGHT or x < SCR_WIDTH:
        curses.endwin()
        print("sorry, your terminal size is not large enough to display this.")
        sys.exit(0)
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak()
    stdscr.keypad(1)

    sequencer = Sequencer(stdscr,fdata)

    try:
        while not sequencer.done:
            sequencer.draw_next()
    except curses.error:
        curses.endwin()
        print("sorry, your terminal size no longer supports the display of this program.")
        sys.exit(0)

    curses.endwin()

    print("congrats %s, your downlink score is %s!\n" % (getuser(),sequencer.score))
