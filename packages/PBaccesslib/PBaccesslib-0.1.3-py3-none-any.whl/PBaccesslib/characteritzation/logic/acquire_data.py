import time
import numpy as np
from PBaccesslib.characteritzation.logic import logger


def acq_and_pop_data(bridge, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, chips_bitmap):
    bridge.use_reset_buffer()
    acq_error = _acq(bridge, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, chips_bitmap)
    if acq_error:
        return True, np.full(14400, 255, dtype=np.uint32)
    else:
        summed_data_frame = None

        for frame in range(frames):
            error, data_frame = _pop_frame(bridge)
            if error:
                logger.error("Time out to pop data frame.")
                return True, data_frame

            else:
                if frame == 0:
                    summed_data_frame = data_frame
                else:
                    summed_data_frame = np.add(summed_data_frame, data_frame)

        return False, summed_data_frame


def _acq(bridge, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, chips_bitmap):
    tries = 10
    while bridge.use_acq(pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames,
                         chips_bitmap) < 0 and tries != 0:
        logger.warning("Tries: {}".format(tries))
        time.sleep(0.2)
        tries -= 1
        if tries == 1:
            logger.error("Impossible to run correctly acq dll function.")
            return True

    return False


def _pop_frame(bridge):
    error, sample = bridge.use_pop_frame()
    return error, sample
