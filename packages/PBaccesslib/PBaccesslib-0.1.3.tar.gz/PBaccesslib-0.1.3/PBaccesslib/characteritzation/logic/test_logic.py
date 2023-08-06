import numpy as np
from PBaccesslib import BITMAP
from PBaccesslib.characteritzation.logic import logger
from PBaccesslib.doc_operations import ManageCsv
from Bconvertacceslib.use_linda_data_manager import use_chip_reg_to_pack_data, simple_data_unpack
from PBaccesslib.characteritzation.logic.use_matrix_operations import pr_unmask, pr_mask
from PBaccesslib.characteritzation.logic.acquire_data import acq_and_pop_data


class Scan:
    def __init__(self, dac_pos_arr: list, data_ref: int, data_low: int, data_max: int,
                 data_incr: int):
        self.ERROR_MAX_ITERATIONS = 10
        self.CHIP_ANALYZED = 0
        self.DAC_REF_POS = 8
        self.data_ref = data_ref
        self.data_low = data_low
        self.data_max = data_max
        self.data_incr = data_incr
        self.dac_pos_arr = dac_pos_arr

    def mask_unmask_disc(self, pixel_reg):
        md_cr = pixel_reg
        all_dac_pos = [0, 1, 2, 3, 4, 5]
        remaining_pos = list(set(all_dac_pos).symmetric_difference(set(self.dac_pos_arr)))
        for dac_pos in self.dac_pos_arr:
            md_cr = pr_unmask(md_cr, dac_pos)
        for dac_pos in remaining_pos:
            md_cr = pr_mask(md_cr, dac_pos)

        return md_cr

    def loop_scan(self, md_cr, pulses_width, pulses, timer_reg, belt_dir, test_pulses, frames, bridge):
        container = []
        iter_dac = 0
        counter_error = 0
        error = False

        times_incr = int((self.data_max - self.data_low) / self.data_incr)

        for time_incr in range(times_incr):
            if counter_error >= self.ERROR_MAX_ITERATIONS:
                logger.error(f"Exit program,  counter_error >= {self.ERROR_MAX_ITERATIONS}")
                error = True
                break

            """Making one acq for all chips"""

            summed_data = None
            for i in range(self.ERROR_MAX_ITERATIONS):
                error, summed_data = acq_and_pop_data(bridge, pulses_width, pulses, timer_reg, belt_dir,
                                                      test_pulses, frames, BITMAP)
                if not error:
                    break
                else:
                    counter_error += 1

            container.append(summed_data)
            iter_dac += 1

            """ ¡¡¡¡¡Here changing chip register matrix!!!!!"""
            for dac_pos in self.dac_pos_arr:
                data_incremented = np.add(md_cr[0][dac_pos], + self.data_incr)
                md_cr, error = self.replace_data_in_matrix(md_cr, data_incremented, (0, dac_pos))

            pack_data = use_chip_reg_to_pack_data(md_cr)
            bridge.use_chip_register_write(pack_data, BITMAP)

        logger.info(f"Iterations done in scan test: {iter_dac}")

        list_data = np.reshape(container, -1)
        all_counters_data = simple_data_unpack(list_data, (iter_dac, 30, 160, 6))
        return error, all_counters_data

    def save_data(self, all_counters_data, folder_path: str, folder_name: str):
        gen_doc = ManageCsv()
        folder_path = gen_doc.create_folder(folder_path, folder_name, add_time=True)
        iter_dac = len(all_counters_data)

        # [DAC_VALUE][ACQ_DATA][PIXELS]
        disc_charac_mx = all_counters_data.transpose((1, 3, 0, 2))[self.CHIP_ANALYZED]
        data_new = np.flip(disc_charac_mx, 2)
        # [DAC_VALUE][ACQ_DATA][PIXELS ROW][PIXEL COLUMNS]
        data_new = np.reshape(data_new, (len(data_new), len(data_new[0]), 8, 20))
        data_new = np.flip(data_new, 2)
        # [DAC_VALUE][PIXELS ROW][PIXEL COLUMNS][ACQ_DATA]
        data_new = data_new.transpose((0, 2, 3, 1))

        """Generating the corresponding csv"""
        for dac_pos in self.dac_pos_arr:
            # [PIXELS ROW][PIXEL COLUMNS][ACQ_DATA]
            new_chip_data = data_new[dac_pos].reshape((len(data_new[dac_pos]) * len(data_new[dac_pos][0])), iter_dac)
            gen_doc.doc_creation(new_chip_data, folder_path + f"DAC{dac_pos}")

        return False

    def replace_data_in_matrix(self, in_matrix, new_value_matrix, pos_tuple):
        try:
            in_matrix[pos_tuple] = new_value_matrix
            return in_matrix, False
        except ValueError:
            return in_matrix, True
