from Excelacceslib.excel_matrix_manage import get_linda_matrix




def get_mx_to_save(path):
    chip_reg, pixel_reg = get_linda_matrix(path)
    chip_reg = chip_reg[:, :, 0:1]  # (1, 19, 30) -> (1, 19, 1)
    pixel_reg = pixel_reg[:, 0:1, :, :]  # (44, 30, 8, 20) -> (44, 1, 8, 20)
    return chip_reg, pixel_reg
