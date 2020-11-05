from pyteomics import mzml
import numpy as np


class DataGetter:
    def __init__(self, input_mzml_path, min_intensity):
        self.input_mzml_path = input_mzml_path
        self.min_intensity = min_intensity

    def get_data(self, ms_level):
        data_for_analyse = []
        for z in mzml.read(self.input_mzml_path):
            if z['ms level'] == ms_level:
                if 1:
                    idx = z['intensity array'] >= self.min_intensity
                    z['intensity array'] = z['intensity array'][idx]
                    z['m/z array'] = z['m/z array'][idx]
                    if 'mean inverse reduced ion mobility array' in z:
                        z['mean inverse reduced ion mobility array'] = z['mean inverse reduced ion mobility array'][idx]

                    idx = np.argsort(z['m/z array'])
                    z['m/z array'] = z['m/z array'][idx]
                    z['intensity array'] = z['intensity array'][idx]
                    if 'mean inverse reduced ion mobility array' in z:
                        z['mean inverse reduced ion mobility array'] = z['mean inverse reduced ion mobility array'][idx]
                    data_for_analyse.append(z)
        return data_for_analyse
