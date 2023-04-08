import numpy as np
import points as pt
from characters import barbarians, dragons, balloons, archers, starchers, healers
import king

class Building:
    def destroy(self, King=None):
        self.destroyed = True
        if self.type == 'wall':
            self.V.remove_wall(self)
            if self.level >= 3:
                troops = barbarians + archers + starchers
                for trp in troops:
                    if abs(trp.position[0] - self.position[0]) <= 2 and abs(trp.position[1] - self.position[1]) <= 2:
                        trp.deal_damage(200)
                if King != None:
                    if abs(King.position[0] - self.position[0]) <= 2 and abs(King.position[1] - self.position[1]) <= 2:
                        King.deal_damage(200)
        elif self.type == 'hut':
            self.V.remove_hut(self)
        elif self.type == 'cannon':
            self.V.remove_cannon(self)
        elif self.type == 'wizardtower':
            self.V.remove_wizard_tower(self)
        elif self.type == 'townhall':
            self.V.remove_town_hall(self)


class Hut(Building):
    def __init__(self, position, V, level):
        self.level = level
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 40 + 10 * level
        self.max_health = 40 + 10 * level
        self.type = 'hut'


class Cannon(Building):
    def __init__(self, position, V, level):
        self.level = level
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 60 + 30 * level
        self.max_health = 60 + 30 * level
        self.type = 'cannon'
        self.attack = 4 + level
        self.attack_radius = 5 + (level / 2)
        self.isShooting = False

    def scan_for_targets(self, King):
        self.isShooting = False

        troops = barbarians + archers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop)
                return

        for starch in starchers:
            if starch.visible == True and (starch.position[0] - self.position[0])**2 + (starch.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(starch)
                return

        if King.alive == False:
            return

        if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King)

    def attack_target(self, target):
        if(self.destroyed == True):
            return
        target.deal_damage(self.attack)


class Wall(Building):
    def __init__(self, position, V, level):
        self.level = level
        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 100 + 40 * level
        self.max_health = 100 + 40 * level
        self.type = 'wall'


class TownHall(Building):
    def __init__(self, position, V, level):
        self.level = level
        self.position = position
        self.dimensions = (4, 3)
        self.V = V
        self.destroyed = False
        self.health = 80 + 20 * level
        self.max_health = 80 + 20 * level
        self.type = 'townhall'


class WizardTower(Building):
    def __init__(self, position, V, level):
        self.level = level
        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 60 + 30 * level
        self.max_health = 60 + 30 * level
        self.type = 'wizardtower'
        self.attack = 4 + level
        self.attack_radius = 5 + (level / 2)
        self.isShooting = False

    def scan_for_targets(self, King):
        self.isShooting = False
        troops = barbarians+ archers + dragons + balloons + healers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop,0)
                return

        for starch in starchers:
            if starch.visible == True and (starch.position[0] - self.position[0])**2 + (starch.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(starch)
                return

        if King.alive == False:
            return

        if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King,1)

    def attack_target(self, target, isKing):
        if(self.destroyed == True):
            return

        if isKing == 1:
            target.deal_damage(self.attack)
        i = target.position[0] - 1
        j = target.position[1] - 1
        troops = barbarians+ archers + dragons + balloons + starchers + healers
        for row in range(i, i+3):
            for col in range(j, j+3):
                if(row < 0 or col < 0):
                    continue
                for troop in troops:
                    if(troop.position[0] == row and troop.position[1] == col):
                        troop.deal_damage(self.attack)


def shoot_cannons(King, V):
    for cannon in V.cannon_objs:
        V.cannon_objs[cannon].scan_for_targets(King)


def shoot_wizard_towers(King, V):
    for tower in V.wizard_tower_objs:
        V.wizard_tower_objs[tower].scan_for_targets(King)
