from fastapi import FastAPI, Depends, HTTPException
import json

app = FastAPI()

@app.post("/predict")
async def predict():