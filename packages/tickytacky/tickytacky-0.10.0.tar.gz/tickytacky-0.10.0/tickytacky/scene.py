from tickytacky.screen import Screen
from tickytacky.sprite import Sprites, Tiles
from pyglet.sprite import Sprite
import json


class Scene():
    def __init__(self, **kwargs):
        self.sprites = Sprites(kwargs.get("sprites"))
        self.height = kwargs.get("height")
        self.width = kwargs.get("width")
        self.window = Screen(
            title=kwargs.get("title"),
            fixed=kwargs.get("fixed", False),
            height=self.height,
            width=self.width,
            pixel_sprites=self.sprites.pixel_sprites)
        self.tiles = Tiles(tile_files=kwargs.get("tile_files", []))
        self.scenes = self.scene_data(scene_data=kwargs.get("scene_data"))
        self.current_scene = self.scenes.get("default_scene")

    def pixel_system(self, x, y):
        _width = self.window.width - 1
        _height = self.window.height - 1
        _x = x * self.window.factor
        _y = ((y*-1 + 150) * self.window.factor)
        f = self.window.factor
        converted_coords = [(_width * f) - _width * f + _x,
                            (_height * f) - _height * f + _y]
        return converted_coords

    def load_scene(self, new_scene):
        self.current_scene = new_scene
        self.scene = []
        for tile in self.scenes[new_scene]:
            coords = self.pixel_system(tile[1], tile[2])
            self.scene.append(
                Sprite(self.tiles.tile_data[tile[0]],
                       x=coords[0], y=coords[1], batch=self.window.batch)
            )
        self.window.batch.draw()

    def scene_data(self, scene_data):
        if scene_data:
            with open(scene_data, "r") as json_file:
                scenes = json.load(json_file)
            return scenes
