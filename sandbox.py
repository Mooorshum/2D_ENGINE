import pygame

from math import sin, cos

from graphics import grass
from graphics.particles import ParticleSystem
from world.particle_presets import flame
from general_game_mechanics.dynamic_objects import Vehicle, SinglePlant

from ui.menu import MainMenu
from ui import START_GAME_EVENT
pygame.init()

from enum import Enum

class GameStates(Enum):
    PLAYING = 1
    PAUSED = 2
    AT_EXIT = 3




font = pygame.font.SysFont(None, 20)

def display_fps(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'fps: {fps}', True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = fps_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(fps_text, text_rect)


class Game:
    def __init__(self):
        self.game_state = GameStates.PAUSED
        self.screen_width = 960
        self.screen_height = 541

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("background.png").convert()

        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.mouse_x, self.mouse_y = None, None

        self.flame = flame
        self.flame.x = 300
        self.flame.y = 300

        self.player = Vehicle(type='vehicle', name='hippie_van')
        self.player.scale = 2
        self.player.x = 200
        self.player.y = 200


        self.cop = Vehicle(type='vehicle', name='cop_car')
        self.cop.scale = 2
        self.cop.x = 400
        self.cop.y = 300


        self.grass_system = grass.GrassSystem()
        for x in range (100, 860, self.grass_system.tile_size):
            for y in range (100, 441, self.grass_system.tile_size):
                self.grass_system.create_new_tile((x, y), 'assets/grass')
        self.grass_system.sort_tiles()
        self.time = 0





        self.main_menu = MainMenu(pygame.display.get_surface().size)



    def run(self):
        clock = pygame.time.Clock()
        while self.game_state != GameStates.AT_EXIT:
            time_delta = clock.tick(60) / 1000.0
            self.handle_events()
            if self.game_state == GameStates.PLAYING:
                self.screen.blit(self.background, (0, 0))
                self.update_screen_game(time_delta)
            elif self.game_state == GameStates.PAUSED:
                self.screen.blit(self.background, (0, 0))
                self.main_menu.draw(self.screen, time_delta)
                pygame.display.update()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameStates.AT_EXIT
            else:
                if event.type == START_GAME_EVENT:
                    self.main_menu.hide()
                    self.game_state = GameStates.PLAYING
                else:
                    self.main_menu.process_events(event)

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game_state = GameStates.PAUSED
            self.main_menu.show()

        self.player.handle_movement(keys)

        

    def update_screen_game(self, time_delta : float):
        display_fps(self.screen, self.clock, font)
        


        grass_bendpoints = [((self.player.x, self.player.y)), ((self.cop.x, self.cop.y))]

        

        self.grass_system.render_grass_tiles(self.screen, grass_bendpoints)
        self.grass_system.apply_wind(1/50, self.time, wind_speed=20)
        self.time += 1

        self.cop.draw_dust(self.screen)
        self.cop.draw(self.screen)
        self.cop.move()
        self.cop.vx = self.cop.speed_limit//2*sin(self.time//20)
        self.cop.vy = self.cop.speed_limit//2*cos(self.time//20)


        self.player.draw_dust(self.screen)
        self.player.draw(self.screen)
        self.player.move()



        self.flame.update_particles()
        self.flame.draw_particles(self.screen)
        

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()