from essentia.standard import *
from essentia import Pool, array
from scipy.spatial.distance import *

import os
import numpy as np

def generate_training_set_from_assignments(dataset_path):
    for dirpath, dnames, fnames in os.walk(dataset_path):
        for f in fnames:
            if 'ref' in f:
                reference = f
                assignment = _find_assignment_for_reference(dataset_path, reference)
                if assignment is not None:
                    _fetch_distance_entries_for_assignment(dataset_path, reference, assignment)

def _fetch_distance_entries_for_assignment(dataset_path, reference, assignment):
    signal_reference = _load_file_as_monophonic_waveform(os.path.join(dataset_path, reference))
    signal_assignment = _load_file_as_monophonic_waveform(os.path.join(dataset_path, assignment))

    signals = [signal_reference, signal_assignment]

    onset_vectors = [_extract_onset_vectors(signal_reference), _extract_onset_vectors(signal_assignment)]

    # TODO Check if reference and student performance
    # have the same number of beats and apply noise
    # thresholding to equalize this number
    if len(onset_vectors[0]) != len(onset_vectors[1]):
        # Change noise threshold
    else:
        # Calculate vector distances

def _load_file_as_monophonic_waveform(file_path):
    fs = 44100

    x = MonoLoader(filename = file_path, sampleRate = fs)()
    return x/np.max(np.abs(x))

def _extract_onset_vectors(waveform):
    window_size = 1024
    hop_size = 512
    od_hfc = OnsetDetection(method='hfc')
    w = Windowing(type = 'hann')
    fft = FFT()
    c2p = CartesianToPolar()
    onsets = Onsets()

    pool = Pool()
    for frame in FrameGenerator(waveform, frameSize = window_size, hopSize = hop_size):
        mag, phase, = c2p(fft(w(frame)))
        pool.add('features', od_hfc(mag, phase))

    onsets = onsets(array([pool['features']]),[1])
    return onsets

def _find_assignment_for_reference(dataset_path, reference):
    reference_id = reference.split("_")[2].replace("ref","").split(".")[0]
    for dirpath, dnames, fnames in os.walk(dataset_path):
        for f in fnames:
            if reference_id in f and not 'ref' in f:
                return f

if __name__ == '__main__':
    generate_training_set_from_assignments('data/MAST_rhythm_subset')