from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import base64
from io import BytesIO
from PIL import Image
from sdxl_onnx import generate_image

class GenerateRequest(BaseModel):
    prompt: str

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(request: GenerateRequest):
    # Generate image using SDXL
    image_path = generate_image(request.prompt)
    
    # Open and convert image to base64
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return {"image": img_str}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)