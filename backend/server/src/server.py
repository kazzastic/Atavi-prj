#FastAPI imports
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse

#Local imports 
from schemas.Prediction import PredictionStore
from models.Prediction import Predict
from database import SessionLocal, get_db
from inference.Inference import tensor_predict 

#Python util imports
from sqlalchemy.orm import Session
import json
import shutil
from io import BytesIO
from PIL import Image

CLASS_NAMES = {
    0: "Missing_hole", 
    1: "Mouse_bite", 
    2: "Open_circuit", 
    3: "Short", 
    4: "Spur", 
    5: "Spurious_copper"
}

app = FastAPI()

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