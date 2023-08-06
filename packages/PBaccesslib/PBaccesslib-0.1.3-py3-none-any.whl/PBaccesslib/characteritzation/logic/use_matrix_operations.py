import numpy as np

# 11 DAC5 disc value, 12 pol, 13 range, 14 mask
# 15 DAC4 disc value, 16 pol, 17 range, 18 mask
# 19 DAC3 disc value, 20 pol, 21 range, 22 mask
# 23 DAC2 disc value, 24 pol, 25 range, 26 mask
# 27 DAC1 disc value, 28 pol, 29 range, 30 mask
# 31 DAC0 disc value, 32 pol, 33 range, 34 mask

# Global variables pixel register
pr_mask_array_pos = [(34,), (30,), (26,), (22,), (18,), (14,)]
pr_disc_array_pos = [(31,), (27,), (23,), (19,), (15,), (11,)]
pr_pol_array_pos = [(32,), (28,), (24,), (20,), (16,), (12,)]
pr_feed_range = [(2,), ]
pr_feed_value = [(37,), ]
pr_tpena_pos = [(36,), ]
# Global variables chip register
chip_reg_array_pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]

""" Pixel register functions """


def pr_unmask(pixel_reg, dac_pos):
    return replace_values(pixel_reg, pr_mask_array_pos[dac_pos], 0, 0, ">=")


def pr_mask(pixel_reg, dac_pos):
    return replace_values(pixel_reg, pr_mask_array_pos[dac_pos], 0, 1, ">=")


def pr_tpena_off(pixel_reg):
    return replace_values(pixel_reg, pr_tpena_pos[0], 0, 0, ">=")


def pr_tpena_on(pixel_reg):
    return replace_values(pixel_reg, pr_tpena_pos[0], 0, 1, ">=")


def pr_set_disc(pixel_reg, dac_pos, new_value):
    return replace_values(pixel_reg, pr_disc_array_pos[dac_pos], 0, new_value, ">=")


def pr_range_true(pixel_reg, dac_pos):
    return replace_values(pixel_reg, pr_pol_array_pos[dac_pos], 0, 1, ">=")


def pr_range_false(pixel_reg, dac_pos):
    return replace_values(pixel_reg, pr_pol_array_pos[dac_pos], 0, 0, ">=")


def pr_set_ifeed(pixel_reg, new_value):
    return replace_values(pixel_reg, pr_feed_value[0], 0, new_value, ">=")


def pr_feed_true_all(pixel_reg):
    return replace_values(pixel_reg, pr_feed_range[0], 0, 1, ">=")


def pr_feed_false_all(pixel_reg):
    return replace_values(pixel_reg, pr_feed_range[0], 0, 0, ">=")


def cr_set_dac(chip_register, dac_pos, new_value):
    val = int((new_value - 0.75) * 0x7FF)
    return replace_values(chip_register, chip_reg_array_pos[dac_pos], 0, val, ">=")


def replace_values(matrix, tuple_pos, old_value, new_value, compare_type):
    try:
        if compare_type == ">=":
            mask = matrix[tuple_pos] >= old_value
        elif compare_type == ">":
            mask = matrix[tuple_pos] > old_value
        elif compare_type == "<=":
            mask = matrix[tuple_pos] <= old_value
        elif compare_type == "<":
            mask = matrix[tuple_pos] < old_value
        else:
            # compare_type == "=="
            mask = matrix[tuple_pos] == old_value

        sub_array = np.where(mask, new_value, matrix[tuple_pos])
        matrix[tuple_pos] = sub_array

        return matrix
    except IndexError:
        raise IndexError
