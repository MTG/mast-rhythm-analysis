import os
import re

from shutil import copy
from pydub import AudioSegment

REFERENCE_MAPPING = {
    (63,2): '63_rhy2_ref1176742.m4a',
    (53,1): '53_rhy1_ref187859.m4a',
    (67,1): '67_rhy1_ref1597742.m4a',
    (61,1): '61_rhy1_ref1342752.m4a',
    (61,2): '61_rhy2_ref1457742.m4a',
    (57,2): '57_rhy2_ref161959.m4a',
    (55,1): '55_rhy1_ref127859.m4a',
    (65,1): '65_rhy1_ref1328742.m4a',
    (58,1): '58_rhy1_ref104359.m4a',
    (67,2): '67_rhy2_ref1043752.m4a',
    (59,2): '59_rhy2_ref123759.m4a',
    (69,1): '69_rhy1_ref1126742.m4a',
    (64,2): '64_rhy2_ref1453742.m4a',
    (66,2): '66_rhy2_ref1397752.m4a',
    (56,2): '56_rhy2_ref104160.m4a',
    (55,2): '55_rhy2_ref162559.m4a',
    (59,1): '59_rhy1_ref113695.m4a',
    (69,2): '69_rhy2_ref1154742.m4a',
    (610,1): '610_rhy1_ref2915742.m4a',
    (63,1): '63_rhy1_ref2304742.m4a',
    (510,1): '510_rhy1_ref104558.m4a',
    (65,2): '65_rhy2_ref2392742.m4a',
    (68,2): '68_rhy2_ref1540742.m4a',
    (510,2): '510_rhy2_ref109558.m4a',
    (53,2): '53_rhy2_ref135059.m4a',
    (54,1): '54_rhy1_ref113160.m4a',
    (62,2): '62_rhy2_ref1329742.m4a',
    (51,2): '51_rhy2_ref126659.m4a',
    (52,2): '52_rhy2_ref120659.m4a',
    (68,1): '68_rhy1_ref1540742.m4a',
    (62,1): '62_rhy1_ref1155742.m4a',
    (52,1): '52_rhy1_ref147659.m4a',
    (64,1): '64_rhy1_ref1199732.m4a',
    (56,1): '56_rhy1_ref296559.m4a',
    (54,2): '54_rhy2_ref128758.m4a',
    (58,2): '58_rhy2_ref175685.m4a',
    (66,1): '66_rhy1_ref1325752.m4a',
    (610,2): '610_rhy2_ref2229742.m4a',
    (51,1): '51_rhy1_ref129959.m4a',
    (57,1): '57_rhy1_ref205558.m4a',
}

PATTERN = "(\d*)_rhy(\d*)_per(\d*)_(pass|fail).wav"

def m4a_2_wav(input, output):
    m4a_version = AudioSegment.from_file(input, "mp4")
    m4a_version.export(output, format="wav")

    return os.path.basename(output)

if __name__ == "__main__":
    passed_performances = []
    rejected_performances = []
    for (dirpath, dirnames, filenames) in os.walk('../data/Merged Performances - 80 Samples - Pattern Balanced/'):
        for filename in filenames:
            if 'pass' in filename:
                passed_performances.append(filename)
            elif 'fail' in filename:
                rejected_performances.append(filename)
    with open('listperformances','w') as listperformances:
        with open('listreferences','w') as listreferences:
            # accepted performances
            for performance in passed_performances:
                listperformances.write('%s\n' % performance)
                m4a_2_wav('../data/Full Dataset/%s.m4a' % performance.split(".")[0], '../data/Only Performances/%s' % performance)

                search_groups = re.search(PATTERN, performance)
                question_set = search_groups.group(1)
                question_number = search_groups.group(2)

                best_reference = REFERENCE_MAPPING[(int(question_set), int(question_number))]
                listreferences.write('%s.wav\n' % best_reference.split(".")[0])

                m4a_2_wav('../data/Full Dataset/%s.m4a' % best_reference.split(".")[0], '../data/Only References/%s.wav' % best_reference.split(".")[0])

            # rejected peformances
            for performance in rejected_performances:
                listperformances.write('%s\n' % performance)
                m4a_2_wav('../data/Full Dataset/%s.m4a' % performance.split(".")[0], '../data/Only Performances/%s' % performance)

                search_groups = re.search(PATTERN, performance)
                question_set = search_groups.group(1)
                question_number = search_groups.group(2)

                best_reference = REFERENCE_MAPPING[(int(question_set), int(question_number))]
                listreferences.write('%s.wav\n' % best_reference.split(".")[0])

                m4a_2_wav('../data/Full Dataset/%s.m4a' % best_reference.split(".")[0], '../data/Only References/%s.wav' % best_reference.split(".")[0])