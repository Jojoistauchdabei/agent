def test_sdxl():
    from sdxl import generate_image
    prompt = "a cat in cyberpunk style"
    image_path = generate_image(prompt)
    print(f"Image generated at: {image_path}")

def test_sdxl_onnx():
    from sdxl_onnx import generate_image
    prompt = "a cat in cyberpunk style"
    image_path = generate_image(prompt)
    print(f"Image generated at: {image_path}")

test_sdxl()
test_sdxl_onnx()

print("All tests passed!")