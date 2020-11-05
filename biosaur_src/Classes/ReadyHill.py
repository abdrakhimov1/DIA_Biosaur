import numpy as np


class ReadyHill:

    def __init__(self, intensity, scan_id, mass, ion_mobility):
        self.mz_std = np.std(mass)
        self.intensity = intensity
        self.scan_id = scan_id
        self.scan_set = set(scan_id)
        self.mass = mass
        self.diff_for_output = 0
        tmp = max(range(len(self.intensity)), key=self.intensity.__getitem__)
        self.scan_of_max_intensity = self.scan_id[tmp]
        self.max_intensity = self.intensity[tmp]
        self.mz = np.average(self.mass, weights=self.intensity)
        # self.mz = self.mass[tmp]
        # self.max_intensity = sum(self.intensity)
        if not (ion_mobility is None):
            self.ion_mobility = ion_mobility
            self.opt_ion_mobility = self.ion_mobility[tmp]
        else:
            self.ion_mobility = None
            self.opt_ion_mobility = None
        self.scan_len = len(self.scan_id)

        self.idict = dict()
        for i, j in zip(self.scan_id, self.intensity):
            self.idict[i] = j
        intensity_np = np.array(intensity)
        self.sqrt_of_i_sum_squares = np.sqrt(np.sum(np.power(intensity_np, 2)))