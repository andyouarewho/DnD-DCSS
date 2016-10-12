"""Generate a random dungeon for the game."""

import random

import tdl

#####################
### CONSOLE STUFF ###
#####################

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60
MAX_ROOMS = 6
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 12
LIMIT_FPS = 20
BG_COLOR = (30, 30, 30)
FG_COLOR = (200, 200, 200)
LOREM_IPSUM = """
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

# temp function for input
def controls():
    this = tdl.event.key_wait() # wait for keypress

    if this.key == 'ESCAPE': # quit game
        return True
    elif this.key == '0': # fullscreen mode
        tdl.console_set_fullscreen(not tdl.console_is_fullscreen())
    if this.key == 'ENTER':
        make_map() # resets console so each enter key is a new map
        basic_map_generator() # dungeon generator code
        render_all() # draw current rendition of map
        for obj in GAME_OBJECTS:
            obj.clear() # clears all GAME_OBJECTS
        for obj in GAME_OBJECTS:
            obj.draw() # draws all GAME_OBJECTS

# Make the game map array
def make_map():
    """Make the game map array."""
    global map
    map = [[Tile(True) # magic! Make a list of classes inside a list.
            for y in range(SCREEN_HEIGHT)]
                for x in range(SCREEN_WIDTH)]


def basic_map_generator():
    rooms = []
    num_rooms = 0
    iterations = 0
    while num_rooms < MAX_ROOMS:
        iterations += 1 # make me incapable of breaking based on max room size
        if iterations > 1000:
            break
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(1, SCREEN_WIDTH - w - 1)
        y = random.randint(1, SCREEN_HEIGHT - h - 1)
        newRoom = Rect(x, y, w, h)
        if num_rooms == 0:
            create_room(newRoom)
            entrance.x = newRoom.centerx
            entrance.y = newRoom.centery
            rooms.append(newRoom)
            num_rooms += 1
        else:
            if not newRoom.intersects(rooms):
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
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
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


def render_all():
    """draw to the screen"""
    CONSOLE.clear()
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                CONSOLE.draw_char(x, y, 'X', fg=FG_COLOR)
            else:
                CONSOLE.draw_char(x, y, ' ', fg=BG_COLOR)


class Rect:
    """define a room class"""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.centerx = int((self.x1 + self.x2) / 2)
        self.centery = int((self.y1 + self.y2) / 2)
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)
    def intersects(self, others):
        for other_room in others:
            if self.intersect(other_room):
                return True
        return False


class Tile:
    """define a tile class (a cell in the X, Y grid/array)"""
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.block_sight = block_sight
        if self.block_sight is None:
            self.block_sight = blocked
    def __repr__(self):
        return '<Tile blocked={}>'.format(self.blocked)


class GameObject:
    """define any object, player, npc, monster, item, etc."""
    def __init__(self, x, y, char, color=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    def draw(self):
        CONSOLE.set_colors(fg=self.color)
        CONSOLE.draw_char(self.x, self.y, self.char)
    def clear(self):
        CONSOLE.draw_char(self.x, self.y, ' ')


### Pre Game Init/Console Stuff ###
# TODO -- get this font to work again
# tdl.set_font('mann.png', rows=32, columns=7) # set console font

CONSOLE = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='mann_game')
CONSOLE.set_colors(fg=FG_COLOR, bg=BG_COLOR)
CONSOLE.clear() # clear console so BG/FG colors can change
CONSOLE.move(0, 0)
CONSOLE.print_str(LOREM_IPSUM) # TODO -- get this working again

make_map() # this is the shit right here -- this is the game world
entrance = GameObject(0, 0, '<')
exit = GameObject(0, 1, '>')
GAME_OBJECTS = [entrance, exit]

### MAIN GAME LOOP MOTHERFUCKER ###
while True:
    tdl.flush()
    if controls() == True:
        break
