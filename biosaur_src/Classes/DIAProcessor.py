import math

import numpy as np


class DIAProcessor:

    def __init__(self, ms1_result, ms2_data):
        self.ms1_result = ms1_result
        self.ms2_data = ms2_data

    def first_mz(self):
        return self.ms1_result['mz'].values[0]

    def last_mz(self):
        return self.ms1_result['mz'].values[-1]

    @staticmethod
    def simple_cos_correlation(int_list_ms2, int_list_ms1):
        top = sum([i1 * i2 for i1, i2 in zip(int_list_ms2, int_list_ms1)])
        bottom = math.sqrt(sum([numb * numb for numb in int_list_ms2])) * \
        math.sqrt(sum([numb * numb for numb in int_list_ms1]))
        return top / bottom

    @staticmethod
    def find_nearest_index(value, int_list_ms1):
        idx = int_list_ms1.searchsorted(value)
        idx = np.clip(idx, 1, len(int_list_ms1) - 1)
        left = int_list_ms1[idx - 1]
        right = int_list_ms1[idx]
        idx -= value - left < right - value
        return idx

    def prepare_list(self, int_list_ms2, int_list_ms1):
        new_list = [0 for i in int_list_ms1]
        for each in int_list_ms2:
            idx = self.find_nearest_index(each, int_list_ms1)
            new_list[idx] = each
        return new_list

    def process_dia(self, precursor_isolation_window):
        border_left = self.first_mz()
        border_right = border_left + precursor_isolation_window
        isolation_windows_correlations = []

        while border_right < self.last_mz():
            tmp_mz_ms1 = self.ms1_result['mz'].values
            i_right = np.array(tmp_mz_ms1) <= border_right
            i_left = np.array(tmp_mz_ms1) >= border_left
            answer_list = []
            for left, right in zip(i_left, i_right):
                if left and right:
                    answer_list.append(True)
                else:
                    answer_list.append(False)
            # correlation_ms1_mz_list = np.array(tmp_mz_ms1)[answer_list]
            correlation_ms1_intensity_list = np.array(self.ms1_result['intensity_1'].values)[answer_list]

            for ms2_instance in self.ms2_data:
                i_right = np.array(ms2_instance['m/z array']) <= border_right
                i_left = np.array(ms2_instance['m/z array']) >= border_left
                answer_list = []
                for left, right in zip(i_left, i_right):
                    if left and right:
                        answer_list.append(True)
                    else:
                        answer_list.append(False)
                # correlation_ms2_mz_list = np.array(ms2_instance['m/z array'])[answer_list]
                correlation_ms2_intensity_list = np.array(ms2_instance['intensity array'])[answer_list]

                if correlation_ms2_intensity_list:
                    correlation = self.simple_cos_correlation(correlation_ms2_intensity_list, correlation_ms1_intensity_list)
                    isolation_windows_correlations.append(correlation)
        return isolation_windows_correlations
