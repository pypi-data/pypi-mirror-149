import numpy as np
from PBaccesslib.wafer_test import main as wafer_main
from PBaccesslib.characteritzation import main as charac_main
from PBaccesslib.doc_operations import ManageCsv
from PBaccesslib import logger, CHIP_REG_PATH, PIXEL_REG_PATH


def chip_test(row: int, column: int, wafer_pos: int, data_folder_path: str, bridge, instrument):
    """
    Execute probecard main test.
    :param row: Chip row.
    :param column: Chip column.
    :param wafer_pos: Wafer position.
    :param data_folder_path
    :param bridge
    :param instrument
    :return: Error return.
    """

    """ Load chip_reg and pixel_reg initial config"""
    try:
        chip_reg = np.load(CHIP_REG_PATH)
        pixel_reg = np.load(PIXEL_REG_PATH)
    except FileNotFoundError:
        logger.error("Check init_config.txt. CHIP_REG_PATH or PIXEL_REG_PATH are not okay.")
        return 1

    """Main folder creation"""
    gen_doc = ManageCsv()
    new_folder_path = gen_doc.create_folder(data_folder_path, f"wafer_{wafer_pos}")
    new_folder_path = gen_doc.create_folder(new_folder_path, f"chip_{row}_{column}")
    td_bin_array, error_programing = wafer_main.test(chip_reg, pixel_reg, bridge, instrument, new_folder_path)
    if sum(td_bin_array) != len(td_bin_array):
        logger.error(f"The output from wafer_test is : {td_bin_array}")
        return 2
    else:
        logger.info(f"The output from wafer_test is : {td_bin_array}")
    if error_programing:
        return 3
    error_dac = charac_main.dac_test(chip_reg, pixel_reg, new_folder_path, bridge)
    if error_dac:
        return 4
    error_disc = charac_main.disc_test(chip_reg, pixel_reg, new_folder_path, bridge)
    if error_disc:
        return 5
    error_ifeed = charac_main.ifeed_test(chip_reg, pixel_reg, new_folder_path, bridge)
    if error_ifeed:
        return 6

    return 0


def chip_test_iffed(row: int, column: int, wafer_pos: int, data_folder_path: str, bridge, instrument):
    """
    Execute probecard main test.
    :param row: Chip row.
    :param column: Chip column.
    :param wafer_pos: Wafer position.
    :param data_folder_path
    :param bridge
    :param instrument
    :return: Error return.
    """

    """ Load chip_reg and pixel_reg initial config"""
    try:
        chip_reg = np.load(CHIP_REG_PATH)
        pixel_reg = np.load(PIXEL_REG_PATH)
    except FileNotFoundError:
        logger.error("Check init_config.txt. CHIP_REG_PATH or PIXEL_REG_PATH are not okay.")
        return 1

    """Main folder creation"""
    gen_doc = ManageCsv()
    new_folder_path = gen_doc.create_folder(data_folder_path, f"wafer_{wafer_pos}")
    new_folder_path = gen_doc.create_folder(new_folder_path, f"chip_{row}_{column}")
    td_bin_array, error_programing = wafer_main.test(chip_reg, pixel_reg, bridge, instrument, new_folder_path)
    if sum(td_bin_array) != len(td_bin_array):
        logger.error(f"The output from wafer_test is : {td_bin_array}")
        return 2
    else:
        logger.info(f"The output from wafer_test is : {td_bin_array}")
    if error_programing:
        return 3
    error_ifeed = charac_main.ifeed_test(chip_reg, pixel_reg, new_folder_path, bridge)
    if error_ifeed:
        return 6

    return 0
