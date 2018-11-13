#===============================#
# Train.py               #
# Author: Xiaofeng Tang         #
# Mail: xiaofeng419@gmail.com   #
#===============================#

#%%
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve
import pickle

def readJson (json_path):
    # Read Json File by AlphaPose
    json_data=open(json_path)
    json_string = json_data.read()
    j = json.loads(json_string)
    return j

def readData(filepath):
    data = readJson(filepath)
    feature = []
    label = []
    for seq in data:
        keypoints = seq['keypoints']
        feature.append(keypoints)
        l = seq['label']
        if (l == 'c'):
            label.append(1)
        else:
            label.append(-1)
    return feature, label

def validateTrainingResult(clf, ID, pose, train_feature, label, cross_image_path, noncross_image_path, vis = False):
    count = 0
    correct = 0
    wrong = 0

    for i in range(len(ID)):
        tag = ''
        x = []
        y = []
        image_ID = ID[i]
        f_array = np.array(train_feature[i])
        C = label[i]
        single_feature = f_array.reshape(1, -1)
        prediction = clf.predict(single_feature)
        if prediction == C:
            correct += 1
            tag = 'correct'
        else:
            wrong += 1
            tag = 'wrong'

        # Visulize Result

        if (vis):
            for j in range(17):
                x.append (pose[i][2*j + 0])
                y.append (pose[i][2*j + 1])

            fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
            ax = fig.gca()
            if prediction == 1:
                p = 'cross'
            else:
                p = 'non-cross'
            if C == 1:
                img = mpimg.imread(cross_image_path + '/' + image_ID)
                truth = 'cross'
            else:
                img = mpimg.imread(noncross_image_path + '/' + image_ID)
                truth = 'non-cross'

            plt.scatter(x, y, s=25, c='red', marker='o')
            if tag == 'wrong':
                plt.text(x[0], y[0] - 40, "Prediction: " + p + "\n Truth: " + truth, fontsize=25, bbox=dict(facecolor='red', alpha=0.5), horizontalalignment ='center')
            else:
                plt.text(x[0], y[0] - 40, "Prediction: " + p + "\n Truth: " + truth, fontsize=25, bbox=dict(facecolor='green', alpha=0.5), horizontalalignment ='center')

            # Plot Limb
            pairs = [(0,1), (1,3), (0,2), (2,4), (5,6), (5,7), (7,9), (6,8), (8,10), (5,11), (6,12), (11,12), (11,13), (13,15), (12,14), (14,16)]
            for pair in pairs:
                node1_x = pose[i][pair[0] * 2 + 0]
                node1_y = pose[i][pair[0] * 2 + 1]
                node2_x = pose[i][pair[1] * 2 + 0]
                node2_y = pose[i][pair[1] * 2 + 1]
                plt.plot([node1_x, node2_x], [node1_y, node2_y], linewidth=5, alpha=0.7 )


            ax.imshow(img)
            plt.show()
        count += 1
    print( "Score:" + str(float(correct) / (count)) + "Sample Size:" + str(count) )
    return count, float(correct) / (count)


# def plotLossEpochs(clf):
#     old_stdout = sys.stdout
#     sys.stdout = mystdout = StringIO()
#     clf.fit(added_train_feature, train_label)
#
#     sys.stdout = old_stdout
#     loss_history = mystdout.getvalue()
#     loss_list = []
#     for line in loss_history.split('\n'):
#         if(len(line.split("loss: ")) == 1):
#             continue
#         loss_list.append(float(line.split("loss: ")[-1]))
#     plt.figure()
#     plt.plot(np.arange(len(loss_list)), loss_list)
#     plt.yscale('log')
#     plt.xscale('log')
#
#     plt.xlabel("Epochs")
#     plt.title('Loss vs Epochs')
#     plt.ylabel("Loss")
#     plt.savefig("pure_SGD: .png")
#     plt.close()

