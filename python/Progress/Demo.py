import Train
import pickle
import json
import ReadPoseData
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np

Demo_json_path = "../../Dataset/Demo/095/alphapose-results.json"
image_path = '../../Dataset/Demo/095/vis'
image_output_path = '../../Dataset/Demo/095/prediction'
filename = 'finalized_model.sav'

j = ReadPoseData.readJson(Demo_json_path)
clf = pickle.load(open(filename, 'rb'))

def addPoseFeature_s(train_feature):
    added_train_feature = [ ]

    angle_between_nodes = [(5,7), (6,8), (7,9), (8,10), (11,13), (13,15), (12,14), (14,16)]

    for pair in angle_between_nodes:
        node1_x = train_feature[pair[0] * 2 + 0]
        node1_y = train_feature[pair[0] * 2 + 1]
        node2_x = train_feature[pair[1] * 2 + 0]
        node2_y = train_feature[pair[1] * 2 + 1]
        vector = (node2_x - node1_x, node2_y - node1_y)

        dot_product = np.dot(vector, (1,0))
        norm = np.linalg.norm(vector)
        angle = np.arccos(dot_product/norm)
        if np.isnan (angle):
            angle = 0
        added_train_feature.append(angle)

    angle_between_limbs = [((11,15), (12,16)), ((5,9), (6,10)) ]
    for limb_pair in angle_between_limbs:
        node1_x = train_feature[limb_pair[0][0] * 2 + 0]
        node1_y = train_feature[limb_pair[0][0] * 2 + 1]
        node2_x = train_feature[limb_pair[0][1] * 2 + 0]
        node2_y = train_feature[limb_pair[0][1] * 2 + 1]
        vector1 = (node2_x - node1_x, node2_y - node1_y)

        node3_x = train_feature[limb_pair[1][0] * 2 + 0]
        node3_y = train_feature[limb_pair[1][0] * 2 + 1]
        node4_x = train_feature[limb_pair[1][1] * 2 + 0]
        node4_y = train_feature[limb_pair[1][1] * 2 + 1]
        vector2 = (node4_x - node3_x, node4_y - node3_y)

        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        angle = np.arccos(dot_product / norm1 / norm2)
        if np.isnan (angle):
            angle = 0
        added_train_feature.append(angle)
    return added_train_feature


def sortImage(j_image):
    image_ID = j_image['image_id']
    num = int(image_ID[1:6])
    return num

previous_image_ID = None
feature = []
j = sorted(j, key = sortImage)
for i in range(len(j)):
    # Enough confidence for pedestrian
    j_image = j[i]
    image_ID = j_image['image_id']
    if image_ID == previous_image_ID:
        new_image = False
    else:
        new_image = True

        #plt.show()
        plt.savefig(image_output_path + '/'  + image_ID, bbox_inches='tight' )
        plt.close()

        img = mpimg.imread(image_path + '/' + image_ID)
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100, frameon=False)

        #ax = fig.gca()
        ag = plt.Axes(fig, [0., 0., 1., 1.])
        ag.set_axis_off()
        fig.add_axes(ag)

        ag.imshow(img)
        feature = []

    previous_image_ID = image_ID
    if j_image['score'] > 1.2:
        x, y, confi, pbox = ReadPoseData.readPoseBox(j_image)
        feature = []
        for i in range(17):
            feature.append(x[i])
            feature.append(y[i])

        added_feature = addPoseFeature_s(feature)
        f_array = np.array(added_feature)
        single_feature = f_array.reshape(1, -1)
        prediction = clf.predict(single_feature)

        #plt.scatter(x, y, s=25, c='red', marker='o')
        if prediction == 1:
            p = 'C'

            plt.text(x[0], y[0] - 40,  p, fontsize=25, bbox=dict(facecolor='green', alpha=0.5), horizontalalignment='center')
        else:
            p = 'NC'
            plt.text(x[0], y[0] - 40,  p, fontsize=25, bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')

        # Plot Limb





#result = loaded_model.score(X_test, Y_test)



