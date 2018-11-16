# Pedestrian Crossing Classifier


### Dataset
We used JAAD [2] in our project. JAAD provides tags for a specific pedestrian of his/her behaviors during several time slices. We obtain “Non-Crossing” sequence as follows: a non-crossing tagged pedestrian in JAAD [2] has other behaviors such as wondering around the curbs, looking at the traffics, waiting the buses etc. Each of these behaviors also has a frame range and associated bounding boxes in JAAD. Similarly, we split each frame range of these behaviors in order in step 15 and tag all the obtained frame segments being “Non-Crossing”. Finally, we get 1860 “Non-Crossing” sequences.  

### Feature Extraction 
For a single frame, we have two kinds of features: human pose and environment signals. We use the state-of-art algorithm AlphaPose [3] to extract human pose, it can provide (x, y) coordinates for 16 joints with prediction confidence. As illustrated in Fig.1, the 16 joints include nose, eyes, knees and ankles, etc.  Based on our task, we focus on joints which highly relevant to postures and movement in  based on Yolocrossing and non-crossing behaviors. We identify the relative angles between parts of limbs and the ground are most critical for C/NC behaviors. Therefore, we extract the angles between the ground and the forearms, the upper arms, the tights and the calves. In addition, the angles between tight and calf of each leg are particular informative as they codes the human’s moving status. Please see the right part of Fig.1 to see the highlighted parts of limbs which we use to compute these 10 angles. For each frame we obtain a 10 dimensions feature, thus a sequence with 15 frames is associated a big-feature with 15×10=150 dimensions.
<p align="center">
  <img  src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/aaa.png"><br>
  <b>Fig.1. Human Pose Extraction</b><br>
</p>
                                            
Our second kind of feature is the environment signals, although it is still under developing at present, we shall integrate it soon. (Fig.2, PSPNET) 
<p align="center">
  <img src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/Feature.png">
</p>
Fig.2. Road Segmentation

### Random Forest 
We use the random forest module provided by scikit-learn library. We set hyper parameters to use 100 decision trees and tree-depth up to 6. Our training sequences are extracted from the first 280 videos of JAAD [2] while testing sequences from the last 66 ones. Although we obtain an unbalance “Crossing vs Non-Crossing” (5125 vs 1860) sample set, we try to make our training/testing sets to be balance. Finally, our training set contains 1699 samples while testing set 444 samples. Please refer experiment part for the performance of our random forest model.

### Experiment 
In this section, we illustrate the experiment of our random forestmodel. Fig.3 and Fig.4 Illustrates the result of the classification on video. Fig.5 give the learning curve of our random forest model, note the validation accuracy of our model on sequential data reach 88%. It is the best accuracy reported in [1]. Check Fig.6 and Fig.7 below to see our random forest model making correct predictions for both C/NC sequences respectively. Please check [4], [5] for our demo. 

<p align="center">
  <img  src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/bbb.png">
  <img  src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/bbb.png"><br>
  <b>Fig.1. Human Pose Extraction</b><br>
</p>
<p align="center">
  <img  src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/learning_curve.png"><br>
  <b>Fig.5. Human Pose Extraction</b><br>
</p>
<p align="center">
  <img  src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/cross_seq.png"><br>
  <b>Fig.6. Ground True: Crossing; Prediction: Crossing</b><br>
</p>
<p align="center">
  <img  src="https://github.com/xiaofeng419/Pedestrian-Intention-Classification/blob/master/standing_seq.png"><br>
  <b>Fig.7. Ground True: Non-Crossing; Prediction: Non-Crossing</b><br>
</p>




### Reference 
[1]. Zhijie Fang and A.M.Lopez, “Is the Pedestrian going to Cross Answering by 2D Pose Estimation” in IV, 2018. 
[2]. I. Kotseruba, A. Rasouli, J. K. Tsotsos. "Joint Attention in Autonomous Driving (JAAD)."arXiv preprint arXiv:1609.04741 (2016). 
[3]. Fang H, Xie S, Tai Y W, et al. Rmpe: Regional multi-person pose estimation[C]//The IEEE International Conference on Computer Vision (ICCV). 2017, 2. 
[4]. https://slack-files.com/TDDA4RLBW-FE59N4LMC-85708314f9
[5]. https://slack-files.com/TDDA4RLBW-FE39JCA0H-ed2d235da3 



img[src*='#center'] { 
    display: block;
    margin: auto;
}


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
