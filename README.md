# Atavi-prj

Deployed: http://34.38.123.215:8081/

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


## Backend 

The backend is made totally using python and FastAPI, along with different recommended FastAPI libraries like pydantic and SQLAlchemy. 

The backend consists of 2 API's and an inferencing utility script which makes the actual prediction. 

1. /predict 
2. /visualize

### /predict

The endpoint takes an image and confidence value from the frontend or postman, triggers the model and results a json result such that, 

```
{
  "predictions": [
    {
      "bounding_box": {
        "x_min": 1207.2335205078125,
        "y_min": 1306.0362548828125,
        "x_max": 1238.0140380859375,
        "y_max": 1347.3870849609375
      },
      "confidence": 0.627797544002533,
      "label": "Mouse_bite"
    },
    {
      "bounding_box": {
        "x_min": 2820.980224609375,
        "y_min": 826.7039184570312,
        "x_max": 2853.017578125,
        "y_max": 879.692626953125
      },
      "confidence": 0.5743025541305542,
      "label": "Mouse_bite"
    }
  ]
}
```
a JSON object is returned. 

### /visualize

This endpoint takes same request, image and confidence value, triggers the model, with a tad bit of processing on the backend server, an image is returned with bounding boxes already populated with prediction class and probability values. 

![alt text](https://github.com/kazzastic/Atavi-prj/blob/master/pred.jpeg) 

### Frontend 

The frontend is made using Vue.js and axios, there are two components. 
1. PredictComponent
2. VisualizeComponent

Both components takes the images and confidence values from a multi-part form and the response is displayed accordingly. 

### How to run?

In order to run this project, I would suggest to go with the most straightforward method which is from the root directory, 

`docker-compose up`

this will expose the frontend on, 

`localhost:8081`

and backend on, 

`localhost:8000`

and postgres on port number `5432`

the only issue you might encounter is setting up the postgres since it requires environment variables, you must make two `.env` files one in the root directory and other in the `/backend` directory, which will contain the following, 

```
POSTGRES_USER=<YOUR-USER-NAME>

POSTGRES_PASSWORD=<YOUR-PASSWORD>

POSTGRES_DB=<YOUR-DATABASE-NAME>
```

I hope you enjoy, if any problem comes, please feel free to open issues or reach out to me. 
