import json
import numpy as np
from sklearn import linear_model

def readJson (json_path):
    # Read Json File by AlphaPose
    json_data=open(json_path)
    json_string = json_data.read()
    j = json.loads(json_string)
    return j

def readData(filepath, feature =[], label = [],  maxiter = 99999):
    j = readJson(filepath)
    count = len(feature)

    for key, value in j.items():
        data = value.split(',')
        feature.append([])

        for i in range(17):
            x = float(data[3 * i + 0])
            y = float(data[3 * i + 1])
            confi = data[3 * i + 2]
            feature[count].append(x)
            feature[count].append(y)
        l = data[-1]
        if (l == 'cross'):
            label.append(1)
        else:
            label.append(-1)
        count += 1
        if count > maxiter:
            break
    return feature, label


train_cross_json_path = "../../Dataset/Data_by_Matlab/cross_pose_data/cross_train_data.json"
train_noncross_json_path = "../../Dataset/Data_by_Matlab/non-cross_pose_data/non-cross_train_data.json"
test_cross_json_path = "../../Dataset/Data_by_Matlab/cross_pose_data/cross_test_data.json"
test_noncross_json_path = "../../Dataset/Data_by_Matlab/non-cross_pose_data/non-cross_test_data.json"



train_feature, train_label = readData(train_noncross_json_path, [], [], maxiter  = 8000)
train_feature, train_label = readData(train_cross_json_path, train_feature, train_label, maxiter = 8000)

test_feature, test_label = readData(test_noncross_json_path, [], [], maxiter  = 2000)
test_feature, test_label = readData(test_cross_json_path, test_feature, test_label,  maxiter = 2000)

clf = linear_model.SGDClassifier(max_iter=300000, verbose = True)
clf.fit(train_feature, train_label)

print ("score is" + str(clf.score(test_feature, test_label)) )