def plot_learning_curve(estimator, title, X, y, ylim=None, cv = 5, n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

# def normlaizePose(train_feature):
#     norm_train_feature = [0 for i in range(len(train_feature)) ]
#     for i in range(len(train_feature)):
#         x = train_feature[i][0]
#         y = train_feature[i][1]
#         yy = []
#         for k in range(17):
#             yy.append(train_feature[i][k*2 + 1])
#         h = max(yy) - min(yy)
#         norm_train_feature[i] = [0 for i in range(17 * 2)]
#         for j in range(17):
#             norm_train_feature[i][j * 2 + 0] = (train_feature[i][j * 2 + 0] - x) / h
#             norm_train_feature[i][j * 2 + 1] = (train_feature[i][j * 2 + 1] - y) / h
#     return norm_train_feature



def addPoseFeature(train_feature):
    added_train_feature = []
    for keypoints_list in train_feature:
        added_train_feature.append([])

        for keypoints in keypoints_list:
            # add angle between points
            angle_between_nodes = [(5,7), (6,8), (7,9), (8,10), (11,13), (13,15), (12,14), (14,16)]
            added_train_feature[-1].append([])
            for pair in angle_between_nodes:
                node1_x = keypoints[pair[0] * 3 + 0]
                node1_y = keypoints[pair[0] * 3 + 1]
                node2_x = keypoints[pair[1] * 3 + 0]
                node2_y = keypoints[pair[1] * 3 + 1]
                vector = (node2_x - node1_x, node2_y - node1_y)

                dot_product = np.dot(vector, (1,0))
                norm = np.linalg.norm(vector)
                angle = np.arccos(dot_product/norm)
                if np.isnan (angle):
                    angle = 0
                added_train_feature[-1][-1].append(angle)

            angle_between_limbs = [((11,15), (12,16)), ((5,9), (6,10)) ]
            for limb_pair in angle_between_limbs:
                node1_x = keypoints[limb_pair[0][0] * 3 + 0]
                node1_y = keypoints[limb_pair[0][0] * 3 + 1]
                node2_x = keypoints[limb_pair[0][1] * 3 + 0]
                node2_y = keypoints[limb_pair[0][1] * 3 + 1]
                vector1 = (node2_x - node1_x, node2_y - node1_y)

                node3_x = keypoints[limb_pair[1][0] * 2 + 0]
                node3_y = keypoints[limb_pair[1][0] * 2 + 1]
                node4_x = keypoints[limb_pair[1][1] * 2 + 0]
                node4_y = keypoints[limb_pair[1][1] * 2 + 1]
                vector2 = (node4_x - node3_x, node4_y - node3_y)

                dot_product = np.dot(vector1, vector2)
                norm1 = np.linalg.norm(vector1)
                norm2 = np.linalg.norm(vector2)
                angle = np.arccos(dot_product / norm1 / norm2)
                if np.isnan (angle):
                    angle = 0
                added_train_feature[-1][-1].append(angle)
    return added_train_feature

#%%

def serializeFeature(feature):
    result_feature = []
    for seq in feature:
        result_feature.append([])
        for data in seq:
            result_feature[-1].extend(data)
        if len(result_feature[-1]) != 150:
            result_feature.pop(-1)
    return result_feature



def main():
    # input path
    train_set_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/train_set.json"
    test_set_path = "/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/seq_json/test_set.json"
    image_path = '/home/xiaofeng/Documents/cs221/Project/Dataset/Data_by_Matlab/images'


    # read data
    train_feature, train_label = readData(train_set_path)
    test_feature, test_label = readData(test_set_path)

    # normalize data
    #norm_train_feature = normlaizePose(train_feature)
    #norm_test_feature = normlaizePose(test_feature)

    # add Pose Feature
    added_train_feature = addPoseFeature(train_feature)
    added_test_feature = addPoseFeature(test_feature)

    # serialize Feature
    serialized_train_feature = serializeFeature(added_train_feature)
    serialized_test_feature = serializeFeature(added_test_feature)

    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state = 0, verbose = True)
    clf.fit(serialized_train_feature, train_label)
    #coef = clf.coef_[0]
    filename = 'finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))

    #plotLossEpochs(clf)

    plt = plot_learning_curve(clf, 'Learning Curve', serialized_train_feature, train_label, train_sizes=np.linspace(.1, 1, 10))

    plt.show()

    print ("test score is " + str(clf.score(serialized_train_feature, train_label)) )
    print ("train score is " + str(clf.score(serialized_test_feature, test_label)) )
    #sample_total, accuracy = validateTrainingResult(clf, test_ID, pose_test_feature, added_test_feature, test_label, cross_image_path, noncross_image_path, vis = False)


if __name__== "__main__":
    main()

