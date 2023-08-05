import pyglet
from pyglet import shapes


class Screen(pyglet.window.Window):
    def __init__(self, width=240, height=160,
                 factor=6, title="NoName", fixed=False,
                 pixel_sprites=[]):
        super().__init__(width*factor, height*factor, title)
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        self.tile_batch = pyglet.graphics.Batch()
        self.height = height
        self.width = width
        self.factor = factor
        self.title = title
        self.pixel = []
        self.sprites = dict()
        for sprite in pixel_sprites:
            self.sprites[sprite["name"]] = {
                "name": sprite.get("name"),
                "data": sprite.get("data"),
                "location": sprite.get("location")}

        if fixed:
            super().set_maximum_size(width*factor, height*factor)
            super().set_minimum_size(width*factor, height*factor)

    def pixel_system(self, x, y):
        _width = self.width - 1
        _height = self.height - 1
        _x = x * self.factor
        _y = ((y*-1 + 159) * self.factor)
        f = self.factor
        return [(_width * f) - _width * f + _x,
                (_height * f) - _height * f + _y]

    def set_pixel(self, pixel, color):
        pixel = self.pixel_system(pixel[0], pixel[1])
        if not color:
            return None
        else:
            self.pixel.append(shapes.Rectangle(
                              pixel[0],
                              pixel[1],
                              self.factor, self.factor,
                              color=color, batch=self.batch))

    def add_sprite(self, name, location=None):
        self.pixel = []
        palette = self.sprites[name]["data"].get("palette")
        shape = self.sprites[name]["data"].get("shape", [])
        max_row_size = 0
        if not location:
            return None
        if self.sprites[name]["location"]:
            for r in range(0, len(shape)):
                for c in range(0, len(shape[r])):
                    if max_row_size < len(shape[r]):
                        max_row_size = len(shape[r])
                    self.set_pixel(pixel=(location[0] + c, location[1] + r),
                                   color=palette.get(shape[r][c]))
        self.sprites[name]["location"] = [location[0], location[1]]

    def draw_all_sprites(self, sprites):
        for name in sprites:
            if self.sprites[name]["location"]:
                self.set_pixels_in_shape(
                    shape=self.sprites[name]["data"].get("shape", []),
                    palette=self.sprites[name]["data"].get("palette"),
                    location=self.sprites[name]["location"]
                )
            sprite_copies = self.sprites[name].get("locations", [])
            # If locations is a key, then place the tile in all the locations
            for copy_sprite in sprite_copies:
                self.set_pixels_in_shape(
                    shape=self.sprites[name]["data"].get("shape", []),
                    palette=self.sprites[name]["data"].get("palette"),
                    location=copy_sprite)

    def set_pixels_in_shape(self, shape, palette, location):
        # Use only for static sprites. using this for moving sprites makes
        # some parts of the sprite lag behind.
        max_row_size = 0
        for r in range(0, len(shape)):
            for c in range(0, len(shape[r])):
                if max_row_size < len(shape[r]):
                    max_row_size = len(shape[r])
                self.set_pixel(
                    pixel=(
                      location[0] + c, location[1] + r),
                    color=palette.get(shape[r][c]))

    def text(self,
             text="",
             font="Times New Roman",
             size=36,
             font_directory=None,
             position=[0, 0],
             anchors=["left", "bottom"]):
        if font_directory:
            pyglet.font.add_directory(font_directory)
        pyglet.text.Label(text,
                          font_name=font,
                          font_size=size,
                          x=position[0], y=position[1],
                          batch=self.batch,
                          anchor_x=anchors[0], anchor_y=anchors[1])

    def on_draw(self):
        self.clear()
        self.batch.draw()
