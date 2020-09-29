import json
import os
import yaml

with open('config/base_caricature.yaml', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    score_structure = config['score_types']
    cmp_methods = config['cmp_methods']
    study_group_num = config['study_group_num']

# cycleGAN_shape_score = 0
# MUNIT_shape_score = 0
# cariGAN_shape_score = 0
# warpGAN_shape_score = 0
# MWGAN_shape_score = 0
#
# cycleGAN_visual_score = 0
# MUNIT_visual_score = 0
# cariGAN_visual_score = 0
# warpGAN_visual_score = 0
# MWGAN_visual_score = 0

# score_matrix = [[0] * len(score_structure) for i in range(len(cmp_methods))]
# print(score_matrix)
score_shape = {'cycleGAN': 0, 'MUNIT': 0, 'cariGANs': 0, 'warpGAN': 0, 'MWGAN': 0 }
score_visual = {'cycleGAN': 0, 'MUNIT': 0, 'cariGANs': 0, 'warpGAN': 0, 'MWGAN': 0 }
score_filenames = os.listdir('scores')
user_num = len(score_filenames)
print(user_num)
if not user_num:
    raise Exception('Empty score files to be calculation.')
for filename in score_filenames:
    with open(os.path.join('scores', filename)) as f:
        score = json.load(f)
        print(len(score))
        for s in score:

            score_visual[s['general_best'].split('.')[0]] += 1;
            score_visual[s['general_worst'].split('.')[0]] -= 1;
            score_shape[s['warp_best'].split('.')[0]] += 1;
            score_shape[s['warp_worst'].split('.')[0]] -= 1;

                # for s_id, score_item in enumerate(score_structure):
                    # print(s_id, score_item)
                    # if s['content'].endswith(method):
                    #     score_matrix[m_id][s_id] += s[score_item['score_type']]
print(score_shape)
print(score_visual)