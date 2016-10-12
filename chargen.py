"""Character Generator"""
import random

class Character():
    def __init__(self, race = None, profession = None, strength=0, intelligence=0, dexterity=0):
        self.race = race
        self.profession = profession
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity
    def __repr__(self):
    	return '{} {}'.format(self.race, self.profession)


class Race():
    def __init__(self, racename='Unknown', strmod=0, intmod=0, dexmod=0):
        self.racename = racename
        self.strmod = strmod
        self.intmod = intmod
        self.dexmod = dexmod
    def __repr__(self):
    	return self.racename


class Profession():
    def __init__(self, profname='Unknown', strmod=0, intmod=0, dexmod=0):
        self.profname = profname
        self.strmod = strmod
        self.intmod = intmod
        self.dexmod = dexmod
    def __repr__(self):
    	return self.profname

def random_roll_race():
    r = {
        1 : 'human',
        2 : 'kobold',
        3 : 'dwarf',
        4 : 'elf',
        5 : 'orc'
        }
    x = r[random.randint(1, 5)]
    return x
def random_roll_prof():
    r = {
        1 : 'fighter',
        2 : 'wizard'
        }
    y = r[random.randint(1, 2)]
    return y

def stat_fix(bob): # SLOPPY WAY TO FIX LOW STAT CONDITION
    if bob.strength < 3:
        roll = random.randint(1, 100)
        if roll < 50:
            bob.strength += 1
            bob.dexterity -= 1
        else:
            bob.strength += 1
            bob.intelligence -= 1
    elif bob.intelligence < 3:
        roll = random.randint(1, 100)
        if roll < 50:
            bob.intelligence += 1
            bob.dexterity -= 1
        else:
            bob.intelligence += 1
            bob.strength -= 1
    elif bob.dexterity < 3:
        roll = random.randint(1, 100)
        if roll < 50:
            bob.dexterity += 1
            bob.intelligence -= 1
        else:
            bob.dexterity += 1
            bob.strength -= 1
    else:
        None

RACES = {
    'human' : Race(racename='human', strmod=6, intmod=6, dexmod=6),
    'kobold' : Race(racename='kobold', strmod=5, intmod=4, dexmod=8),
    'dwarf' : Race(racename='dwarf', strmod=9, intmod=6, dexmod=6),
    'elf' : Race(racename='elf', strmod=3, intmod=10, dexmod=8),
    'orc' : Race(racename='orc', strmod=8, intmod=6, dexmod=4)
    }


PROFESSIONS = {
    'fighter' : Profession(profname='fighter', strmod=8, intmod=0, dexmod=4),
    'wizard' : Profession(profname='wizard', strmod=-1, intmod=10, dexmod=3)
    }


john = Character(RACES[random_roll_race()], PROFESSIONS[random_roll_prof()])
john.strength += john.race.strmod + john.profession.strmod
john.intelligence += john.race.intmod + john.profession.intmod
john.dexterity += john.race.dexmod + john.profession.dexmod
stat_fix(john)
print str.upper(john.race.racename), str.upper(john.profession.profname)
print 'STR:', john.strength, 'INT:', john.intelligence, 'DEX:', john.dexterity
