#===============================#
# ReadPoseData.py               #
# Author: Xiaofeng Tang         #
# Mail: xiaofeng419@gmail.com   #
#===============================#

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg


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

def write_pose_cross_data(j, bbox_path, image_path, vis):
    for j_image in j:

        # Enough confidence for pedestrian
        if j_image['score'] > 1.2:

            image_ID = j_image['image_id']

            # Read BBox by Matlab
            tokens = image_ID.split('_')
            vid = tokens[0]
            vnum = tokens[1]
            pid = tokens[2]
            pnum = 'B' + tokens[3][1:-4]
            txtFileName = vid + '_' + vnum + '_' + pid + '_' + pnum + '.txt'
            txtFilePath = bbox_path + txtFileName
            file1 = open(txtFilePath, "r")
            bbox = file1.readlines()[0].split(',')[1:5]
            file1.close()

            # Show original image at 19020 * 1080
            img = mpimg.imread(image_path + image_ID)
            fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
            ax = fig.gca()
            ax.imshow(img)

            bbox_x = int(bbox[0])
            bbox_y = int(bbox[1])
            bbox_w = int(bbox[2])
            bbox_h = int(bbox[3])
            bbox = [bbox_x, bbox_y, bbox_x + bbox_w, bbox_y + bbox_h]
            rect = patches.Rectangle((bbox_x, bbox_y), bbox_w, bbox_h, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

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

                x.append(j_image["keypoints"][i * 3 + 0])
                y.append(j_image["keypoints"][i * 3 + 1])
                confi.append(j_image["keypoints"][i * 3 + 2])

                if confi[-1] > 0.45:
                    # get pose box
                    if x[-1] > right_x:
                        right_x = x[-1]
                    if x[-1] < left_x:
                        left_x = x[-1]
                    if y[-1] > top_y:
                        top_y = y[-1]
                    if x[-1] < bottom_y:
                        bottom_y = y[-1]

                    # Visualize Json result
                    plt.scatter(x, y, s=2, c='red', marker='o')

            # Get Pose Box
            pbox_x = left_x
            pbox_y = bottom_y
            pbox_w = right_x - left_x
            pbox_h = top_y - bottom_y
            pbox = [pbox_x, pbox_y, pbox_x + pbox_w, pbox_y + pbox_h]

            # Calculate Intersection area with bbox

            # bbox left edge is inside pbox
            iou = bb_intersection_over_union(pbox, bbox)

            plt.show()
            plt.close()


json_path = "../../Dataset/Data_by_Matlab/cross_pose_json/alphapose-results.json"
bbox_path = '../../Dataset/Data_by_Matlab/cross/bbox/'
image_path = '../../Dataset/Data_by_Matlab/cross/image/'

# Read Json File by AlphaPose
json_data=open(json_path)
json_string = json_data.read()
j = json.loads(json_string)

write_pose_cross_data(j, bbox_path, image_path, vis)

