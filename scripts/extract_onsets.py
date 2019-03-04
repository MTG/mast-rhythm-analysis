from essentia.standard import *
from essentia import Pool, array

import numpy
import math

def _load_file_as_monophonic_waveform(file_path):
    fs = 44100

    x = MonoLoader(filename = file_path, sampleRate = fs)()
    return x/numpy.max(numpy.abs(x))

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

def extract_onsets(base_dir, list_files, output_file):
    with open(list_files, 'r') as listfiles:
        with open(output_file, 'w') as output:
            for audio_file in listfiles.readlines():
                audio_file = audio_file.strip()
                audio_file_full_path = '%s%s' % (base_dir, audio_file)

                w = _load_file_as_monophonic_waveform(audio_file_full_path)
                onsets = _extract_onset_vectors(w)


                output.write('%s\n' % " ".join(list(str(x) for x in onsets)))

def rescale_and_make_bins(performances_file, references_file, window_size=0.2):
    with open(performances_file, 'r') as perf_onsets_file:
        with open(references_file, 'r') as ref_onsets_file:
            perfs_onsets = perf_onsets_file.readlines()
            refs_onsets = ref_onsets_file.readlines()
            with open('%s [BINS]' % performances_file, 'w') as performances_file_bin, open('%s [BINS]' % references_file, 'w') as references_file_bin:
                for i in range(len(perfs_onsets)):
                    perf_onsets = [ float(x) for x in perfs_onsets[i].strip().split(" ") ]
                    ref_onsets = [ float(x) for x in refs_onsets[i].strip().split(" ") ]

                    # setting onset boundaries from first to last onsets
                    perf_onsets = [ x - perf_onsets[0] for x in perf_onsets ]
                    ref_onsets = [ x - ref_onsets[0] for x in ref_onsets ]

                    # re-scaling performance to match reference tempo
                    perf_inner_duration = perf_onsets[-1] - perf_onsets[0]
                    ref_inner_duration = ref_onsets[-1] - ref_onsets[0]
                    time_rescaling_factor = ((perf_inner_duration - ref_inner_duration) / perf_inner_duration)

                    rescaled_perf_onsets = [adjust_onset_by_rate(onset, time_rescaling_factor) for onset in perf_onsets]

                    performance_onset_bins = make_bins(rescaled_perf_onsets, window_size)
                    performances_file_bin.write('%s\n' % " ".join([str(x) for x in performance_onset_bins]))

                    references_onset_bins = make_bins(ref_onsets, window_size)
                    references_file_bin.write('%s\n' % " ".join([str(x) for x in references_onset_bins]))

def make_bins(onset_times, windows_size):
    total_length = onset_times[-1] - onset_times[0]
    n_bins = math.ceil(total_length/windows_size)
    bins = []

    for i in range(int(n_bins)):
        for onset_time in onset_times:
            if windows_size*i <= onset_time <= windows_size*(i+1):
                bins.append(1)
                break
        else:
            bins.append(0)

    return bins

def adjust_onset_by_rate(onset, time_rescaling_factor):
    return onset - (onset * time_rescaling_factor)

if __name__ == "__main__":
    # # directory that contains audio files
    # base_dir_performances = '../Experiment Data/Only Performances/'
    # # text file with all file names
    # list_files_performances = '../Experiment Data/listperformances'
    # # file that will store the onsets
    # output_file_performances = '../Experiment Data/MAST Onsets [Performances]'

    # extract_onsets(base_dir_performances, list_files_performances, output_file_performances)

    #  # directory that contains audio files
    # base_dir_references = '../Experiment Data/Only References/'
    # # text file with all file names
    # list_files_references = '../Experiment Data/listreferences'
    # # file that will store the onsets
    # output_file_references = '../Experiment Data/MAST Onsets [References]'

    # extract_onsets(base_dir_references, list_files_references, output_file_references)
    rescale_and_make_bins('/home/felipe/workspace/mast-rhythm-analysis/Experiment Data/MAST Onsets [Performances]',
                          '/home/felipe/workspace/mast-rhythm-analysis/Experiment Data/MAST Onsets [References]')