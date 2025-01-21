import os
import numpy as np
from PIL import Image
import torch
from diffusers import StableDiffusionXLPipeline
import onnxruntime as ort
from transformers import CLIPTokenizer
from typing import Optional, Union, List
import shutil

class SDXLTurboOnnx:
	def __init__(self, model_path: str = "stabilityai/sdxl-turbo", cache_dir: str = "models/sdxl-turbo"):
		self.model_path = model_path
		self.cache_dir = cache_dir
		self.onnx_dir = os.path.join(self.cache_dir, "onnx")
		self.providers = ['CPUExecutionProvider']  # Only use CPU provider
		
		# Create cache directory if it doesn't exist
		os.makedirs(self.cache_dir, exist_ok=True)
		
		# Initialize pipeline
		self.pipe = StableDiffusionXLPipeline.from_pretrained(
			self.model_path,
			torch_dtype=torch.float32,  # Use float32 for CPU
			use_safetensors=True
		)
		
		# Move to CPU
		self.pipe.to("cpu")

		
		# Export to ONNX if not exists
		if not os.path.exists(self.onnx_dir):
			self._export_to_onnx()

	def _export_to_onnx(self):
		"""Export pipeline to ONNX format"""
		print(f"Exporting model to ONNX format in {self.onnx_dir}")
		
		try:
			# Export the pipeline to ONNX
			self.pipe.export_to_onnx(self.onnx_dir)
			print("Model export complete")
			
		except Exception as e:
			raise RuntimeError(f"Failed to export model to ONNX: {str(e)}")

	def generate(
		self,
		prompt: Union[str, List[str]],
		negative_prompt: Optional[Union[str, List[str]]] = None,
		num_inference_steps: int = 1,
		guidance_scale: float = 0.0,
		width: int = 512,
		height: int = 512,
		seed: Optional[int] = None
	) -> Image.Image:
		"""Generate image using the pipeline"""
		if seed is not None:
			generator = torch.Generator("cpu").manual_seed(seed)  # Use CPU generator
		else:
			generator = None
			
		# Generate image using the pipeline
		output = self.pipe(
			prompt=prompt,
			negative_prompt=negative_prompt,
			num_inference_steps=num_inference_steps,
			guidance_scale=guidance_scale,
			width=width,
			height=height,
			generator=generator
		)
		
		return output.images[0]

# Example usage
if __name__ == "__main__":
	# Initialize pipeline
	pipeline = SDXLTurboOnnx()
	
	# Get prompt from user
	prompt = input("Enter prompt: ")
	
	# Generate image
	image = pipeline.generate(
		prompt=prompt,
		num_inference_steps=1,
		width=512,
		height=512
	)
	
	# Create output directory
	os.makedirs("output/sdxl_onnx", exist_ok=True)
	
	# Find next available number
	existing_files = os.listdir("output/sdxl_onnx")
	next_num = len(existing_files) + 1
	
	# Create filename with number and prompt
	safe_prompt = "".join(x for x in prompt if x.isalnum() or x in " -_")[:50]  # Clean prompt for filename
	filename = f"{next_num:04d}_{safe_prompt}.png"
	
	# Save image
	image.save(os.path.join("output/sdxl_onnx", filename))

