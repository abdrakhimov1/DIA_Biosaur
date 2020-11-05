import numpy as np
import math
import itertools


class Feature:

    def __init__(self, finished_hills, each, each_id, negative_mode, isotopes_mass_error_map):

        self.charge = each[1][0][1]
        self.shift = each[3]
        mass_for_average2 = [np.average(finished_hills[each[0]].mass, weights=finished_hills[each[0]].intensity)]
        intensity_for_average2 = [finished_hills[each[0]].max_intensity, ]
        self.mz = np.average(mass_for_average2, weights=intensity_for_average2)
        intensity_for_average = finished_hills[each[0]].intensity + list(itertools.chain.from_iterable(finished_hills[ech[0]].intensity for ech in each[1]))
        scans_for_average = finished_hills[each[0]].scan_id + list(itertools.chain.from_iterable(finished_hills[ech[0]].scan_id for ech in each[1]))
        self.negative_mode = negative_mode
        if negative_mode:
            self.neutral_mass = self.mz * self.charge + \
                1.0072765 * self.charge - self.shift * 1.00335
        else:
            self.neutral_mass = self.mz * self.charge - \
                1.0072765 * self.charge - self.shift * 1.00335
        self.isotopes_numb = len(each[1])
        self.scan_numb = len(finished_hills[each[0]].scan_id)
        self.scans = finished_hills[each[0]].scan_id
        self.id_for_scan = finished_hills[each[0]].intensity.index(
            max(finished_hills[each[0]].intensity))
        self.intensity = finished_hills[each[0]].max_intensity
        self.idict = finished_hills[each[0]].idict
        self.sqrt_of_i_sum_squares = math.sqrt(
            sum(v**2 for v in self.idict.values()))
        self.scan_set = finished_hills[each[0]].scan_set
        if not (finished_hills[each[0]].ion_mobility is None):
            self.ion_mobility = finished_hills[each[0]].opt_ion_mobility
        else:
            self.ion_mobility = None
        self.scan_id = int(np.average(scans_for_average, weights=intensity_for_average))
        self.RT = int(np.average(scans_for_average, weights=intensity_for_average))
        self.sulfur = (each[1][1][4] if len(each[1]) > 1 else -1)
        self.cos_corr = each[4][0]
        self.cos_corr_2 = each[4][1]
        self.corr_fill_zero = each[4][2]
        self.diff_for_output = each[4][3]
        self.intensity_1 = each[4][4]
        self.scan_id_1 = each[4][5]
        self.mz_std_1 = each[4][6]
        self.intensity_2 = each[4][7]
        self.scan_id_2 = each[4][8]
        self.mz_std_2 = each[4][9]
        self.id = each_id
