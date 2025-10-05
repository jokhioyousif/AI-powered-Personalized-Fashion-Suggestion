# File: fastapi_backend.py
# Purpose: The backend API server. Runs locally and communicates with the Colab AI worker.

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
import requests
import json
from typing import List

# --- Configuration ---
# Paste the public URL from your Google Colab notebook here.

COLAB_AI_WORKER_URL = "ngrok url here/generate" 

app = FastAPI()

@app.post("/create-look")
async def create_look(
    user_image: UploadFile = File(...),
    height: int = Form(...),
    weight: int = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    style: str = Form(...),
    occasion: str = Form(...),
    clothing_items: str = Form(...),
    preferred_colors: str = Form(None)
):
    """
    This endpoint receives all the data from the Streamlit frontend,
    forwards it to the Google Colab AI worker, and streams the
    resulting image back.
    """
    print("Backend: Received request from Streamlit frontend.")

    # Prepare the data to be sent to the Colab worker
    # The Colab worker expects the same multipart format
    files = {'user_image': (user_image.filename, await user_image.read(), user_image.content_type)}
    
    data = {
        'height': height,
        'weight': weight,
        'age': age,
        'gender': gender,
        'style': style,
        'occasion': occasion,
        'preferred_colors': preferred_colors,
        'clothing_items': clothing_items # Forward the JSON string directly
    }

    try:
        print(f"Backend: Forwarding request to Colab AI Worker at {COLAB_AI_WORKER_URL}...")
        
        # Forward the request to the Colab AI Worker
        response = requests.post(COLAB_AI_WORKER_URL, files=files, data=data, timeout=300, stream=True)
        
        # Check the response from the Colab worker
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        print("Backend: Received successful response from Colab. Streaming image back to frontend.")
        
        # Stream the image content back to the Streamlit frontend
        return StreamingResponse(response.iter_content(chunk_size=8192), media_type=response.headers['Content-Type'])

    except requests.exceptions.RequestException as e:
        print(f"Backend ERROR: Could not connect to the Colab AI worker. {e}")
        raise HTTPException(status_code=503, detail=f"The AI Worker is not reachable. Details: {e}")
    except Exception as e:
        print(f"Backend ERROR: An unexpected error occurred. {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred in the backend. Details: {e}")

# --- How to Run This File ---
# 1. Make sure you have fastapi and uvicorn installed:
#    pip install "fastapi[all]"
# 2. In your terminal, run this command:
#    uvicorn fastapi_backend:app --reload

if __name__ == "__main__":
    uvicorn.run("fastapi_backend:app", host="127.0.0.1", port=8000, reload=True)
