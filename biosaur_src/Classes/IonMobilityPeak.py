import numpy as np


class IonMobilityPeak:

    def __init__(self, mz, intensity, ion_mobility):
        self.mz_array = [mz, ]
        self.mass_array = [[mz, ], ]
        self.intensity_array = [[intensity, ]]
        self.ion_mobility_array = [[ion_mobility, ]]
        self.intensity_max = [intensity, ]
        self.ion_mobility_opt = [ion_mobility, ]
        self.ion_mobility_max = [ion_mobility, ]
        self.ion_mobility_min = [ion_mobility, ]
        self.total = 1

    def get_nearest_values(self, value):
        return np.argsort(np.abs(self.mz_array) - value)

    def extend(self, mz, intensity, ion_mobility):
        self.mz_array.append(mz)
        self.mass_array.append([mz, ])
        self.intensity_array.append([intensity, ])
        self.intensity_max.append(intensity)
        self.ion_mobility_opt.append(ion_mobility)
        self.ion_mobility_array.append([ion_mobility, ])
        self.ion_mobility_max.append(ion_mobility)
        self.ion_mobility_min.append(ion_mobility)
        self.total += 1

    def append_and_recalc(self, mz, intensity, ion_mobility, index):
        self.mass_array[index].append(mz)
        self.intensity_array[index].append(intensity)
        self.ion_mobility_array[index].append(ion_mobility)
        self.recalc(index)

    def recalc(self, index):
        self.mz_array[index] = np.mean(self.mass_array[index])
        self.ion_mobility_max[index] = max(self.ion_mobility_array[index])
        self.ion_mobility_min[index] = min(self.ion_mobility_array[index])
        if self.intensity_array[index][-1] > self.intensity_array[index][-2]:
            self.intensity_max[index] = self.intensity_array[index][-1]
            self.ion_mobility_opt[index] = self.ion_mobility_array[index][-1]

    def push_me_to_the_peak(self, mz, intensity, ion_mobility, diff):
        # nearest_ids = self.get_nearest_values(mz)
        flag = 0

        nearest_id = self.total - 1
        mass_accuracy = diff * 1e-6 * mz
        while nearest_id >= 0:
            tmp_diff = abs(self.mz_array[nearest_id] - mz)
            # tmp_diff = abs(self.mz_array[nearest_id] - mz) / mz
            # if tmp_diff <= diff * 1e-6:
            if tmp_diff <= mass_accuracy:
                if abs(
                        self.ion_mobility_max[nearest_id] -
                        ion_mobility) <= 0.1 or abs(
                        self.ion_mobility_min[nearest_id] -
                        ion_mobility) <= 0.1:
                    flag = 1
                    self.append_and_recalc(
                        mz, intensity, ion_mobility, nearest_id)
                    break
            else:
                break
            nearest_id -= 1

        if not flag:
            self.extend(mz, intensity, ion_mobility)
