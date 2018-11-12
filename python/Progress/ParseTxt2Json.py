#===============================#
# ReadPoseData.py               #
# Author: Xiaofeng Tang         #
# Mail: xiaofeng419@gmail.com   #
#===============================#

import json
import os

cross_in_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/cross'
non_cross_in_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/non-cross'
out_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json'


dirs = {'c':cross_in_path, 'nc':non_cross_in_path}

for label , path in dirs.items():
    result = []
    for filename in os.listdir(path):

        tokens = filename.split('_')
        vnum = tokens[1]

        file = open(path + "/" + filename, 'r')
        info =  (file.readlines()[1:])
        if len(info) < 15:
            file.close()
            continue

        seq = {}
        video_id = 'video_' + vnum

        seq["video_id"] = video_id
        content = []
        skip_flag = False
        for frame_info_str in info:
            frame_info = frame_info_str.split(',')
            frame_num = frame_info[0]
            x = frame_info[1]
            y = frame_info[2]
            w = frame_info[3]
            h = frame_info[4]
            if int(h) < 100:
                skip_flag = True
                file.close()
                continue
            image_id = 'I' + str(frame_num).zfill(5) + '.png'
            content.append((image_id, x, y, w, h))
        if not skip_flag:
            seq['content'] = content
            result.append(seq)
        file.close()

    outFilePath = out_path + '/' +  'annotation_seq_bbox_' + label +'.json'
    with open(outFilePath, 'w') as outfile:
        json.dump(result, outfile)

def readJson (json_path):
    # Read Json File by AlphaPose
    json_data=open(json_path)
    json_string = json_data.read()
    j = json.loads(json_string)
    return j

#j = readJson('/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json' + '/annotation_seq.json')
#a  = 1