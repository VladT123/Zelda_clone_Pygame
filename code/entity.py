import pygame
from math import sin
from support import import_csv_layout, import_folder
from random import choice, randint, randrange

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >=0:
            return 255
        else:
            return 0


class Grass(Entity):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.graphics = {'grass': import_folder('../graphics/grass')}
        self.sprite_type = 'grass'
        self.frame_index = randint(0, len(self.graphics['grass'])-1)
        self.image = self.graphics['grass'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

    def animate(self):
        speed = [0.0375, 0.01875]
        self.animation_speed = choice(speed)
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.graphics['grass']):
            self.frame_index = 0

        # self.image = self.graphics['grass'][int(self.frame_index)]
        # self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()
