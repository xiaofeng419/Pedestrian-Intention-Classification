#===============================#
# ReadPoseData.py               #
# Author: Xiaofeng Tang         #
# Mail: xiaofeng419@gmail.com   #
#===============================#

import os
import json

def readJson (json_path):
    # Read Json File by AlphaPose
    json_data=open(json_path)
    json_string = json_data.read()
    j = json.loads(json_string)
    return j

pose_json_folders_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/pose_jsons"
newpose_json_out_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json"

newpose = {}

for videofolder in os.listdir(pose_json_folders_path):

    pose_json_path = pose_json_folders_path + '/' + videofolder + '/alphapose-results.json'
    pose = readJson(pose_json_path)
    newpose[videofolder] = {}

    #                                   |- 'score': 2, 'keypoints': []
    #                      |-I00001.png +
    #          |-video_001:+            |- 'score': ...
    # newpose: +           |-I00002.png...
    #          |-video_002 ...

    for data in pose:
        image_id = data['image_id']
        keypoints = data['keypoints']

        if image_id not in newpose[videofolder]:
            newpose[videofolder][image_id] = []
        newpose[videofolder][image_id].append({'score': data['score'], 'keypoints': data['keypoints']} )


outFilePath = newpose_json_out_path + '/' + 'consolidated_alpha_pose.json'
with open(outFilePath, 'w') as outfile:
    json.dump(newpose, outfile)