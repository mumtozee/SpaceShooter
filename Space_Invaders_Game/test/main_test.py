import unittest
import pygame
import os
import sys

PARENT_DIR = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PARENT_DIR)))

from src import classes

screen = pygame.display.set_mode((800, 600))
tmp_player = classes.PlayerCreator.create(classes.PlayerCreator())
enemy = classes.EnemyCreator.create(classes.EnemyCreator())


class PlayerFactoryTester(unittest.TestCase):
    def test_is_tmp_player(self):
        global tmp_player
        self.assertIsInstance(tmp_player, classes.Player, "tmp_player has type tmp_player")
        self.assertIsInstance(tmp_player.bullet, classes.Bullet, "tmp_player has bullet")


class EnemyFactoryTester(unittest.TestCase):
    def test_is_enemy(self):
        global enemy
        self.assertIsInstance(enemy, classes.Enemy, "tmp_player has type tmp_player")


class PlayerFuctionalityTester(unittest.TestCase):
    def test_is_tmp_player_moving(self):
        global tmp_player
        tmp_player.x_change = 2
        tmp_X = tmp_player.X
        tmp_player.move()
        self.assertEqual(tmp_player.X, tmp_X + tmp_player.x_change)

    def test_fire(self):
        global tmp_player, screen
        tmp_player.fire(tmp_player.X, tmp_player.Y, screen)
        self.assertEqual(tmp_player.bullet_state, 'fire')


class EnemyFunctionalityTester(unittest.TestCase):
    def test_is_enemy_moving(self):
        global enemy
        enemy.x_change = 6
        tmp_X = enemy.X
        enemy.move()
        self.assertEqual(enemy.X, tmp_X + enemy.x_change)


class TestObjectDrawing(unittest.TestCase):
    def test_draw(self):
        global enemy
        enemy.draw(0, 0, screen)
        color = tuple(screen.get_at((32, 32)))
        self.assertNotEqual(color, (0, 0, 0, 255))


class CollisionTest(unittest.TestCase):
    def test_collide(self):
        global enemy, tmp_player
        enemy.X = 0
        enemy.Y = 0
        tmp_player.X = 100
        tmp_player.Y = 100
        self.assertFalse(tmp_player.collide(enemy))
        tmp_player.X = 0
        tmp_player.Y = 0
        self.assertTrue(tmp_player.collide(enemy))


if __name__ == '__main__':
    unittest.main()
