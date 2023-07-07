import pygame
import sys
from settings import *
from support import import_csv_layout, import_folder
from tile import Tile
from player import Player
from debug import debug
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from entity import Grass

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # sprite setup
        self.soul_level = 0
        self.create_map()

        # UI
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # sounds
        self.win_sound = pygame.mixer.Sound('../audio/win.wav')
        self.lose_sound = pygame.mixer.Sound('../audio/lose.wav')
        self.win_sound.set_volume(0.5)
        self.lose_sound.set_volume(0.5)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects'),

        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        if style == 'grass':
                            Grass((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites])
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "object", surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                   (x, y),
                                   [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                    self.soul_level
                                )
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites, self.enemy_sprites],
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp,
                                    self.soul_level
                                )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

        if style == 'firestorm':
            self.magic_player.firestorm(self.player, cost, [self.visible_sprites, self.attack_sprites])

        if style == 'push':
            self.magic_player.push(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 50)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):

        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def clear_all(self):
        for sprite in self.attackable_sprites:
            sprite.kill()
        for sprite in self.attack_sprites:
            sprite.kill()
        for sprite in self.visible_sprites:
            sprite.kill()
        for sprite in self.obstacle_sprites:
            sprite.kill()
        for sprite in self.enemy_sprites:
            sprite.kill()

    def game_over(self):
        if not self.player.alive:
            self.clear_all()
            self.create_map()
            self.player.stats = self.player.base_stats
            self.player.exp = 0
            self.soul_level = 0
            self.player.alive = True
            self.upgrade = Upgrade(self.player)
            self.lose_sound.play()

    def check_new_game(self):
        if len(self.enemy_sprites) == 0 and self.player.alive:
            self.win_sound.play()
            self.temp_stats = self.player.stats
            self.temp_exp = self.player.exp
            self.clear_all()
            self.soul_level += 1
            self.create_map()
            self.player.stats = self.temp_stats
            self.player.exp = self.temp_exp
            self.upgrade = Upgrade(self.player)

    def run(self):

        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.check_new_game()
            self.game_over()
            debug(self.soul_level)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.image.load("../graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        # Getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # Drawing BG
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
