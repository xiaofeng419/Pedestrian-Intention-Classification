#===============================#
# ReadPoseData.py               #
# Author: Xiaofeng Tang         #
# Mail: xiaofeng419@gmail.com   #
#===============================#

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import random
import os

def readJson (json_path):
    # Read Json File by AlphaPose
    json_data=open(json_path)
    json_string = json_data.read()
    j = json.loads(json_string)
    return j

# From https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

def readBoundingBox (frame):
    # Read BBox by Matlab

    img_id = frame[0]
    bbox_x = int(frame[1])
    bbox_y = int(frame[2])
    bbox_w = int(frame[3])
    bbox_h = int(frame[4])
    bbox = [bbox_x, bbox_y, bbox_x + bbox_w, bbox_y + bbox_h]
    return img_id, bbox

def readPoseBox (keypoints):
    '''
        Result (17 body parts)
            {0,  "Nose"},
            {1,  "LEye"},
            {2,  "REye"},
                    {3,  "LEar"},
                    {4,  "REar"},
                    {5,  "LShoulder"},
                    {6,  "RShoulder"},
                    {7,  "LElbow"},
                    {8,  "RElbow"},
                    {9,  "LWrist"},
                    {10, "RWrist"},
                    {11, "LHip"},
                    {12, "RHip"},
                    {13, "LKnee"},
                    {14, "Rknee"},
                    {15, "LAnkle"},
                    {16, "RAnkle"},
    '''
    # x, y are the vectors of body parts locations, confi is the vector of the confidence
    x = []
    y = []
    confi = []

    # Extract 17 points for each pedestrian
    right_x = 0
    left_x = 99999
    top_y = 0
    bottom_y = 99999
    for i in range(17):
        x.append(keypoints[i * 3 + 0])
        y.append(keypoints[i * 3 + 1])
        confi.append(keypoints[i * 3 + 2])
        if confi[-1] > 0.45:
            # get pose box
            if x[-1] > right_x:
                right_x = x[-1]
            if x[-1] < left_x:
                left_x = x[-1]
            if y[-1] > top_y:
                top_y = y[-1]
            if y[-1] < bottom_y:
                bottom_y = y[-1]

            # Visualize Json result
            #plt.scatter(x, y, s=2, c='red', marker='o')
    w = right_x - left_x
    # Get Pose Box
    pbox = [0, 0, 0, 0]
    pbox[0] = left_x - 0.2 * w
    pbox[1] = bottom_y
    pbox[2] = right_x + 0.2 * w
    pbox[3] = top_y
    return x, y, confi, pbox

def write_pose_cross_data(pose_database, annotation_seq, image_path, output_path, cross, vis = False):
    result = []

    for seq in annotation_seq:
        seq_bad_flag = False
        vid_id = seq['video_id']
        content = seq['content']
        frame_data = {'video_id': vid_id}
        frame_data['img_id'] = []
        if cross:
            frame_data['label'] = 'c'
        else:
            frame_data['label'] = 'nc'
        for frame in content:
            img_id, bbox = readBoundingBox(frame)
            frame_data['img_id'].append(img_id)
            if img_id not in pose_database[vid_id]:
                seq_bad_flag = True
                break
            poses = pose_database[vid_id][img_id]

            max_iou = 0
            for entry in poses:
                score = entry['score']
                if score < 1.0:
                    continue
                x, y, confi, pbox = readPoseBox(entry['keypoints'])
                iou = bb_intersection_over_union(pbox, bbox)
                #If iou is not 0
                if (iou > max_iou):
                    max_iou = iou
                    result_keypoints = entry['keypoints']
                    result_pbox = pbox

            # no pose found for this frame. Seq is bad. Go to next seq
            if max_iou == 0:
                seq_bad_flag = True
                break

            if 'keypoints' not in frame_data:
                frame_data['keypoints'] = []
            frame_data['keypoints'].append(result_keypoints)

            # Get Road info
            # L_ankle_x = result_keypoints[15 * 3]
            # L_ankle_y = result_keypoints[15 * 3 + 1]
            # R_ankle_x = result_keypoints[16 * 3]
            # R_ankle_y = result_keypoints[16 * 3 + 1]
            # nose_y = result_keypoints[1]
            # road_box[0] =
            # road_box[1] =
            # road_box[2] =
            # road_box[3] =

            if (vis):
                # Show original image at 19020 * 1080
                img = mpimg.imread(image_path + vid_id + '/' + img_id)
                fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
                ax = fig.gca()
                ax.imshow(img)
                rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                rect = patches.Rectangle((result_pbox[0], result_pbox[1]), result_pbox[2] - result_pbox[0], result_pbox[3] - result_pbox[1], linewidth=1, edgecolor='g', facecolor='none')
                ax.add_patch(rect)
                plt.show()
                plt.close()

        if (seq_bad_flag): continue
        result.append(frame_data)

    if cross == True:
        tag = 'cross'
    else:
        tag = 'non-cross'
    outFilePath = output_path +  'annotated_seq_' + tag + '.json'
    with open(outFilePath, 'w') as outfile:
        json.dump(result, outfile)


def generateTrainTestDataSet(cross_data, non_cross_data, output_data_path):
    train_set = []
    test_set = []

    while True:
        x = random.random()
        if x < 0.5:
            if len(cross_data) == 0:
                break
            data = cross_data.pop(0)
        else:
            if len(non_cross_data) == 0:
                break
            data = non_cross_data.pop(0)
        vid_id = data['video_id']
        tokens = vid_id.split('_')
        vnum = int(tokens[1])
        if vnum < 280:
            train_set.append(data)
        else:
            test_set.append(data)

    outFilePath = output_data_path + 'train_set.json'
    with open(outFilePath, 'w') as outfile:
        json.dump(train_set, outfile)
    outFilePath = output_data_path + 'test_set.json'
    with open(outFilePath, 'w') as outfile:
        json.dump(test_set, outfile)

def main():
    pose_json_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/consolidated_alpha_pose.json"
    c_annotation_json_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/annotation_seq_bbox_c.json"
    nc_annotation_json_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/annotation_seq_bbox_nc.json"
    output_data_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/"
    image_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/images/'


    c_annotation_seq = readJson(c_annotation_json_path)
    nc_annotation_json_path = readJson(nc_annotation_json_path)
    pose_database = readJson(pose_json_path)

    write_pose_cross_data(pose_database, c_annotation_seq, image_path, output_data_path, cross = True, vis = False)
    write_pose_cross_data(pose_database, nc_annotation_json_path, image_path, output_data_path, cross = False, vis = False)

    # Generate train and test set
    cross_data = readJson(output_data_path + 'annotated_seq_cross.json')
    non_cross_data = readJson(output_data_path + 'annotated_seq_non-cross.json')
    generateTrainTestDataSet(cross_data, non_cross_data, output_data_path)


#%%

if __name__== "__main__":
  main()



#%%


#%%