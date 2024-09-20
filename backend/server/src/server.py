#FastAPI imports
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

#Local imports 
from models.Prediction import Predict
from database import SessionLocal, get_db
from inference.Inference import tensor_predict

#Python util imports
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json

CLASS_NAMES = {
    0: "Missing_hole", 
    1: "Mouse_bite", 
    2: "Open_circuit", 
    3: "Short", 
    4: "Spur", 
    5: "Spurious_copper"
}

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:8080",  # Allow frontend's origin
    # You can add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

def draw_predictions_on_image(img, predictions, confidence_limit):
    # Create a drawing context to overlay predictions
    draw = ImageDraw.Draw(img)
    
    # Optionally, you can set a font for labels (e.g., for drawing text)
    try:
        font = ImageFont.load_default()  # You can load custom fonts here if needed
    except IOError:
        font = None

    # Iterate through predictions and draw boxes
    for prediction in predictions:
        x_min, y_min, x_max, y_max, confidence, class_id = prediction.tolist()

        # Apply confidence limit filter
        if confidence >= confidence_limit:
            label = CLASS_NAMES.get(int(class_id), "Unknown")
            confidence_text = f"{label}: {confidence:.2f}"

            # Draw bounding box
            draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)

            # Draw label above the box (with some padding)
            if font:
                text_position = (x_min, y_min - 10)  # Slightly above the box
                draw.text(text_position, confidence_text, fill="yellow", font=font)

    return img

@app.post("/predict")
async def predict_image(
    image: UploadFile = File(...),
    confidence_limit: float = Form(..., description="Confidence limit for predictions"),
    db: Session = Depends(get_db)
):
    try:
        #Ensure file in request is an image
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(status_code=400, detail="File Type Not Supported")
        
        #Load image 
        image_data = await image.read()
        img = Image.open(BytesIO(image_data))

        #Calling the inference function with image and confidence
        predictions = tensor_predict(img)

        # Formatting the predictions for response
        result_data = []
        for prediction in predictions:
            x_min, y_min, x_max, y_max, confidence, class_id = prediction.tolist()

            #only consider limits with confidence limit 
            if confidence >= confidence_limit:
                class_id = int(class_id)
                label = CLASS_NAMES.get(class_id, "unknown")

                result = {
                    "bounding_box": {
                        "x_min": float(x_min), 
                        "y_min": float(y_min), 
                        "x_max": float(x_max), 
                        "y_max": float(y_max)
                    },
                    "confidence": float(confidence),
                    "label": label
                }
                result_data.append(result)

        new_data = Predict(data = result_data)
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        
        return JSONResponse(content={"predictions": result_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error ocurred: {str(e)}")
    
@app.post('/visualize')
async def visualize_image(
    image: UploadFile = File(...),
    confidence_limit: float = Form(..., description="Confidence limit for predictions"),
    db: Session = Depends(get_db)
):
    try:
        # Ensure file in request is an image
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(status_code=400, detail="File Type Not Supported")
        
        # Load image 
        image_data = await image.read()
        img = Image.open(BytesIO(image_data))

        # Call inference function to get predictions
        predictions = tensor_predict(img)

        # Draw predictions (bounding boxes and labels) on the image
        img_with_predictions = draw_predictions_on_image(img, predictions, confidence_limit)

        # Save the image to an in-memory bytes buffer
        buf = BytesIO()
        img_with_predictions.save(buf, format="JPEG")  # You can choose the format (JPEG, PNG)
        buf.seek(0)

        # Save the result data in the database
        result_data = []
        for prediction in predictions:
            x_min, y_min, x_max, y_max, confidence, class_id = prediction.tolist()
            if confidence >= confidence_limit:
                class_id = int(class_id)
                label = CLASS_NAMES.get(class_id, "unknown")
                result = {
                    "bounding_box": {
                        "x_min": float(x_min), 
                        "y_min": float(y_min), 
                        "x_max": float(x_max), 
                        "y_max": float(y_max)
                    },
                    "confidence": float(confidence),
                    "label": label
                }
                result_data.append(result)

        new_data = Predict(data=json.dumps(result_data))
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        # Return the image with the predictions as a StreamingResponse
        return StreamingResponse(buf, media_type="image/jpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")