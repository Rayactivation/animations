from __future__ import absolute_import

import random, math
from simple_af.model import Effect, Scene, MultiEffect
from simple_af.state import STATE

class SolidBackground(Effect):
    """Always return a singular color. Can be bound top/bottom and
    left-right (wrap-around not supported yet)
    """

    def __init__(self, color=(255, 0, 0), start_col=0, end_col=None, start_row=0, end_row=None):
        Effect.__init__(self)
        self.color = color
        self.slice = (slice(start_row, end_row), slice(start_col, end_col))
        print "Created with color", self.color


def printpixel(idx, pixel):
    print idx, pixel

def compute_pixel(pixels, idx, pix, cos_rad, sin_rad, frame):
    point = pix['points'][frame]
    z_normalized = point[1]-120
    x_rotated = cos_rad*point[0] - sin_rad*point[2]
    y_rotated = sin_rad*point[0] + cos_rad*point[2]
    pixels[idx] = (
        0, #abs(x_rotated),
        z_normalized * 3, #abs(y_rotated),
        100)

class Gradient(Effect):
    def __init__(self):
        super(Gradient, self).__init__()
        curmaxz=0
        for pix in STATE.layout.pixels:
            curmaxz = max(pix['point'][1], curmaxz)
        print "Max Z", curmaxz
        self.frames_per_period = len(STATE.layout.pixels[0]['points'])

    def next_frame(self, pixels, t):
        #map(printpixel, pixels)
        cos_rad = math.cos(t)
        sin_rad = math.sin(t)
        frame = int(t*STATE.fps) % self.frames_per_period
        #print 'Frame', frame, 'T', t, 'frames per period', self.frames_per_period, "fps", STATE.fps, "trunc", int(t/STATE.fps)
        map(lambda (idx, pix): compute_pixel(pixels, idx, pix, cos_rad, sin_rad, frame), enumerate(STATE.layout.pixels))

#    def is_completed(self, t):
 #       return random.randint(0,1)

SCENES = [
    Scene(
        name= "GradientExample",
        effects=[
            Gradient()
        ]
    )
]