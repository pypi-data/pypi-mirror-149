from Bconvertacceslib.use_linda_data_manager import use_chip_reg_to_pack_data, use_pixel_reg_to_pack_data
from PBaccesslib.wafer_test import logger
from PBaccesslib import BITMAP


def read_write_test(chip_reg, pixel_reg, bridge):
    error = False
    tries = 10
    error_max = 2
    count_error = 0

    for _try in range(tries):
        chip_error = full_array_chip_register_write(chip_reg, bridge)
        pixel_error = full_array_pixel_register_write(pixel_reg, bridge)

        if chip_error or pixel_error:
            logger.error(f"Error reading / writing dll full_array_programing_registers in try: {_try}")
            error = True
            count_error += 1

        if count_error >= error_max:
            break
    return error


def full_array_chip_register_write(chip_reg, bridge):
    pack_data = use_chip_reg_to_pack_data(chip_reg)
    error = bridge.use_full_array_chip_register_write(pack_data, BITMAP)

    if error == -1:
        logger.error("Error reading writing dll full_array_chip_register_read")
        return True
    else:
        return False


def full_array_pixel_register_write(pixel_reg, bridge):
    pack_data = use_pixel_reg_to_pack_data(pixel_reg)
    error = bridge.use_full_array_pixel_register_write(pack_data, BITMAP)

    if error < 0:
        logger.error("Error reading writing dll full_array_chip_register_read")
        return True
    else:
        return False
