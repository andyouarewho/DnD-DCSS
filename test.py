import libtcodpy as libtcod
import random

#####################
### CONSOLE STUFF ###
#####################

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60
LIMIT_FPS = 20
BG_COLOR = libtcod.darkest_gray
FG_COLOR = libtcod.lightest_gray

loremipsum = """
    Lorem ipsum dolor sit amet, metus rutrum non libero ultrices pharetra,
euismod quam lacus semper accumsan. Nunc maecenas cum, vestibulum mattis,
mauris viverra malesuada orci proin, ut etiam magna at vestibulum nec sit.
Tristique eu ut porttitor porta tristique maecenas. Vulputate orci, tincidunt
ut curae sed mauris feugiat, sed dolor wisi pede consectetuer montes.
Ut luctus, enim praesent, fringilla porta maecenas. Rutrum sit est diam ut,
etiam metus, risus felis aliquam tellus, elit neque tincidunt vitae, mollis eu.

    Nullam mi urna rutrum pulvinar, mollis nulla wisi aliquam elit, nisl quam
ullamcorper rutrum risus arcu metus, potenti lectus in, vestibulum lacinia
condimentum quis. Aliquam etiam id a lorem amet lacus, dolor curabitur lectus,
magna lectus auctor et varius, arcu arcu, orci donec vitae et magna torquent
sit. Mi quam, pede imperdiet auctor libero maecenas sed at, interdum proin sit
libero ac vestibulum. Ac orci, euismod bibendum a, convallis vel, nunc dui eget
malesuada volutpat. In vestibulum sit scelerisque, nulla in nec purus nunc
nulla, diam magni ea eum ante proin, sit ut viverra, lacinia turpis ut.
"""
teststring = """
This is a test string in order to test things.
"""


# temp function for input
def controls():
    this = libtcod.console_check_for_keypress(True)
    if this.vk == libtcod.KEY_ESCAPE:
#    if libtcod.console_is_key_pressed(libtcod.KEY_ESCAPE):
        return True
    if this.vk == libtcod.KEY_ENTER:
#    if libtcod.console_is_key_pressed(libtcod.KEY_ENTER):
        for _ in range(10):
            newRoom = Rect(random.randint(1, SCREEN_WIDTH), random.randint(1, SCREEN_HEIGHT), random.randint(3, 10), random.randint(3, 10))
            if newRoom.x2 < SCREEN_HEIGHT and newRoom.y2 < SCREEN_HEIGHT:
                for x in range(newRoom.x1, newRoom.x2):
                    for y in range(newRoom.y1, newRoom.y2):
                        map[x][y].block_sight = False
                        map[x][y].blocked = False
        render_all()



def make_map():
    global map
    map = [[Tile(True) # magic! Make a list of classes inside a list.
            for y in range(SCREEN_HEIGHT)]
                for x in range(SCREEN_WIDTH)]

def render_all(): # draw to the screen
    libtcod.console_clear(0)
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(0, x, y, libtcod.darkest_gray)
            else:
                libtcod.console_set_char_background(0, x, y, libtcod.dark_gray)



# define a room class
class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        center = ((x + w)/2, ((y + h)/2))
# define a tile class (a cell in the X, Y grid/array)
class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.block_sight = block_sight
        if self.block_sight is None:
            self.block_sight = blocked




### Pre Game Init/Console Stuff ###
libtcod.console_set_custom_font('mann.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD) # set console font
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'mann_game', False) # initialize the window with attributes (width, height, title, fullscreen boolean)
libtcod.console_set_default_background(0, BG_COLOR) # default background is black but you can change it
libtcod.console_set_default_foreground(0, FG_COLOR) # default foreground is white but you can change it
libtcod.console_clear(0) # clear console so BG/FG colors can change
libtcod.console_print(0, 0, 0, loremipsum) # print test string for font preview CAN DELETE ME
make_map() # this is the shit right here -- this is the game world
### MAIN GAME LOOP MOTHERFUCKER ###
while not libtcod.console_is_window_closed():
    libtcod.console_flush()
    if controls() == True: # can simplify but only here to clarify logic of statment
        break
