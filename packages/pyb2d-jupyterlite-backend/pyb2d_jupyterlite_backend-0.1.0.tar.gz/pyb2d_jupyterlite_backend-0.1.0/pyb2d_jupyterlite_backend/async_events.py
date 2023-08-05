import asyncio


class Event(object):
    def get_future(self):
        raise NotImplemented()


class MouseDownEvent(Event):
    def __init__(self, widget, callback):
        super(MouseDownEvent, self).__init__()
        self._widget = widget
        self._callback = callback

    def on_mouse_down(self, x, y):
        self._callback(x, y)
        future.set_result(self)
        self._widget.on_mouse_down(self.on_mouse_down, remove=True)

    def get_future(self):
        future = asyncio.Future()
        self._widget.on_mouse_down(self.on_mouse_down)
        return future


class MouseMoveEvent(Event):
    def __init__(self, widget, callback):
        super(MouseMoveEvent, self).__init__()
        self._widget = widget
        self._callback = callback

    def on_mouse_move(self, x, y):
        self._callback(x, y)
        future.set_result(self)
        self._widget.on_mouse_move(self.on_mouse_move, remove=True)

    def get_future(self):
        future = asyncio.Future()
        self._widget.on_mouse_move(self.on_mouse_move)
        return future


class MouseUpEvent(Event):
    def __init__(self, widget, callback):
        super(MouseUpEvent, self).__init__()
        self._widget = widget
        self._callback = callback

    def on_mouse_up(self, x, y):
        self._callback(x, y)
        future.set_result(self)
        self._widget.on_mouse_up(on_mouse_up, remove=True)

    def get_future(self):
        future = asyncio.Future()

        self._widget.on_mouse_up(self.on_mouse_up)
        return future
