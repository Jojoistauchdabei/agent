from diffusers import AutoPipelineForText2Image
import torch
from datetime import datetime
import os

# Global pipeline variable
pipeline = None

def initialize_pipeline(model_dir="models/sdxl-turbo"):
    global pipeline
    if pipeline is not None:
        return pipeline
        
    os.makedirs(model_dir, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Check if model exists locally
    try:
        pipeline = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            variant="fp16" if device == "cuda" else None,
            local_files_only=True,
            cache_dir=model_dir
        )
    except Exception:
        # If local load fails, download model
        pipeline = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            variant="fp16" if device is "cuda" else None,
            local_files_only=False,
            cache_dir=model_dir
        )
    
    pipeline = pipeline.to(device)
    return pipeline

def generate_image(prompt, output_dir="output/generated_images"):
    global pipeline
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize pipeline if not already done
    if pipeline is None:
        pipeline = initialize_pipeline()
    
    # Generate image
    image = pipeline(
        prompt=prompt,
        width=512,
        heigh=1024,
        num_inference_steps=2,
        guidance_scale=0.0,
    ).images[0]
    
    # Sanitize prompt for filename
    safe_prompt = "".join(x for x in prompt if x.isalnum() or x.isspace())
    safe_prompt = safe_prompt[:50].strip()  # Limit length and trim whitespace
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sdxl_turbo_{timestamp}_{safe_prompt}.png"
    filepath = os.path.join(output_dir, filename)
    
    image.save(filepath)
    print(f"Image saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    prompt = input("Enter prompt: ")
    generate_image(prompt)
