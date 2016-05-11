from hal.outputs.rgbled import RGBLED
from enum import Enum
import datetime
import sys

STATUS_TIMEOUT = datetime.timedelta(seconds=1)


class STATUS(Enum):
    normal = 0      # green
    evaluating = 1  # cyan
    horny = 2       # yellow
    mating = 3      # red


class StatusLED(RGBLED):
    def __init__(self, config_options=None):
        super().__init__(config_options)

        self._status = None
        self._last_update = datetime.datetime.now() - (STATUS_TIMEOUT*2)
        self.set_status(STATUS.normal)

    def set_status(self, status):
        if self._status == status:
            return

        if status == STATUS.normal:
            # if not enough time passed since last update
            if self._last_update + STATUS_TIMEOUT > datetime.datetime.now():
                return

            color = self._green
        elif status == STATUS.evaluating:
            color = self._cyan
        elif status == STATUS.horny:
            color = self._yellow
        elif status == STATUS.mating:
            color = self._red
        else:
            # error
            print("invalid status update: {}".format(status), file=sys.stderr)
            return

        self._status = status
        self._last_update = datetime.datetime.now()
        self.set_color(color)
