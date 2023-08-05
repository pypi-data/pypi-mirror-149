from tickytacky.screen import Screen
from tickytacky.sprite import Sprites


class Scene():
    def __init__(self, **kwargs):
        self.sprites = Sprites(kwargs.get("sprites"))
        self.window = Screen(
            title=kwargs.get("title"),
            fixed=kwargs.get("fixed", False),
            height=kwargs.get("height"),
            width=kwargs.get("width"),
            pixel_sprites=self.sprites.pixel_sprites)
