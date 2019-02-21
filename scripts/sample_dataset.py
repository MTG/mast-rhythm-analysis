import shutil, os
import random

def sample_dataset(dataset_path, n_samples, output_folder='sampled'):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        for audio_file in filenames:
            f.append(os.path.join(dirpath, audio_file))
    passed_performances = [audio_file for audio_file in f if 'pass' in audio_file]
    rejected_performances = [audio_file for audio_file in f if 'fail' in audio_file]

    # The sample must have passed and rejected performances on a rate of 1/1
    copy_2_output(random.sample(passed_performances, n_samples/2), os.path.join(dataset_path, output_folder))
    copy_2_output(random.sample(rejected_performances, n_samples/2), os.path.join(dataset_path, output_folder))

def copy_2_output(files_list, output_folder):
    print len(files_list)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for audio_file in files_list:
        shutil.copy(audio_file, output_folder)

if __name__ == "__main__":
    sample_dataset('data/m4a/tmp/MAST Rhythm - Paired Performances', 2, output_folder='/home/felipe/workspace/mast-rhythm-analysis/data/m4a/sampled2')