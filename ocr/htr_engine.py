from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

print("Loading TrOCR Handwriting AI... (This might take a minute the first time)")
# Load the pre-trained Microsoft model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def read_handwriting(image_path):
    print(f"\nAnalyzing ink loops and cursive in: {image_path}...")
    image = Image.open(image_path).convert("RGB")
    
    # The AI looks at the image and converts it to tensor math
    pixel_values = processor(image, return_tensors="pt").pixel_values
    
    # The AI generates the text prediction
    generated_ids = model.generate(pixel_values, max_new_tokens=50)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return generated_text

if __name__ == "__main__":
    # Point this to the exact IAM handwriting image that just failed
    test_image = "datasets/iam_lines/iam_0.png" 
    
    text = read_handwriting(test_image)
    
    print("\n--- AI EXTRACTED HANDWRITING ---")
    print(text)