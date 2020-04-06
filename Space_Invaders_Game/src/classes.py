import abc
import pygame
import random
import math
import os

resource_path = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))\
                + '\\..\\res\\'


class Creator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self):
        pass


class PlayerCreator(Creator):
    def create(self):
        return Player()


class EnemyCreator(Creator):
    def create(self):
        return Enemy()


class Unit(metaclass=abc.ABCMeta):
    def __init__(self, image_src, x, y, x_change=0, y_change=0):
        self.image = pygame.image.load(image_src)
        self.X = x
        self.Y = y
        self.x_change = x_change
        self.y_change = y_change

    def draw(self, x, y, screen=pygame.display):
        screen.blit(self.image, (x, y))

    def collide(self, other):
        distance = math.sqrt(math.pow(self.X - other.X, 2) + math.pow(self.Y - other.Y, 2))
        if distance < 27:
            return True
        else:
            return False

    @abc.abstractmethod
    def move(self):
        pass


class Bullet(Unit):
    def __init__(self, x, y, x_change=0, y_change=12):
        Unit.__init__(self, resource_path + 'bullet.png', x, y, x_change, y_change)

    def move(self):
        pass


class Player(Unit):
    def __init__(self, x=300, y=480, x_change=0, y_change=0, bullet_state='ready'):
        Unit.__init__(self, resource_path + 'battleship.png', x, y, x_change, y_change)
        self.bullet_state = bullet_state
        self.bullet = Bullet(x, y)

    def fire(self, x, y, screen=pygame.display):
        self.bullet_state = 'fire'
        self.bullet.draw(x + 20, y + 10, screen)

    def move(self):
        self.X += self.x_change
        if self.X >= 736:
            self.X = 736
        elif self.X <= 0:
            self.X = 0


class Enemy(Unit):
    def __init__(self):
        Unit.__init__(self, resource_path + 'enemy.png', random.randint(0, 735), random.randint(50, 150), 2, 15)

    def move(self):
        self.X += self.x_change
        if self.X <= 0:
            self.x_change = 2
            self.Y += self.y_change
        elif self.X >= 736:
            self.x_change = -2
            self.Y += self.y_change
