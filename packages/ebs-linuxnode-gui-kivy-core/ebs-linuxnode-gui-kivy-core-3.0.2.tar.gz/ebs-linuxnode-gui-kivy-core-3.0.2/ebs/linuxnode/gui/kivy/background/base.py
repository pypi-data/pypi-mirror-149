

import time


class BackgroundProviderBase(object):
    is_visual = True

    def __init__(self, actual):
        self._actual = actual
        self._widget = None
        self._end_call = None
        self._paused = False
        self._eresidual = None
        self._callback = None

    @property
    def actual(self):
        if hasattr(self._actual, 'actual'):
            return self._actual.actual
        else:
            return self._actual

    def check_support(self, target):
        # Check if the provider supports the target and
        # if the target exists.
        raise NotImplementedError

    def play(self, target, duration=None, callback=None, **kwargs):
        # Create a Widgetized Background and return it.
        # It will be attached later.
        if duration and callback:
            self._callback = callback
            self._end_call = self.actual.reactor.callLater(duration, callback)

    def stop(self):
        # Stop and unload the Widgetized Background.
        # The widget has already been detached.
        if self._end_call and self._end_call.active():
            self._end_call.cancel()
        self._widget = None

    def pause(self):
        # Pause the Widgetized Background.
        # It has already been detached.
        if self._paused:
            return
        if self._end_call and self._end_call.active():
            ietime = self._end_call.getTime()
            ptime = time.time()
            self._eresidual = ietime - ptime
            self._end_call.cancel()
        self._paused = True

    def resume(self):
        # Resume the Widgetized Background.
        # It will be attached later.
        if not self._paused:
            return
        self._paused = False
        if self._eresidual:
            self._end_call = self.actual.reactor.callLater(self._eresidual, self._callback)
            self._eresidual = None
