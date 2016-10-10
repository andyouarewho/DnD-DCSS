import libtcodpy as libtcod
import random

#####################
### CONSOLE STUFF ###
#####################

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60
MAX_ROOMS = 6
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 12
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
    this = libtcod.console_check_for_keypress(True) # wait for keypress
    if this.vk == libtcod.KEY_ESCAPE: # quit game
        return True
    elif this.vk == libtcod.KEY_0: # fullscreen mode
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    if this.vk == libtcod.KEY_ENTER:
        make_map() # resets console so each enter key is a new map
        basic_map_generator() # dungeon generator code
        render_all() # draw current rendition of map
        for object in objects:
            object.clear # clears all objects
        for object in objects:
            object.draw() # draws all objects

# Make the game map array
def make_map():
    global map
    map = [[Tile(True) # magic! Make a list of classes inside a list.
            for y in range(SCREEN_HEIGHT)]
                for x in range(SCREEN_WIDTH)]

def basic_map_generator():
    rooms = []
    num_rooms = 0
    while num_rooms < MAX_ROOMS:
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(1, SCREEN_WIDTH - w - 1)
        y = random.randint(1, SCREEN_HEIGHT - h - 1)
        if num_rooms == 0:
            newRoom = Rect(x, y, w, h)
            create_room(newRoom)
            entrance.x = newRoom.centerx
            entrance.y = newRoom.centery
            rooms.append(newRoom)
            num_rooms += 1
        else:
            newRoom = Rect(x, y, w, h)
            other_room = rooms[num_rooms - 1]
            if newRoom.intersect(other_room):
                continue
            else:
                create_room(newRoom)
                prev_x = rooms[num_rooms - 1].centerx
                prev_y = rooms[num_rooms - 1].centery
                new_x = newRoom.centerx
                new_y = newRoom.centery
                chance = random.randint(1, 100)
                if chance <= 50:
                    create_h_tunnel(prev_y, prev_x, new_x)
                    create_v_tunnel(new_x, prev_y, new_y)
                else:
                    create_h_tunnel(new_y, prev_x, new_x)
                    create_v_tunnel(prev_x, prev_y, new_y)
                rooms.append(newRoom)
                num_rooms += 1
    if num_rooms == MAX_ROOMS:
        exit.x = rooms[MAX_ROOMS - 1].centerx
        exit.y = rooms[MAX_ROOMS - 1].centery

def create_room(room):
    global map
    for x in range(room.x1, room.x2):
        for y in range(room.y1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(y, x1, x2):
    global map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(x, y1, y2):
    global map
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

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
        self.centerx = int((self.x2 - self.x1) / 2 + self.x1)
        self.centery = int((self.y2 - self.y1) / 2 + self.y1)
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

# define a tile class (a cell in the X, Y grid/array)
class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.block_sight = block_sight
        if self.block_sight is None:
            self.block_sight = blocked

# define any object, player, npc, monster, item, etc.
class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    def draw(self):
        libtcod.console_set_default_foreground(0, self.color)
        libtcod.console_put_char(0, self.x, self.y, self.char, libtcod.BKGND_NONE)
    def clear(self):
        libtcod.console_put_char(0, self.x, self.y, ' ', libtcod.BKGND_NONE)


### Pre Game Init/Console Stuff ###
libtcod.console_set_custom_font('mann.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD) # set console font
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'mann_game', False) # initialize the window with attributes (width, height, title, fullscreen boolean)
libtcod.console_set_default_background(0, BG_COLOR) # default background is black but you can change it
libtcod.console_set_default_foreground(0, FG_COLOR) # default foreground is white but you can change it
libtcod.console_clear(0) # clear console so BG/FG colors can change
libtcod.console_print(0, 0, 0, loremipsum) # print test string for font preview CAN DELETE ME
make_map() # this is the shit right here -- this is the game world
entrance = Object(0, 0, '<', libtcod.lime)
exit = Object(0, 1, '>', libtcod.lime)
objects = [entrance, exit]
### MAIN GAME LOOP MOTHERFUCKER ###
while not libtcod.console_is_window_closed():
    libtcod.console_flush()
    if controls() == True: # can simplify but only here to clarify logic of statment
        break
