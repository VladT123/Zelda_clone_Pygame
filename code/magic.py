import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'fire': pygame.mixer.Sound('../audio/fire.wav'),
        }
    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['fire'].play()
            direction = player.status.split('_')[0]

            if direction == 'right':
                aim = pygame.math.Vector2(1, 0)
            elif direction == 'left':
                aim = pygame.math.Vector2(-1, 0)
            elif direction == 'up':
                aim = pygame.math.Vector2(0, -1)
            else:
                aim = pygame.math.Vector2(0, 1)

            for i in range(1, 6):

                if aim.x:
                    offset_x = (aim.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame', (x, y), groups, 'flame')
                else:
                    offset_y = (aim.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups, 'flame')

    def firestorm(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            self.sounds['fire'].play()
            aim_r = pygame.math.Vector2(1, 0)
            aim_l = pygame.math.Vector2(-1, 0)
            aim_u = pygame.math.Vector2(0, -1)
            aim_d = pygame.math.Vector2(0, 1)

            for i in range(1, 3):
                offset_x = (aim_r.x * i) * TILESIZE
                offset_y = (aim_r.y * i) * TILESIZE
                x = player.rect.centerx + offset_x + randint(-TILESIZE//1, TILESIZE//1)
                y = player.rect.centery + offset_y + randint(-TILESIZE//1, TILESIZE//1)
                self.animation_player.create_particles('flame', (x, y), groups, 'flame')
                offset_x = (aim_l.x * i) * TILESIZE
                offset_y = (aim_l.y * i) * TILESIZE
                x = player.rect.centerx + offset_x + randint(-TILESIZE//1, TILESIZE//1)
                y = player.rect.centery + offset_y + randint(-TILESIZE//1, TILESIZE//1)
                self.animation_player.create_particles('flame', (x, y), groups, 'flame')
                offset_x = (aim_u.x * i) * TILESIZE
                offset_y = (aim_u.y * i) * TILESIZE
                x = player.rect.centerx + offset_x + randint(-TILESIZE//1, TILESIZE//1)
                y = player.rect.centery + offset_y + randint(-TILESIZE//1, TILESIZE//1)
                self.animation_player.create_particles('flame', (x, y), groups, 'flame')
                offset_x = (aim_d.x * i) * TILESIZE
                offset_y = (aim_d.y * i) * TILESIZE
                x = player.rect.centerx + offset_x + randint(-TILESIZE//1, TILESIZE//1)
                y = player.rect.centery + offset_y + randint(-TILESIZE//1, TILESIZE//1)
                self.animation_player.create_particles('flame', (x, y), groups, 'flame')

    def heal(self, player, strength, cost, groups):
        self.sounds['heal'].play()
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def push(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['heal'].play()
            aim_r = pygame.math.Vector2(1, 0)
            aim_l = pygame.math.Vector2(-1, 0)
            aim_u = pygame.math.Vector2(0, -1)
            aim_d = pygame.math.Vector2(0, 1)
            self.animation_player.create_particles('aura', player.rect.center, groups)
            r_offset = 1
            for j in range(0, 1):
                for i in range(1, 2):
                    offset_x = (aim_r.x * i) * TILESIZE
                    offset_y = (aim_r.y * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    self.animation_player.create_particles('push', (x, y), groups, 'push')
                    offset_x = (aim_l.x * i) * TILESIZE
                    offset_y = (aim_l.y * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    self.animation_player.create_particles('push', (x, y), groups, 'push')
                    offset_x = (aim_u.x * i) * TILESIZE
                    offset_y = (aim_u.y * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    self.animation_player.create_particles('push', (x, y), groups, 'push')
                    offset_x = (aim_d.x * i) * TILESIZE
                    offset_y = (aim_d.y * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//r_offset, TILESIZE//r_offset)
                    self.animation_player.create_particles('push', (x, y), groups, 'push')





