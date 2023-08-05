import pyglet


class Clock():
    def schedule_interval(self, update, interval):
        pyglet.clock.schedule_interval(update, interval)
