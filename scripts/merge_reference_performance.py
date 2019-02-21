import os, re
import subprocess
import random

from pydub import AudioSegment

PATTERN = "(\d*)_rhy(\d*)_per(\d*)_(pass|fail).m4a"
PATTERN_REFERENCES = "(\d*)_rhy(\d*)_ref(\d*).m4a"

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

def walk_and_merge(path):
    for dirpath, dnames, fnames in os.walk(path):
        if dirpath == path:
            grouped_performances = _group_performance_by_groupset_and_number(fnames)
            references = random.sample(grouped_performances.keys(), 20)

            for reference in references:
                main_reference = reference[0]

                search_groups = re.search(PATTERN_REFERENCES, main_reference)
                question_set = search_groups.group(1)
                question_number = search_groups.group(2)

                best_reference = REFERENCE_MAPPING[(int(question_set), int(question_number))]

                sampled_performances = random.sample(grouped_performances[reference], 10)

                for sampled_performance in sampled_performances:
                    # Converting m4a to wave files and moving to temporary folder
                    converted_audios = []
                    for audio_file in ["../data/m4a/%s" % best_reference, "../data/m4a/%s" % sampled_performance]:
                        base_name = os.path.splitext(os.path.basename(audio_file))[0]
                        converted_audios.append(m4a_2_wav(audio_file, "../data/m4a/tmp/%s.wav" % base_name))

                    # Creating auxiliar file for FFMPEG concat
                    converted_audios.insert(1, "silence.wav")
                    with open('../data/m4a/tmp/concat_list.txt', 'w') as concat_file:
                        for item in converted_audios:
                            concat_file.write("file '%s'\n" % item)

                    # Run FFMPEG command for concating reference and peformance
                    bash_command = "ffmpeg -f concat -safe 0 -i ../data/m4a/tmp/concat_list.txt -c copy ../data/m4a/tmp/merged/%s" % converted_audios[2]

                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()



        # for rhythmic_performance in fnames:
        #     if re.match(PATTERN, rhythmic_performance):
        #         search_groups = re.search(PATTERN, rhythmic_performance)
        #         question_set = search_groups.group(1)
        #         question_number = search_groups.group(2)
        #         reference_id = search_groups.group(3)

        #         # If there's no reference defined for such (question_set, question_number)
        #         # use the first reference requested and store it as main reference for this
        #         # (question_set, question_number), otherwise use the stored reference no matter
        #         # which reference_id is passed
        #         if not (question_set, question_number) in REFERENCE_MAPPING:
        #             rhythmic_reference = "%s_rhy%s_ref%s.m4a" % (question_set, question_number, reference_id)
        #             REFERENCE_MAPPING[(question_set, question_number)] = rhythmic_reference
        #         else:
        #             print "fetching reference from cache"
        #             rhythmic_reference = REFERENCE_MAPPING[(question_set, question_number)]

        #         # If a reference is available for a specific performance
        #         if os.path.isfile("../data/m4a/%s" % rhythmic_reference):
        #             # Converting m4a to wave files and moving to temporary folder
        #             converted_audios = []
        #             for audio_file in ["../data/m4a/%s" % rhythmic_reference, "../data/m4a/%s" % rhythmic_performance]:
        #                 base_name = os.path.splitext(os.path.basename(audio_file))[0]
        #                 converted_audios.append(m4a_2_wav(audio_file, "../data/m4a/tmp/%s.wav" % base_name))

        #             # Creating auxiliar file for FFMPEG concat
        #             converted_audios.insert(1, "silence.wav")
        #             with open('../data/m4a/tmp/concat_list.txt', 'w') as concat_file:
        #                 for item in converted_audios:
        #                     concat_file.write("file '%s'\n" % item)

        #             # Run FFMPEG command for concating reference and peformance
        #             bash_command = "ffmpeg -f concat -safe 0 -i ../data/m4a/tmp/concat_list.txt -c copy ../data/m4a/tmp/merged/%s" % converted_audios[2]

        #             process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        #             output, error = process.communicate()

        #         # Else, report missing data
        #         else:
        #             with open('../data/m4a/tmp/report_file.txt', 'w') as concat_file:
        #                 concat_file.write("No %s reference available for %s performance\n" % (rhythmic_reference, rhythmic_performance))

def _group_performance_by_groupset_and_number(files):
    grouped = {}
    for rhythmic_performance in files:
        if re.match(PATTERN, rhythmic_performance):
            search_groups = re.search(PATTERN, rhythmic_performance)
            question_set = search_groups.group(1)
            question_number = search_groups.group(2)
            reference_id = search_groups.group(3)

            sorted_references = tuple(_get_sorted_references(files, question_set, question_number))
            grouped[sorted_references] = grouped.get(sorted_references, [])
            grouped[sorted_references].append(rhythmic_performance)

    return grouped


def _get_sorted_references(files, question_set, question_number):
    references = []
    for rhythmic_performance in files:
        if re.match(PATTERN_REFERENCES, rhythmic_performance):
            search_groups = re.search(PATTERN_REFERENCES, rhythmic_performance)
            ref_question_set = search_groups.group(1)
            ref_question_number = search_groups.group(2)

            if ref_question_set == question_set and ref_question_number == question_number:
                references.append(rhythmic_performance)
    references.sort()
    return references



def m4a_2_wav(input, output):
    m4a_version = AudioSegment.from_file(input, "mp4")
    m4a_version.export(output, format="wav")

    return os.path.basename(output)

if __name__ == "__main__":
    walk_and_merge("../data/m4a/")