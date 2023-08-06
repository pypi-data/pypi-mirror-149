import datetime
import glob
import platform
import os
import numpy as np
import pandas as pd
from PBaccesslib import logger


class RowExtractor:
    def __init__(self, path, row_name_array, sep=","):
        self.path = path
        self.row_name_array = row_name_array
        self.sep = sep

    def normal_ext(self):
        out = []
        ch = pd.read_csv(self.path, sep=self.sep)
        for row_name in self.row_name_array:
            out.append(ch[row_name].values)
        return np.array(out)

    def replace_ext(self, replace_ch, replaced_ch):
        out = []
        ch = pd.read_csv(self.path, sep=self.sep).replace(replace_ch, replaced_ch, regex=True)

        for row_name in self.row_name_array:
            out.append(ch[row_name].values)
        return np.array(out)


class ManageCsv:
    def __init__(self):
        if platform.system() == "Linux":
            self.bar = "/"
        else:
            self.bar = "\\"

    def csv_names_inside_folder(self, path_where):
        return [os.path.basename(x) for x in glob.glob(path_where + '*.csv')]

    def create_folder(self, path_where, folder_name, add_time=False):
        if add_time:
            date_time = datetime.datetime.utcnow()
            str_date_time = date_time.strftime("%yy%mm%dd_%Hh%Mm%Ss")
            folder_path = path_where + self.bar + str_date_time + "_" + folder_name + self.bar
        else:
            folder_path = path_where + self.bar + folder_name + self.bar

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return folder_path

    def doc_creation(self, matrix, full_path, index_label=False, header=False, chunksize=100000, encoding='utf-8'):
        try:
            data_frame = pd.DataFrame(matrix)
            data_frame.to_csv(full_path
                              , header=header
                              , index=index_label
                              , chunksize=chunksize
                              , encoding=encoding)
        except FileNotFoundError:
            logger.error("No such file or directory")
