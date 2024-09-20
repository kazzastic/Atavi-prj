from ultralytics import YOLO

# Load the YOLOv10 model
model = YOLO('../weights/best.pt')

# Run inference on an image
results = model.predict(
    source="/Users/kazim/Downloads/PCB_DATASET/images/Spur/05_spur_10.jpg",
    save=True,  # Optional: saves output image with predictions
    conf=0.25
)

# Results Object
for result in results:
    print(result.boxes.data)  # Each result should contain the detected boxes, scores, etc.