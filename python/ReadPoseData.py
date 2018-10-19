#===============================#
# ReadPoseData.py               #
# Author: Xiaofeng Tang         #
# Mail: xiaofeng419@gmail.com   #
#===============================#

import json
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Read Json File by AlphaPose
json_data=open("/home/xiaofeng/Documents/Alphapose_pytorch/AlphaPose/examples/res/alphapose-results.json")
json_string = json_data.read()
j = json.loads(json_string )

# Show original image at 19020 * 1080
img = mpimg.imread('/home/xiaofeng/Documents/cs221/Project/Dataset/JAAD/videos/try/I00061.png')
plt.figure(figsize=(19.2, 10.8), dpi=100)
imgplot = plt.imshow(img)

# x, y are the vectors of body parts locations, confi is the vector of the confidence
x = []
y = []
confi = []

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

for data_j in j:
    for i in range(17):
        x.append(data_j["keypoints"][i*3 + 0])
        y.append(data_j["keypoints"][i * 3 + 1])
        confi.append(data_j["keypoints"][i * 3 + 2])

        if confi[-1] > 0.5:
            # Visualize Json result
            plt.scatter(x, y, s=2, c='red', marker='o')
plt.show()


