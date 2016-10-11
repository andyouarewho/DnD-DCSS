import random


def human(player):
    player.strength += 6
    player.intelligence += 6
    player.dexterity += 6
    player.race_name = 'human'
def kobold(player):
    player.strength += 5
    player.intelligence += 4
    player.dexterity += 8
    player.race_name = 'kobold'
def dwarf(player):
    player.strength += 9
    player.intelligence += 6
    player.dexterity += 6
    player.race_name = 'dwarf'
def deep_elf(player):
    player.strength += 3
    player.intelligence += 10
    player.dexterity += 8
    player.race_name = 'deep elf'
def orc(player):
    player.strength += 8
    player.intelligence += 6
    player.dexterity += 8
    player.race_name = 'orc'


def fighter(player):
    player.strength += 8
    player.dexterity += 4
    player.profession_name = 'fighter'
def wizard(player):
    player.strength -= 1
    player.intelligence += 10
    player.dexterity += 3
    player.profession_name = 'wizard'


class NewPlayer(object):
    def __init__(self):
        self.strength = 0
        self.intelligence = 0
        self.dexterity = 0
        self.race_name = None
        self.race = None
        self.profession_name = None
        self.profession = None
        racelist = [
            human, kobold, dwarf, deep_elf, orc
            ]
        proflist = [
            fighter, wizard
        ]
        blah = random.randint(0, len(racelist)-1)
        blarg = random.randint(0, 1)
        plop = racelist[blah]
        plop(self)
        plank = proflist[blarg]
        plank(self)


bob = NewPlayer()


print bob.strength, bob.intelligence, bob.dexterity,
print bob.race_name, bob.profession_name
