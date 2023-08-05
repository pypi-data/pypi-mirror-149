import json
from flask import Flask, render_template
import logging
import tempfile
import pyglet
from PIL import Image, ImageDraw

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder="../tools/")


@app.route('/')
def sprite_maker():
    return render_template('home.html')


@app.route('/spriteOutput.html')
def sprite_output():
    return render_template('spriteOutput.html')


@app.route('/sprite_maker16.html')
def sprite_16():
    return render_template('sprite_maker16.html')


@app.route('/sprite_maker32.html')
def sprite_32():
    return render_template('sprite_maker32.html')


class Sprites():
    def __init__(self, sprite_files=[]):
        self.pixel_sprites = []
        for sprite_file in sprite_files:
            data = self.load_sprite_file(sprite_file)
            self.pixel_sprites.append(
                {"name": data.get("name"),
                 "data": data}
            )

    def load_sprite_file(self, file):
        with open(file, "r") as json_file:
            sprite = json.load(json_file)
        return sprite


class Tiles():
    def __init__(self, factor=6, tile_files=[]):
        self.tile_data = dict()
        for tile_file in tile_files:
            data = self.load_tile_file(tile_file)
            png_image = Image.new('RGB',
                                  (len(data["shape"][0])*factor,
                                   len(data["shape"])*factor))
            for row in range(0, len(data["shape"])):
                for col in range(0, len(data["shape"][row])):
                    color = data["palette"].get(
                        data["shape"][row][col], [0, 0, 0]
                    )
                    draw_obj = ImageDraw.Draw(png_image)
                    draw_obj.rectangle(
                        [col*factor, row*factor,
                         (col*factor)+factor, (row*factor)+factor],
                        fill=(color[0], color[1], color[2])
                    )

            with tempfile.NamedTemporaryFile(suffix=".png") as tmp_file:
                png_image.save(tmp_file.name)
                self.tile_data[data.get("name")] = pyglet.image.load(
                    tmp_file.name
                )

    def load_tile_file(self, file):
        with open(file, "r") as json_file:
            sprite = json.load(json_file)
        return sprite


if __name__ == "__main__":
    app.run(host="0.0.0.0")
