import pygame

from graphics.plants import PlantSystem
from graphics.grass import GrassSystem
from graphics.sprite_stacks import SpritestackAsset

from general_game_mechanics.dynamic_objects import DynamicObject, Character # , Vehicle
from graphics.camera import Camera

from world_builder.level_editor import Level

from presets import particle_presets


pygame.init()


class Game:
    def __init__(self):

        """ MAP SETTINGS """
        self.map_width = 2000
        self.map_height = 2000
        
        """ DISPLAY SETTINGS """
        self.screen_width = 800
        self.screen_height = 600

        """ RENDER RESOLUTION """
        self.render_width = 400
        self.render_height = 300

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.camera = Camera(
            width=self.render_width,
            height=self.render_height,
            map_width=self.map_width,
            map_height=self.map_height
        )

        pygame.display.set_caption("SANDBOX")

        self.clock = pygame.time.Clock()
        self.time = 0


        """ PLAYER ASSETS """
        self.player_asset = SpritestackAsset(type='character', name='dude', hitbox_size=(16, 16), movelocked=False)


        """ NPC ASSETS """
        self.npc_assets = []


        """ VEHICLE ASSETS """
        self.vehicle_assets = [
            SpritestackAsset(type='vehicle', name='cop_car', hitbox_size=(64,36), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='vehicle', name='pickup_truck', hitbox_size=(64,36), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='vehicle', name='hippie_van', hitbox_size=(64,36), hitbox_type='circle', movelocked=False),
        ]


        """ NON-INTERACTABLE SPRITE STACK ASSETS """
        self.non_interactable_sprite_stack_assets = [
            SpritestackAsset(type='texture', name='branches_1', hitbox_size=(32,32), hitbox_type='circle', y0_base_offset=-1000),
        ]


        """ DYNAMIC SPRITE STACK ASSETS """
        self.dynamic_sprite_stack_assets = [

            # BUILDINGS
            SpritestackAsset(type='building', name='house_1', hitbox_size=(128,128), hitbox_type='circle'),
            SpritestackAsset(type='building', name='red_barn', hitbox_size=(128,128), hitbox_type='circle'),
            SpritestackAsset(type='building', name='shed', hitbox_size=(64,45), hitbox_type='circle'),
            SpritestackAsset(type='building', name='toilet', hitbox_size=(45,45), hitbox_type='circle'),

            # FENCES
            SpritestackAsset(type='fence', name='fence_1', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_2', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_3', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_4', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_5', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_6', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_7', hitbox_size=(10,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_8', hitbox_size=(10,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_9', hitbox_size=(10,10), hitbox_type='circle'),

            # WALLS
            SpritestackAsset(type='wall', name='wall_1', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_2', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_3', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_4', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_5', hitbox_size=(32,20), hitbox_type='circle'),

            # WINDMILLS
            SpritestackAsset(type='windmill', name='windmill_1', hitbox_size=(32,32), hitbox_type='circle'),

            # WELLS
            SpritestackAsset(type='well', name='well_1', hitbox_size=(50,50), hitbox_type='circle'),

            # TREES
            SpritestackAsset(type='tree', name='tree_1', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_2', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_3', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_4', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_5', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_6', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_7', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_8', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_9', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_trunk_1', hitbox_size=(25,25), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_trunk_2', hitbox_size=(25,25), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_trunk_3', hitbox_size=(25,25), hitbox_type='circle'),

            # ROCKS
            SpritestackAsset(type='rock', name='rock_1', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_2', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_3', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_4', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_5', hitbox_size=(32,32), hitbox_type='circle'),

            # CRATES
            SpritestackAsset(type='crate', name='crate_1', hitbox_size=(32,20), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='crate', name='crate_2', hitbox_size=(32,32), hitbox_type='circle', movelocked=False),

            # HAY BALES
            SpritestackAsset(type='hay_bale', name='hay_bale_1', hitbox_size=(32,32), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='hay_bale', name='hay_bale_2', hitbox_size=(32,32), hitbox_type='circle', movelocked=False),

            # BARRELS
            SpritestackAsset(type='barrel', name='barrel_1', hitbox_size=(16,16), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='barrel', name='barrel_2', hitbox_size=(16,16), hitbox_type='circle', movelocked=False),

            # WHEELBARROWS
            SpritestackAsset(type='wheelbarrow', name='wheelbarrow_1', hitbox_size=(25,25), hitbox_type='circle', movelocked=False),

            # WATER TOWERS
            SpritestackAsset(type='water_tower', name='water_tower_1', hitbox_size=(64,64), hitbox_type='circle'),

            # CAMPFIRES
            SpritestackAsset(type='campfire', name='campfire_1', hitbox_size=(32,32), hitbox_type='circle'),
        ]


        """ PLANT SYSTEM ASSETS """
        self.plant_systems = [
            PlantSystem(
                folder='assets/_plant_assets/bush_1',
                num_branches_range = (4,7),
                base_angle_range = (30, 70),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
            PlantSystem(
                folder='assets/_plant_assets/bush_2',
                num_branches_range = (1,10),
                base_angle_range = (70, 80),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
            PlantSystem(
                folder='assets/_plant_assets/bush_3',
                num_branches_range = (1,8),
                base_angle_range = (70, 80),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
            PlantSystem(
                folder='assets/_plant_assets/bush_4',
                num_branches_range = (1,4),
                base_angle_range = (5, 15),
                stiffness_range = (0.1, 0.03),
                relax_speed=0.2,
                scale=1
            ),
        ]


        """ GRASS SYSTEM ASSETS """
        self.grass_systems = [
            GrassSystem(
                folder = 'assets/_grass_assets/grass_1',
                min_tile_size=20,
                max_tile_size=40,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.1,
                num_assets=10,
                scale=0.5
            ),
            GrassSystem(
                folder = 'assets/_grass_assets/grass_2',
                min_tile_size=20,
                max_tile_size=40,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.1,
                num_assets=10,
                scale=0.5
            ),
        ]


        """ PARTICLE SYSTEM PRESETS """
        self.particle_system_presets = [
            particle_presets.flame,
        ]


        """ TEST LEVEL """
        self.test_level = Level(self)


    def run(self):
        while 1 != 0:
            self.handle_events()
            self.update_screen_game()


    def handle_events(self):
        self.events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.test_level.handle_controls_editing(keys)
        self.test_level.edit_level()
        self.camera.handle_movement(keys)


    def update_screen_game(self):

        self.test_level.render()
        self.test_level.update()
        pygame.display.update()

        self.clock.tick(110)
        self.time += 1


if __name__ == "__main__":
    game = Game()
    game.run()
