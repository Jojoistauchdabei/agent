import torch
import os
from diffusers import MochiPipeline
from diffusers.utils import export_to_video

# Create models directory if it doesn't exist
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models/mochi-1-preview")
os.makedirs(MODEL_DIR, exist_ok=True)

# Check device availability
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32

try:
    # Initialize pipeline with device-specific settings and local cache
    pipe = MochiPipeline.from_pretrained(
        "genmo/mochi-1-preview",
        cache_dir=MODEL_DIR,
        variant="bf16" if device == "cuda" else None,
        torch_dtype=dtype
    )

    # Move pipeline to appropriate device
    pipe.to(device)

    # Enable memory optimizations
    pipe.enable_model_cpu_offload()
    pipe.enable_vae_tiling()

    # Generate frames
    prompt = "Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k."
    frames = pipe(
        prompt,
        num_frames=84,
        guidance_scale=8.0,  # Adjust for better results on CPU
        num_inference_steps=20 if device == "cpu" else 30  # Reduce steps for CPU
    ).frames[0]

    # Export video
    export_to_video(frames, "mochi.mp4", fps=30)
    print(f"Video generated successfully using {device}")

except Exception as e:
    print(f"Error during video generation: {str(e)}")
