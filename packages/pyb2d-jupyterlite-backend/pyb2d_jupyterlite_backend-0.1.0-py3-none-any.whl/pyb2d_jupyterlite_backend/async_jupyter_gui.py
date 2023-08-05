import b2d
import asyncio
from b2d.testbed.backend.gui_base import GuiBase
import functools
import IPython
from b2d.testbed import TestbedBase
import time
from b2d.testbed.backend.jupyter.jupyter_batch_debug_draw import JupyterBatchDebugDraw


from ipycanvas import MultiCanvas, Canvas, hold_canvas
import ipywidgets
from ipywidgets import Label, HTML, Button, HBox, VBox

from .async_events import *


def wait_for_change(widget, value):
    future = asyncio.Future()

    def getvalue(change):
        # make the new value available
        future.set_result(change.new)
        widget.unobserve(getvalue, value)

    widget.observe(getvalue, value)
    return future


_id_to_gui = dict()


class JupyterAsyncGui(GuiBase):
    class Settings(GuiBase.Settings):
        class Config:
            arbitrary_types_allowed = True

        id: object = None

    def __init__(self, testbed_cls, settings, testbed_settings=None):

        self.id = settings.id
        if settings.id is None:
            settings.id = testbed_cls

        if settings.id in _id_to_gui:
            old_self = _id_to_gui[settings.id]
            old_self._terminate()
        _id_to_gui[settings.id] = self

        self.settings = settings
        self.resolution = self.settings.resolution

        # steping settings
        self._fps = settings.fps
        self._dt_s = 1.0 / self._fps

        # testworld
        if testbed_settings is None:
            testbed_settings = dict()
        self.testbed_settings = testbed_settings
        self.testbed_cls = testbed_cls
        self.testbed = None

        # debug_draw
        self.debug_draw = None
        self.flip_bit = False

        # todo!
        self._debug_draw_flags = self.settings.get_debug_draw_flags()

        # flag to stop loop
        self._exit = False

        self.scale = settings.scale
        self.translate = settings.translate

        self.paused = False
        self.reached_end = False

        self._last_screen_pos = None
        self._mouse_is_down = False

    def _terminate(self):
        if not self.paused:
            self.paused = True

    def make_testbed(self):

        if self.testbed is not None:
            self.testbed.say_goodbye_world()
        self.testbed = self.testbed_cls(settings=self.testbed_settings)

        # make debug draw
        self.debug_draw = JupyterBatchDebugDraw(
            self.canvas, flags=self._debug_draw_flags
        )
        self.debug_draw.screen_size = self.resolution
        self.debug_draw.scale = self.scale
        self.debug_draw.translate = self.translate
        self.debug_draw.flip_y = True
        self.testbed.set_debug_draw(self.debug_draw)

    def on_mouse_down(self, xpos, ypos):
        if not self.paused:
            self._mouse_is_down = True
            self._last_screen_pos = xpos, ypos
            pos = self.debug_draw.screen_to_world(self._last_screen_pos)
            pos = pos.x, pos.y

            self.testbed.on_mouse_down(pos)

    # moue callbacks
    def on_mouse_up(self, xpos, ypos):
        if not self.paused:
            self._mouse_is_down = False
            self._last_screen_pos = xpos, ypos
            pos = self.debug_draw.screen_to_world((xpos, ypos))
            pos = pos.x, pos.y

            self.testbed.on_mouse_up(pos)

    def on_mouse_move(self, xpos, ypos):
        if not self.paused:
            lxpos, lypos = self._last_screen_pos
            self._last_screen_pos = xpos, ypos

            pos = self.debug_draw.screen_to_world((xpos, ypos))
            pos = pos.x, pos.y

            handled_event = self.testbed.on_mouse_move(pos)
            if (
                not handled_event
                and self._mouse_is_down
                and self._last_screen_pos is not None
            ):
                dx, dy = xpos - lxpos, ypos - lypos

                translate = self.debug_draw.translate
                self.debug_draw.translate = (
                    translate[0] + dx,
                    translate[1] - dy,
                )

    def start_ui(self):
        # make the canvas
        self.canvas = Canvas(width=self.resolution[0], height=self.resolution[1])
        self.out = ipywidgets.Output()

        # _setup_ipywidgets_gui
        self._setup_ipywidgets_gui()
        # make the world
        self.make_testbed()

        self._events = [
            MouseDownEvent(widget=self.canvas, callback=self.on_mouse_down),
            MouseMoveEvent(widget=self.canvas, callback=self.on_mouse_move),
            MouseUpEvent(widget=self.canvas, callback=self.on_mouse_up),
        ]

        # d = IPyEvent(

        #     source=self.canvas, watched_events=["keydown", "keyup", "wheel"]
        # )
        return self

    async def _loop(self):
        if self.reached_end:
            self.reached_end = False

        event_futures = [e.get_future() for e in self._events]
        # wait_for_pause_future = wait_for_change(slider, 'value')
        # Event loop
        ii = 0

        done, not_done = await asyncio.wait(event_futures, timeout=0.0001)

        while not self.paused:
            t0 = time.time()
            self._single_step()
            t1 = time.time()
            delta = t1 - t0
            if delta < self._dt_s:
                timeout = self._dt_s - delta
            else:
                timeout = 0.0001
            done, not_done = await asyncio.wait(list(not_done), timeout=timeout)
            ii += 1

            # if ii % 1 == 0:
            #     #self.fantasy
            #     # self.out.clear_output(wait=True)
            #     with self.out:
            #         self.out.append_stdout(f"#done {len(done)} #not_done {len(not_done)}\n")
            #         #print("d",done, "nd",not_done)

            # in case of any event
            if len(done) >= 1:
                # assert False
                # self.out.append_stdout(f"{len(done)=} {len(not_done)=}\n")
                not_done = list(not_done) + [f.result().get_future() for f in done]

            t1 = time.time()
            delta = t1 - t0
            if delta < self._dt_s:
                timeout = self._dt_s - delta
                await asyncio.sleep(delta)

            if self._exit:
                break

    def _setup_ipywidgets_gui(self):

        IPython.display.display(self.canvas, self.out)  # , self.tab)
        # IPython.display.display(self.event_info)

    def _single_step(self):

        canvas = self.canvas

        with hold_canvas(canvas):
            canvas.clear()
            # self.debug_draw._canvas = canvas
            old_style = canvas.fill_style
            canvas.fill_style = "black"
            canvas.fill_rect(0, 0, self.resolution[0], self.resolution[1])

            self._step_world()

            canvas.fill_style = old_style

        # clear this one

    def _step_world(self):
        self.testbed.step(self._dt_s)
