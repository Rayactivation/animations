import os, sys, math
import argparse
import json

IN_LINE_SPACING=1.312

parser = argparse.ArgumentParser()
parser.add_argument(
    '-o',
    '--output_file',
    dest='output_file',
    default='block_ray_layout_animated.json',
    action='store',
    type=str,
    help='json file to output to. Will be overwritten')
parser.add_argument(
    '--scale',
    dest='scale',
    default=20,
    action='store',
    type=float)
parser.add_argument(
    '--pretty-print',
    dest='pretty_print',
    action='store_true')
"""
parser.add_argument(
    '--invertX',
    dest='invertX',
    default=True,
    action='store',
    type=bool)
parser.add_argument(
    '--invertY',
    dest='invertY',
    default=True,
    action='store',
    type=bool)
"""

options = parser.parse_args()
filename = options.output_file
SCALE = options.scale

ADDRESS="10.0.0.32"

Z_BASE = 12*13
Z_BOOM = Z_BASE-6

RADIUS = 20*12
ANIMATION_PERIOD = 10*30
THETA_PER_FRAME = 2.0*math.pi/ANIMATION_PERIOD

def generate_box(strip_offset=0):
    print "Generating Box..."

    X_CENTER = RADIUS
    Y_START = -3*12
    Y_STEP = IN_LINE_SPACING
    HEAD_LIGHTS = [5,5,6,7,6,5,4,3,2,1,0]
    lights = [
        {
            "address": ADDRESS,
            "strip": strip+strip_offset,
            "strip_index": stripidx,
            "point": [strip*4+X_CENTER, Z_BASE, Y_START + stripidx*Y_STEP],
            #FIXME - Animate by section, this is redundant
            "points": [[strip*4+X_CENTER, Z_BASE, Y_START + stripidx*Y_STEP] for _ in range(ANIMATION_PERIOD)],
            "section": "body"
        }
        for strip in range(-9,9+1) for stripidx in range(126+3*(HEAD_LIGHTS[abs(strip)]))
    ]

    for point in lights:
        point["points"] = [point["point"]]*ANIMATION_PERIOD

    return lights

def generate_tail(strip_offset=0):
    print "Generating Tail..."

    X_CENTER = RADIUS

    Y_START = -3 * 12
    Y_STEP = -IN_LINE_SPACING

    STRIP_LENGTH = 100

    lights = []
    for strip in range(-4, 4+1):
        X_START = 2*strip * 4.0 / 2 + X_CENTER
        X_END = 2*strip * 4.0 / 8 + X_CENTER
        X_STEP = (X_END - X_START) / STRIP_LENGTH
        lights += [
            {
                "address": ADDRESS,
                "strip": strip + strip_offset,
                "strip_index": stripidx,
                "point": [X_START + X_STEP * stripidx, Z_BASE, Y_START + stripidx * Y_STEP],
                "section": "tail"
            }
            for stripidx in range(STRIP_LENGTH)
        ]

    for point in lights:
        point["points"] = [point["point"]]*ANIMATION_PERIOD

    return lights

def generate_wing(inverse, strip_offset=0):
    print "Generating wing..."
    print "Strip Offset:", strip_offset, "Inverse:", inverse
    INVERSE_MULT = -1 if inverse else 1

    X_START = RADIUS + INVERSE_MULT*3*12
    X_STEP = INVERSE_MULT * IN_LINE_SPACING
    MAX_LENGTH = 64 #leds
    #Z_STEP = IN_LINE_SPACING/4 #1:4 height
    Z_STEP = IN_LINE_SPACING  # Animate up to 45 degrees

    NUM_STRIPS = 33
    THETA_OFFSET_PER_STRIP = 2.0*math.pi/(3.0*NUM_STRIPS)

    Y_CENTER = 4.5*12
    return [
        {
            "address": ADDRESS,
            "strip": strip+strip_offset,
            "strip_index": stripidx,
            "point": [X_START + (stripidx+1)*X_STEP, Z_BASE+stripidx*Z_STEP, Y_CENTER+strip*4],
            "points": [[
                X_START + (stripidx+1)*X_STEP,
                Z_BASE+stripidx*Z_STEP*max(0,math.sin(theta*THETA_PER_FRAME+THETA_OFFSET_PER_STRIP*strip+16)),
                Y_CENTER+strip*4
            ] for theta in range(ANIMATION_PERIOD)],
            "section": "wing-"+("inside" if inverse else "outside")
        }
        for strip in range(-16, 16 + 1) for stripidx in range(MAX_LENGTH-abs(strip)*2)
    ]

def generate_pole(strip_offset=0):
    print "Generating pole arm"
    Z_STEP = IN_LINE_SPACING
    Z_LENGTH = int((Z_BASE-6)/IN_LINE_SPACING)
    return [
        {
            "address": ADDRESS,
            "strip": strip_offset,
            "strip_index": stripidx,
            "point": [0, 0 + stripidx * Z_STEP, 0],
            "points": [[0, 0 + stripidx * Z_STEP, 0] for _ in range(ANIMATION_PERIOD)],
            "section": "pole"
        }
        for stripidx in range(Z_LENGTH)
    ]

def generate_boom(strip_offset=0):
    print "Generating pole arm"
    X_STEP = IN_LINE_SPACING
    X_LENGTH = int(RADIUS/IN_LINE_SPACING)
    return [
        {
            "address": ADDRESS,
            "strip": strip_offset,
            "strip_index": stripidx,
            "point": [stripidx*X_STEP, Z_BOOM, 0],
            "points": [[stripidx*X_STEP, Z_BOOM, 0] for _ in range(ANIMATION_PERIOD)],
            "section": "boom"
        }
        for stripidx in range(X_LENGTH)
    ]



lights = generate_box()+generate_tail(19) + generate_wing(False, 2*19) + generate_wing(True, 2*19+33)+generate_pole(2*19+66)+generate_boom(2*19+67)

print "Writing to file:", filename, "Pretty Print:", options.pretty_print
with open(filename, 'w') as file_out:
    json.dump(lights, file_out, indent=options.pretty_print if options.pretty_print else None)