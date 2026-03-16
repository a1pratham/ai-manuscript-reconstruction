from transformers import TrOCRProcessor, VisionEncoderDecoderModel, logging
from PIL import Image
import warnings

# 1. Mute standard Python warnings
warnings.filterwarnings("ignore")

# 2. Mute Hugging Face informational logs (Only show critical errors)
logging.set_verbosity_error()

print("Loading TrOCR Handwriting AI...")
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def read_handwriting(image_path):
    # print(f"\nAnalyzing ink loops and cursive in: {image_path}...")
    image = Image.open(image_path).convert("RGB")
    
    pixel_values = processor(image, return_tensors="pt").pixel_values
    
    generated_ids = model.generate(pixel_values, max_new_tokens=50)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return generated_text

if __name__ == "__main__":
    test_image = "datasets/iam_lines/iam_6.png" 
    
    text = read_handwriting(test_image)
    
    print("\n--- AI EXTRACTED HANDWRITING ---")
    print(text)