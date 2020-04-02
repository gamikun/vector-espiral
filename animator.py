from math import sqrt, sin, cos, pi
import subprocess
import cairo

def circumference(n, r=1, xy=(0, 0)):
    x, y = xy
    t = pi * 2 / n
    return [
        (cos(t * i) * r + x, sin(t * i) * r + y)
        for i in range(n)
    ]

RADIUS = 400
WIDTH = 1080

cx, cy = 0.5, 0.5
dots = circumference(14, r=RADIUS / WIDTH, xy=(0.5, 0.5))

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, WIDTH)
ctx = cairo.Context(surface)
ctx.scale(WIDTH, WIDTH)

ctx.set_line_width(3.0 / WIDTH)
ctx.set_source_rgb(1.0, 1.0, 1.0)

def line_in_time(ctx, src, dst, time=1.0):
    x, y = src
    subx, suby = dst
    w = subx - x
    h = suby - y

    ctx.move_to(x, y)
    ctx.line_to(x + w * time, y + h * time)

ctx.set_source_rgb(1.0, 1.0, 1.0)
            
framerate = 60
seconds = 5
frames = framerate * seconds

ffmpeg = subprocess.Popen(
    ['ffmpeg',
        '-f', 'image2pipe',
        '-framerate', str(framerate),
        '-vcodec', 'png',
        '-i', '-',
        '-f', 'mp4',
        '-b:v', '5000k',
        '-y',
        'algo.mp4'
    ],
    stdin=subprocess.PIPE
)

for frame in range(frames):
    time = frame / frames

    # Clean
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    ctx.paint()

    ctx.set_source_rgb(1.0, 1.0, 1.0)
    for index, pos in enumerate(dots):
        x, y = pos
        for subindex, subpos in enumerate(dots):
            subx, suby = subpos
            if subindex > index:
                line_in_time(ctx, pos, subpos, time=time)
                ctx.stroke()

    surface.write_to_png(ffmpeg.stdin)

for extra_second in range(framerate * 3):
    surface.write_to_png(ffmpeg.stdin)
    
ffmpeg.communicate()