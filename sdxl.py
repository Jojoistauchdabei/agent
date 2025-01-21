from datetime import datetime
import os
from pathlib import Path
from typing import Optional
from PIL import Image
from diffusers import AutoPipelineForText2Image
import torch

# Constants
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
DEFAULT_STEPS = 1
DEFAULT_GUIDANCE = 0.0
OUTPUT_DIR = "output/generated_images/sdxl-turbo"
MODEL_CACHE_DIR = "models/sdxl-turbo"

# Global pipeline variable
pipeline = None

def get_best_device():
    try:
        if hasattr(torch, 'hip') and torch.hip.is_available():
            # Force CPU for ROCm/HIP due to compatibility issues
            print("ROCm/HIP detected")
            return "hip", torch.float32
        elif torch.cuda.is_available():
            print("CUDA is available")
            return "cuda", torch.float16
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("MPS is available")
            return "mps", torch.float32
    except:
        pass
    return "cpu", torch.float32

def initialize_pipeline() -> "StableDiffusionPipeline":
    """Initialize the SDXL Turbo pipeline."""
    device, dtype = get_best_device()
    
    try:
        pipeline = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=dtype,
            variant="fp16" if dtype == torch.float16 else None,
            cache_dir=MODEL_CACHE_DIR
        )
        pipeline.to(device)
        print(f"Pipeline initialized on {device}")
        return pipeline
    except Exception as e:
        print(f"Failed to initialize on {device}, falling back to CPU: {str(e)}")
        # CPU fallback
        pipeline = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float32,
            cache_dir=MODEL_CACHE_DIR
        )
        pipeline.to("cpu")
        return pipeline

def sanitize_filename(prompt: str, max_length: int = 50) -> str:
    """Create a safe filename from the prompt."""
    safe_prompt = "".join(x for x in prompt if x.isalnum() or x.isspace())
    return safe_prompt[:max_length].strip()

def generate_image(prompt: str, output_dir: str = OUTPUT_DIR) -> str:
    """Generate an image from a text prompt."""
    global pipeline
    
    try:
        if pipeline is None:
            pipeline = initialize_pipeline()
            
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate the image
        output = pipeline(prompt, num_inference_steps=DEFAULT_STEPS, guidance_scale=DEFAULT_GUIDANCE)
        
        # Save the image
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_prompt = sanitize_filename(prompt)
        filename = f"{safe_prompt}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        output.images[0].save(filepath)
        return filepath
        
    except Exception as e:
        if "cuda" in str(e).lower() and pipeline is not None:
            print("CUDA error detected, falling back to CPU")
            pipeline.to("cpu")
            return generate_image(prompt, output_dir)  # Retry on CPU
        raise RuntimeError(f"Failed to generate image: {str(e)}")

if __name__ == "__main__":
    try:
        prompt = input("Enter prompt: ")
        generate_image(prompt)
    except KeyboardInterrupt:
        print("\nGeneration cancelled by user")
    except Exception as e:
        print(f"Error: {str(e)}")
