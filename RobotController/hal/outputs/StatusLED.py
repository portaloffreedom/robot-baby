from hal.outputs.rgbled import RGBLED
from enum import Enum
import datetime
import sys


STATUS_TIMEOUT = datetime.timedelta(seconds=1)


class StatusLED(RGBLED, Enum):
    normal = 0      # green
    evaluating = 1  # cyan
    horny = 2       # yellow
    mating = 3      # red

    def __init__(self, config_options=None):
        super().__init__(config_options)

        self._status = None
        self._last_update = datetime.datetime.now()
        self.set_status(StatusLED.normal)

    def set_status(self, status):
        if self._status == status:
            return
        self._status = status

        if status == StatusLED.normal:
            # if not enough time passed since last update
            if self._last_update + STATUS_TIMEOUT > datetime.datetime.now():
                return

            color = self._green
        elif status == StatusLED.evaluating:
            color = self._cyan
        elif status == StatusLED.horny:
            color = self._yellow
        elif status == StatusLED.mating:
            color = self._red
        else:
            # error
            print("invalid status update: {}".format(status), file=sys.stderr)
            return

        self._last_update = datetime.datetime.now()
        self.set_color(color)
