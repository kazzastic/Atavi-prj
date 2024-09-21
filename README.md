# Atavi-prj

This is an application consisting of three parts, 
1. Training (ultralytics and YOLOv10)
2. Backend (FastAPI)
3. Frontend (Vue.js)

## Training 

In order to train this model, I have used the framework called ultralytics, in order to run the training pipeline, we first need to configure the dataset in a particular file structure, this detail regarding the pipeline configuration and the structuring of dataset in a particular folders is in the `backend/train` in a notebook. 

 Something notable here would be the pre-trained weights, in order to train this model, I have used YOLOv10s which is one of the 5 or 6 pre-trained weights which could be found online on YOLO original github repository. Why this is notable is because of the fact that this architecture and weights has given me a staggering accuracy and performance. I have attached a few images of results below. 

![alt text](https://github.com/kazzastic/Atavi-prj/blob/master/results.png)

The confusion matrix also shows quite accurate results, 

![alt text](https://github.com/kazzastic/Atavi-prj/blob/master/confusion_matrix_normalized.png)

650 training images and 190 validation images, the rest I kept for testing later on from frontend or postman. 

The images are resized to 640 x 640 size, this is also mentioned in the training notebook, the original size of the images was quite large, in order to train the network a smaller size was preferred in order to optimize the training time.