from b2d.testbed.backend.jupyter.jupyter_batch_debug_draw import JupyterBatchDebugDraw
from b2d import vec2, Vec2
import numpy as np

from ipycanvas import Canvas, hold_canvas
import IPython
import asyncio
import time
import functools


def render_world(world, ppm=20, flags=None, world_margin=None, bounding_box=None):
    if world_margin is None:
        world_margin = Vec2(0, 0)
    world_margin = Vec2(world_margin[0], world_margin[1])

    if bounding_box is None:
        lower_left, top_right = world.get_world_aabb()
    else:
        lower_left, top_right = bounding_box

    lower_left = vec2(lower_left)
    top_right = vec2(top_right)
    lower_left, top_right = world.get_world_aabb()
    lower_left -= world_margin
    top_right += world_margin
    world_size = top_right - lower_left

    image_size = world_size * ppm
    shape = [int(image_size[0] + 0.5), int(image_size[1] + 0.5)]

    image = np.zeros(shape + [3], dtype="uint8")
    canvas = Canvas()
    canvas.width = shape[0]
    canvas.height = shape[1]

    debug_draw = JupyterBatchDebugDraw(canvas=canvas, flags=flags)
    debug_draw.flip_y = True
    debug_draw.scale = ppm
    debug_draw.screen_size = shape
    t = (-ppm * lower_left[0], -ppm * lower_left[1])
    debug_draw.translate = t

    # draw the world with a temporary debug draw
    # (will restore the old debug draw after the call)
    def callback():
        world.draw_debug_data()

    canvas.fill_style = "black"
    canvas.fill_rect(0, 0, shape[0], shape[1])
    world.with_temporary_debug_draw(debug_draw, callback=callback)

    return canvas


def plot_world(*args, **kwargs):
    canvas = render_world(*args, **kwargs)
    IPython.display.display(canvas)


def animate_world(
    world,
    ppm=20,
    flags=None,
    world_margin=None,
    fps=24,
    t=3,
    bounding_box=None,
    pre_step=None,
    post_step=None,
):
    if flags is None:
        flags = ["shape", "joint", "particle"]

    if world_margin is None:
        world_margin = Vec2(0, 0)
    world_margin = Vec2(world_margin[0], world_margin[1])

    if bounding_box is None:
        lower_left, top_right = world.get_world_aabb()
    else:
        lower_left, top_right = bounding_box

    lower_left = vec2(lower_left)
    top_right = vec2(top_right)

    lower_left -= world_margin
    top_right += world_margin
    world_size = top_right - lower_left

    image_size = world_size * ppm
    shape = [int(image_size[0] + 0.5), int(image_size[1] + 0.5)]

    canvas = Canvas()
    canvas.width = shape[0]
    canvas.height = shape[1]
    IPython.display.display(canvas)

    debug_draw = JupyterBatchDebugDraw(canvas=canvas, flags=flags)

    debug_draw.flip_y = True
    debug_draw.scale = ppm
    debug_draw.screen_size = shape
    translate = (-ppm * lower_left[0], -ppm * lower_left[1])
    debug_draw.translate = translate

    dt = 1.0 / fps
    n_steps = int(t / dt + 0.5)

    image_list = []

    def busy_sleep(s):
        ms = s * 1000.0

        def current_milli_time():
            return time.time() * 1000.0

        t0 = current_milli_time()
        while True:
            t1 = current_milli_time()
            if t1 - t0 >= ms:
                break

    def callback(w):
        w.draw_debug_data()
        for i in range(n_steps):

            t0 = time.time()
            if pre_step is not None:
                pre_step(dt)
            w.step(dt, 1, 1)
            if post_step is not None:
                post_step(dt)
            with hold_canvas(canvas):
                canvas.clear()
                canvas.fill_style = "black"
                canvas.fill_rect(0, 0, shape[0], shape[1])
                w.draw_debug_data()

                t1 = time.time()
                delta = t1 - t0
                if delta < dt:
                    timeout = dt - delta
                    busy_sleep(timeout)

    world.with_temporary_debug_draw(
        debug_draw, callback=functools.partial(callback, w=world)
    )
