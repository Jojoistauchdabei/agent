import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import numpy as np
import os

# Vordefinierter Speicherort für das Video
output_dir = "./output/videos"
video_filename = "spiderman_surfs.mp4"

# Erstelle den Output-Ordner, wenn er nicht existiert
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

model_id = "damo-vilab/text-to-video-ms-1.7b"
cache_dir = "./models/damo-vilab-text-to-video-ms-1.7b"

pipe = DiffusionPipeline.from_pretrained(
    model_id,
    width=255,
    heigh=255,
    cache_dir=cache_dir,
    local_files_only=False  # Set to True after first download
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

prompt = "Spiderman is surfing"
video_frames = pipe(prompt, num_inference_steps=25).frames

# Convert the frames to numpy arrays with 3 channels (RGB)
frames = [frame[:, :, :3] for frame in video_frames]

# Export the frames to video
video_path = os.path.join(output_dir, video_filename)
export_to_video(frames, output_video_path=video_path)

print(f"Video saved to: {video_path}")