class NextPeak:
    def __init__(
            self,
            next_mz_array,
            next_intensity_array,
            next_scan_id,
            next_ion_mobility_array):

        self.next_mz_array = next_mz_array
        self.next_intensity_array = next_intensity_array
        self.next_ion_mobility_array = next_ion_mobility_array
        self.next_scan_id = next_scan_id
