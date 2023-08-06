from PBaccesslib.doc_operations import ManageCsv
from PBaccesslib.wafer_test import logger


def touchdown_test(bridge):
    """"""
    error, out = bridge.use_read_touchdown()
    if error < 0:
        logger.error("Error reading read_touchdown!")
        return [0, 0]

    if out == 3:
        bin_array = [1, 1]
    elif out == 1:
        bin_array = [0, 1]
    elif out == 2:
        bin_array = [1, 0]
    else:
        bin_array = [0, 0]

    return bin_array


def keithley_test(inst, folder_path, ):
    # gpib = "GPIB0::26::INSTR"
    try:
        bin_array, test_output = inst.main(100e-3, 100e-3, 20, 2.5, 2.2, 10e-3, 2.2, 10e-3)
        gen_doc = ManageCsv()
        gen_doc.doc_creation(test_output, folder_path + f"consumption.txt")
        return bin_array
    except ConnectionError:
        logger.error("Error connecting with instrument")
        return [0, 0, 0, 0]
