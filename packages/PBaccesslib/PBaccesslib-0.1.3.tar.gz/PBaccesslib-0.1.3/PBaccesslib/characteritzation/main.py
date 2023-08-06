from PBaccesslib.characteritzation.dac_scan import DacScan
from PBaccesslib.characteritzation.disc_scan import DiscScan
from PBaccesslib.characteritzation.ifeed_scan import IfeedScan

pulses_width = 1000
pulses = 20
timer_reg = 1500
belt_dir = False
test_pulses = False
frames = 1


def dac_test(chip_reg, pixel_reg, folder_path, bridge):
    folder_path = folder_path + "dac_scan"
    table_test = [[500, 0, 1000, 5],
                  [600, 100, 1100, 5],
                  [700, 200, 1200, 5],
                  [800, 300, 1300, 5],
                  [900, 400, 1400, 5],
                  [1000, 500, 1500, 5]]
    error = False

    for dac_pos_arr in [[0, 2, 4], [1, 3, 5]]:
        for data_ref, data_low, data_max, data_incr in table_test:
            folder_name = f"DacScan_{dac_pos_arr[0]}_{data_ref}"
            dac_scan = DacScan(dac_pos_arr, data_ref, data_low, data_max, data_incr, bridge)
            error = dac_scan.test(pixel_reg, chip_reg, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames,
                                  folder_path, folder_name)
            if error:
                break
        if error:
            break

    return error


def disc_test(chip_reg, pixel_reg, folder_path, bridge):
    global PATH
    folder_path = folder_path + "disc_scan"
    table_test = [[False, 0],
                  [False, 3],
                  [False, 6],
                  [False, 9],
                  [False, 12],
                  [False, 15],
                  [True, 15],
                  [True, 12],
                  [True, 9],
                  [True, 6],
                  [True, 3],
                  [True, 2],
                  [True, 0]]
    data_ref = 500
    data_low = 200
    data_max = 800
    data_incr = 5
    error = False

    for dac_pos_arr in [[0, 2, 4], [1, 3, 5]]:
        for polarity, disc_value in table_test:
            folder_name = f"DiscScan_{dac_pos_arr[0]}_{polarity}_{disc_value}"
            disc_scan = DiscScan(dac_pos_arr, data_ref, data_low, data_max, data_incr, bridge)
            error = disc_scan.test(pixel_reg, chip_reg, polarity, disc_value, pulses_width, pulses, timer_reg, belt_dir,
                                   test_pulses, frames, folder_path, folder_name)
            if error:
                break
        if error:
            break

    return error


def ifeed_test(chip_reg, pixel_reg, folder_path, bridge):
    folder_path = folder_path + "ifeed_scan"
    table_test = [[False, 1],
                  [False, 4],
                  [False, 7],
                  [False, 10],
                  [False, 13],
                  [True, 8],
                  [True, 10],
                  [True, 12],
                  [True, 14],
                  [True, 15]]

    data_ref = 500
    data_low = 200
    data_max = 1000
    data_incr = 10
    dac_pos = [1, ]
    error = False

    for iffed_range, ifeed_value in table_test:
        folder_name = f"IfeedScan_dacpos_{dac_pos[0]}_{iffed_range}_{ifeed_value}"
        iffed_scan = IfeedScan(dac_pos, data_ref, data_low, data_max, data_incr, bridge)
        error = iffed_scan.test(pixel_reg, chip_reg, iffed_range, ifeed_value, pulses_width, pulses, timer_reg,
                                belt_dir, True, frames, folder_path, folder_name)
        if error:
            break

    return error
