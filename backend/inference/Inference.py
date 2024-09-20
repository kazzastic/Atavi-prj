from ultralytics import YOLO

def tensor_predict(image):
    #Load the model
    model = YOLO('../weights/best.pt')

    #Run inference with conf
    results = model.predict(
        source = image,
        save = False,
        conf = 0.25
    )

    for res in results:
        return res.boxes.data