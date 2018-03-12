# For more interesting morphs, change the cut variable
# Or the order of the LERP lists in triangle_points

import math

import imageio
from PIL import Image, ImageDraw

from io import BytesIO

im = Image.new("RGB", (600, 600))
drawing = ImageDraw.Draw(im)

# For playing around with LERPs
accepting_input = False
succeed = accepting_input
inp1 = ""
inp2 = ""

if accepting_input:
    inp1 = input("Type in 123 in any order...\n")
    inp2 = input("Do it again!\n")
    # succeed = True

    if len(inp1) != 3 or len(inp2) != 3:
        print("Input should be 3 digits long.")
        succeed = False
    else:
        for i in inp1 + inp2:
            if i not in ["1", "2", "3"]:
                succeed = False
                print("Input should only be 1, 2 or 3")
                break


def polar_cartesian(r, angle):
    return [r * math.cos(angle), r * math.sin(angle)]


def draw_circle(xy, r, col="red", im=im):
    x = xy[0]
    y = xy[1]
    coords = [x - r, y - r, x + r, y + r]
    ImageDraw.Draw(im).ellipse(coords, fill=col)


def shift(xy, im=im):
    # Centres images
    return [xy[0] + im.size[0] / 2, xy[1] + im.size[1] / 2]


def circle_points(radius, m):
    n = 3 * m  # To split evenly into a triangle
    unit = math.pi * 2 / n
    out = []
    for i in range(n):
        xy = polar_cartesian(radius, i * unit)
        out.append(xy)
    return out


def triangle_points(radius, n):
    p1 = [0, -radius]
    p2 = polar_cartesian(radius, math.pi / 6)
    p3 = polar_cartesian(radius, 5 * math.pi / 6)

    out = []
    diff1 = [p2[0] - p1[0], p2[1] - p1[1]]
    diff2 = [p3[0] - p2[0], p3[1] - p2[1]]
    diff3 = [p1[0] - p3[0], p1[1] - p3[1]]
    if accepting_input:
        old_diff = [diff1, diff2, diff3]
        old_points = [p1, p2, p3]

        diff = [old_diff[int(x) - 1] for x in inp1]
        points = [old_points[int(x) - 1] for x in inp2]

    else:
        diff = [diff1, diff2, diff3]
        points = [p1, p2, p3]

    for x in range(3):
        for i in range(n):
            percent = i / n
            next_x = points[x][0] + diff[x][0] * percent
            next_y = points[x][1] + diff[x][1] * percent
            out.append([next_x, next_y])
    return out


def morph(radius, n, steps=5, point_size=5):
    circle = circle_points(radius, n)
    triangle = triangle_points(radius, n)

    # These will add both a circle and a triangle to the images
    # circle = circle + triangle
    # triangle = triangle + circle

    # Cut = 2/3 of n reduces the rotation in the morph
    # Cut = 0 rotates 120(?) clockwise
    cut = int(2 * n / 3)
    triangle = triangle[cut:] + triangle[:cut]
    step = 1 / steps

    frames = []

    for f in range(steps + 1):  # create all frames
        linear = step * f
        percent_x = linear  # math.sin(linear*math.pi/2)
        percent_y = linear
        image = Image.new("RGB", (600, 600))
        for i in range(len(circle)):
            c = circle[i]
            t = triangle[i]
            # LERP betweeen
            diff = [c[0] - t[0], c[1] - t[1]]
            x = t[0] + diff[0] * percent_x
            y = t[1] + diff[1] * percent_y
            # Smooth colour, joining together
            col = (int(math.fabs((i * 512 / len(circle)) - 256)), 125, 125)

            # Used with both circle and triangle

            # unit = f/(steps+1)
            # val_c = int(unit*unit*255)
            # val_t = val_c
            # if i < int(len(circle)/2):
            #    col = (val_c, 255-val_c, 100)
            # else:
            #    col = (255-val_t, val_t, 100)

            draw_circle(shift([x, y]), point_size, col, im=image)

        frames.append(image)

    return frames


def save_gif(images, filename, fps=5):
    im_frames = []
    images.reverse()
    saved = len(images)
    while images:
        byte_io = BytesIO()
        img = images.pop()
        img.save(byte_io, 'PNG', optimize=True)
        byte_io.seek(0)
        im_frames.append(imageio.imread(byte_io))
    imageio.mimwrite(filename, im_frames, format='gif', fps=fps)
    print(f"gif saved with {saved} frames.")


if succeed or not accepting_input:
    f = morph(radius=200, n=100, steps=10, point_size=1)
    # Add buffer to start and end
    f = ([f[0]]*5) + f + [f[-1]]*5
    save_gif(f, f"animation{inp1}{inp2}.gif")
