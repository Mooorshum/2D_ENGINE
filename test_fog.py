import pygame

from graphics import grass, plants
from graphics.rendering import global_render
from general_game_mechanics.dynamic_objects import DynamicObject, Vehicle
from graphics.camera import Camera
from graphics.particles import FogSystem

from world.particle_presets import flame


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

        self.map_width = 1500
        self.map_height = 750

        self.screen_width = 800
        self.screen_height = 600

        self.render_width = 400
        self.render_height = 300

        self.render_surface = pygame.Surface((self.render_width, self.render_height))

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.camera = Camera(self.render_width, self.render_height, self.map_width, self.map_height)
        
        self.background = pygame.image.load("background.png").convert()

        pygame.display.set_caption("SANDBOX")

        self.clock = pygame.time.Clock()

        self.mouse_x, self.mouse_y = None, None


        self.player = Vehicle(type='vehicle', name='hippie_van', scale=1)
        self.player_start_position = [200, 200]
        self.player.position = [500, 500]
        self.camera.position = [300, 300]


        self.cop_1 = Vehicle(type='vehicle', name='cop_car', scale=1)
        self.cop_1.position = [400, 400]
        self.cop_1.rotation = 25


        self.cop_2 = Vehicle(type='vehicle', name='cop_car', scale=1)
        self.cop_2.position = [400, 200]
        self.cop_2.rotation = 70


        self.hillbilly = Vehicle(type='vehicle', name='pickup_truck', scale=1)
        self.hillbilly.position = [850, 580]
        self.hillbilly.rotation = 30


        self.well = DynamicObject(type='filler_object', name='well', scale=1)
        self.well.position = [510, 320]
        self.well.rotation = 20
        self.well.movelocked = True


        self.shack_1 = DynamicObject(type='building', name='shack', scale=1)
        self.shack_1.position = [530, 180]
        self.shack_1.rotation = -30
        self.shack_1.movelocked = True


        self.shack_2 = DynamicObject(type='building', name='shack', scale=1)
        self.shack_2.position = [200, 450]
        self.shack_2.rotation = 10
        self.shack_2.movelocked = True


        self.barn = DynamicObject(type='building', name='barn', scale=1)
        self.barn.position = [750, 520]
        self.barn.rotation = 50
        self.barn.movelocked = True


        self.crate_1 = DynamicObject(type='filler_object', name='crate_1', scale=1)
        self.crate_1.position = [500, 550]
        self.crate_1.rotation = 50
        self.crate_1.mass = 100


        self.crate_2 = DynamicObject(type='filler_object', name='crate_1', scale=1)
        self.crate_2.position = [560, 570]
        self.crate_2.rotation = 20
        self.crate_2.mass = 100


        self.bottle_1 = DynamicObject(type='filler_object', name='bottle', scale=1)
        self.bottle_1.position = [570, 570]
        self.bottle_1.rotation = -35
        self.bottle_1.mass = 10
        

        self.bottle_2 = DynamicObject(type='filler_object', name='bottle', scale=1)
        self.bottle_2.position = [500, 600]
        self.bottle_2.rotation = -45
        self.bottle_2.mass = 10


        self.bottle_3 = DynamicObject(type='filler_object', name='bottle', scale=1)
        self.bottle_3.position = [510, 590]
        self.bottle_3.rotation = 60
        self.bottle_3.mass = 10


        self.hay_bale_1 = DynamicObject(type='filler_object', name='hay_bale_1', scale=1)
        self.hay_bale_1.position = [780, 650]
        self.hay_bale_1.rotation = 40
        self.hay_bale_1.mass = 100


        self.hay_bale_2 = DynamicObject(type='filler_object', name='hay_bale_1', scale=1)
        self.hay_bale_2.position = [730, 610]
        self.hay_bale_2.rotation = 30
        self.hay_bale_2.mass = 100


        self.hay_bale_3 = DynamicObject(type='filler_object', name='hay_bale_1', scale=1)
        self.hay_bale_3.position = [760, 600]
        self.hay_bale_3.rotation = 15
        self.hay_bale_3.mass = 100


        self.hay_bale_4 = DynamicObject(type='filler_object', name='hay_bale_2', scale=1.5)
        self.hay_bale_4.position = [560, 610]
        self.hay_bale_4.rotation = -20
        self.hay_bale_4.mass = 500


        self.hay_bale_5 = DynamicObject(type='filler_object', name='hay_bale_2', scale=1.5)
        self.hay_bale_5.position = [580, 570]
        self.hay_bale_5.rotation = -70
        self.hay_bale_5.mass = 500


        self.wheelbarrow = DynamicObject(type='filler_object', name='wheelbarrow', scale=1.2)
        self.wheelbarrow.position = [630, 570]
        self.wheelbarrow.rotation = 50
        self.wheelbarrow.mass = 100


        self.campfire = DynamicObject(type='filler_object', name='campfire', scale=1)
        self.campfire.position = [600, 500]
        self.campfire.rotation = 30
        self.campfire.movelocked = True


        self.flame = flame
        self.flame.position = [self.campfire.position[0], self.campfire.position[1] - 5, -5]
        

        self.grass_system = grass.GrassSystem(
            folder = 'assets/grass',
            tile_size=25,
            blades_per_tile=10,
            stiffness=0.03,
            scale=0.5
        )


        self.shrubs = plants.PlantSystem(
            folder='assets/branchy_bush',
            num_branches_range = (1,7),
            base_angle_range = (-1.2, 1.2),
            stiffness_range = (0.01, 0.2),
            gravity = 0.1,
            density = 1,
            scale=0.5
            )


        self.fern = plants.PlantSystem(
            folder='assets/fern',
            num_branches_range = (5,8),
            base_angle_range = (-1.2, 1.2),
            stiffness_range = (0.01, 0.2),
            gravity = 0.1,
            density = 1,
            scale=0.75
            )

        self.fog = FogSystem(
            cloud_size=(40, 40, 0),
            map_size=(self.map_width, self.map_height),
            max_particle_count=5,
            max_cloud_opacity=1
        )


        """ OBJECTS THAT SHOULD BE RENDERED """
        self.rendered_objects = [
            self.player, self.cop_1, self.cop_2, self.hillbilly,
            self.well,
            self.shack_1, self.shack_2, self.barn,
            self.campfire, self.flame,
            self.wheelbarrow,
            self.hay_bale_1, self.hay_bale_2, self.hay_bale_3, self.hay_bale_4, self.hay_bale_5,
            self.crate_1, self.crate_2,
            self.bottle_1, self.bottle_2, self.bottle_3,
        ]
        self.rendered_objects += self.fog.clouds


        """ OBJECTS THAT CAN COLLIDE, BEND GRASS ETC """
        self.dynamic_objects = [
            self.player, self.cop_1, self.cop_2, self.hillbilly,
            self.wheelbarrow,
            self.hay_bale_1, self.hay_bale_2, self.hay_bale_3, self.hay_bale_4, self.hay_bale_5,
            self.crate_1, self.crate_2,
            self.bottle_1, self.bottle_2, self.bottle_3,
        ]


        self.time = 0




    def run(self):
        clock = pygame.time.Clock()
        
        while self.game_state != GameStates.AT_EXIT:
            time_delta = clock.tick(60) / 1000.0
            self.handle_events()
            if self.game_state == GameStates.PLAYING:
                self.update_screen_game(time_delta)
            elif self.game_state == GameStates.PAUSED:
                pygame.display.update()

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameStates.AT_EXIT
            else:
                self.game_state = GameStates.PLAYING

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game_state = GameStates.PAUSED

        self.player.handle_movement(keys)
        self.camera.handle_movement(keys)


    def update_screen_game(self, time_delta : float):
        display_fps(self.screen, self.clock, font)

        """ DRAWING BACKGROUND """
        self.render_surface.fill((105, 66, 56))

        """ LOCKING CAMERA TO PLAYER """
        self.camera.follow(self.player.position)
        self.camera.align(self.player.rotation - 90)
        self.camera.move()

        """ APPLYING EFFECTS TO GRASS """
        self.grass_system.apply_wind(1/20, self.time)

        """ HANDLING OBJECT MOVEMENT """
        for dynamic_object in self.dynamic_objects:
            dynamic_object.move()


        """ HANDLING COLLISIONS """
        colliding_objects = self.dynamic_objects
        for object_1 in colliding_objects:
            for object_2 in colliding_objects:
                if object_1 != object_2:
                    object_1.hitbox.handle_collision(object_2)

        """ UPDATING PARTICLES """
        self.flame.update()
        self.fog.update(self.camera)





        """ OBJECTS THAT BEND PLANTS AND GRASS """
        self.foliage_bend_objects = self.dynamic_objects
        self.grass_system.bend_objects = self.foliage_bend_objects
        self.shrubs.bend_objects = self.foliage_bend_objects
        self.fern.bend_objects = self.foliage_bend_objects

        




        



        """ DYNAMIC SORTED RENDERING OF ALL GAME OBJECTS """
        global_render(
            self.render_surface,
            self.camera,
            self.rendered_objects,
            bend_objects=self.foliage_bend_objects,

        )


        


        upscaled_surface = pygame.transform.scale(self.render_surface, (self.screen_width, self.screen_height))
        self.screen.blit(upscaled_surface, (0, 0))


        """ DISPLAYING HITBOXES FOR MOVABLE OBJECTS """
        """ self.player.hitbox.draw(self.screen, offset=offset)
        self.cop.hitbox.draw(self.screen, offset=offset)
        self.hillbilly.hitbox.draw(self.screen, offset=offset) """


        display_fps(self.screen, self.clock, font)

        

        self.time += 1

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()
