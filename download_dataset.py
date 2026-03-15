import os
from datasets import load_dataset

print("Connecting to Hugging Face to download IAM handwriting images...")

# Swapped to the official, perfectly formatted IAM dataset
dataset = load_dataset("Teklia/IAM-line", split='train', streaming=True)

# Create a clean folder for your images
output_dir = "datasets/iam_lines"
os.makedirs(output_dir, exist_ok=True)

print("Saving the first 5 line images and their text...")

# Open a text file to save the "Ground Truth" answers
with open(f"{output_dir}/ground_truth.txt", "w", encoding="utf-8") as f:
    
    iterator = iter(dataset)
    for i in range(5):
        sample = next(iterator)
        image = sample['image'] # The actual picture
        text = sample['text']   # The correct transcription
        
        # Save the image as a PNG
        img_filename = f"iam_{i}.png"
        image.save(f"{output_dir}/{img_filename}")
        
        # Save the answer to the text file
        f.write(f"{img_filename} | {text}\n")
        print(f"Saved: {img_filename}")

print(f"\nSuccess! Check the '{output_dir}' folder in your project.")