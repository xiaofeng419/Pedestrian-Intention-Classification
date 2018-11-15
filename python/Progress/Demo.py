import pickle
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
import os
import Train
import ReadPoseData


def sortImage(img_id):

    num = int(img_id[1:6])
    return num

previous_image_ID = None
feature = []

pose_json_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/consolidated_alpha_pose.json"
image_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Demo/165/vis/'
image_output_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Demo/165/prediction/'
vid_id = 'video_0165'
trained_weights = 'finalized_model.sav'
seq_length = 15
missing_frame_thrsd = 5

pose_database = Train.readJson(pose_json_path)
pose_database = pose_database[vid_id]

clf = pickle.load(open(trained_weights, 'rb'))
#                      |- [anglefeature] 10x
#                   |- +
# tracked_pose_list +  |- [anglefeature] 10x
tracked_pose_list = []

#
#                   |- [pbox] 1~15x
# tracked_pose_list +
tracked_pose_pboxes = []

image_names = os.listdir(image_path)
image_names = sorted(image_names, key = sortImage)
pose_pboxes_del_dict = {}

count = 0
for image_name in image_names:
    if count > -1:
        img = mpimg.imread(image_path + image_name)
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100, frameon=False)

        ag = plt.Axes(fig, [0., 0., 1., 1.])
        ag.set_axis_off()
        fig.add_axes(ag)
        ag.imshow(img)

        if image_name in pose_database:
            poses = pose_database[image_name]
            if (image_name == 'I00093.png'):
                a = 1

            for i in range(len(tracked_pose_pboxes)):
                best_pbox = None
                best_keypoints = None
                best_pose = None
                max_iou = 0
                for pose in poses:
                    keypoints = pose['keypoints']
                    x, y, confi, pbox = ReadPoseData.readPoseBox(keypoints)
                    # if (pbox[3] - pbox[1]) < 20 or pose['score'] < 0.1:
                    #     continue

                    iou = ReadPoseData.bb_intersection_over_union(pbox, tracked_pose_pboxes[i])
                    if iou > 0.01 and iou > max_iou:
                        max_iou = iou
                        best_pbox = pbox
                        best_keypoints = keypoints
                        best_pose = pose

                # if found a matching pbox from current image
                # update tracked_pose_pboxes[i] and tracked_pose_list[i]
                if max_iou > 0:
                    poses.remove(best_pose)
                    tracked_pose_pboxes[i] = best_pbox
                    added_feature = Train.addPoseFeature([[best_keypoints]])
                    converted_feature = added_feature[0][0]
                    tracked_pose_list[i].append(converted_feature)

                    # clear index in  pose_pboxes_del_dict
                    pose_pboxes_del_dict[i] = 0

                    if len(tracked_pose_list[i]) > seq_length:
                        del tracked_pose_list[i][0]

                # if not found a matching pbox from current image
                # delete tracked_pose_pboxes[i] and tracked_pose_list[i]
                else:
                    if i in pose_pboxes_del_dict:
                        pose_pboxes_del_dict[i] += 1
                    else:
                        pose_pboxes_del_dict[i] = 1

            # delete non-tracked poses
            deleteIndex = []
            for key, item in pose_pboxes_del_dict.items():
                if item == missing_frame_thrsd:
                    deleteIndex.append(key)
                    pose_pboxes_del_dict[key] = 0
            tracked_pose_pboxes = [i for j, i in enumerate(tracked_pose_pboxes) if j not in deleteIndex]
            tracked_pose_list = [i for j, i in enumerate(tracked_pose_list) if j not in deleteIndex]


            # There are still unmatched poses. Create new list
            for pose in poses:
                keypoints = pose['keypoints']
                x, y, confi, pbox = ReadPoseData.readPoseBox(keypoints)
                if (pbox[3] - pbox[1]) < 30 or pose['score'] < 0.5:
                    continue
                tracked_pose_pboxes.append(pbox)
                added_feature = Train.addPoseFeature([[keypoints]])
                converted_feature = added_feature[0][0]
                tracked_pose_list.append([converted_feature])

            for i in range(len(tracked_pose_list)):

                if len(tracked_pose_list[i]) == seq_length:
                    serialized_train_feature = Train.serializeFeature([tracked_pose_list[i]])
                    prediction = clf.predict(serialized_train_feature)
                    if prediction == 1:
                        p = 'C'
                        plt.text(tracked_pose_pboxes[i][0] + 10, tracked_pose_pboxes[i][1] - 40,  p, fontsize=25, bbox=dict(facecolor='green', alpha=0.5), horizontalalignment='center')
                    else:
                        p = 'NC'
                        plt.text(tracked_pose_pboxes[i][0] + 10, tracked_pose_pboxes[i][1] - 40,  p, fontsize=25, bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')

            #plt.show()
            plt.savefig(image_output_path + '/' + image_name, bbox_inches='tight')
            if count > 123:
                a = 1
            print (image_name)
            plt.close()
    count += 1






# for i in range(len(j)):
#     # Enough confidence for pedestrian
#     j_image = j[i]
#     image_ID = j_image['image_id']
#     if image_ID == previous_image_ID:
#         new_image = False
#     else:
#         new_image = True
#
#         #plt.show()
#         plt.savefig(image_output_path + '/'  + image_ID, bbox_inches='tight' )
#         plt.close()
#
#         img = mpimg.imread(image_path + '/' + image_ID)
#         fig = plt.figure(figsize=(19.2, 10.8), dpi=100, frameon=False)
#
#         #ax = fig.gca()
#         ag = plt.Axes(fig, [0., 0., 1., 1.])
#         ag.set_axis_off()
#         fig.add_axes(ag)
#
#         ag.imshow(img)
#         feature = []
#
#     previous_image_ID = image_ID
#     if j_image['score'] > 1.2:
#         x, y, confi, pbox = ReadPoseData.readPoseBox(j_image)
#         feature = []
#         for i in range(17):
#             feature.append(x[i])
#             feature.append(y[i])
#
#         added_feature = addPoseFeature_s(feature)
#         f_array = np.array(added_feature)
#         single_feature = f_array.reshape(1, -1)
#         prediction = clf.predict(single_feature)
#
#         #plt.scatter(x, y, s=25, c='red', marker='o')
#         if prediction == 1:
#             p = 'C'
#
#             plt.text(x[0], y[0] - 40,  p, fontsize=25, bbox=dict(facecolor='green', alpha=0.5), horizontalalignment='center')
#         else:
#             p = 'NC'
#             plt.text(x[0], y[0] - 40,  p, fontsize=25, bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')
#
#         # Plot Limb
#
#
#


#result = loaded_model.score(X_test, Y_test)



