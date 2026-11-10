import os
import json
import urllib.request
from PIL import Image, ImageDraw

def download_file(url, target_path, desc):
    print(f"Downloading {desc}...")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as resp, open(target_path, 'wb') as f:
        f.write(resp.read())
    size_mb = os.path.getsize(target_path) / (1024 * 1024)
    print(f" -> Saved to {target_path} ({size_mb:.2f} MB)")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    sample_dir = os.path.join(base_dir, "sample_images")
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(sample_dir, exist_ok=True)

    # 1. Download Quantized ONNX Model (2.56 MB)
    model_url = "https://huggingface.co/onnx-community/mobilenet_v2_1.0_224-plant-disease-identification-ONNX/resolve/main/onnx/model_quantized.onnx"
    model_path = os.path.join(models_dir, "plant_disease_model_quantized.onnx")
    if not os.path.exists(model_path) or os.path.getsize(model_path) < 1000000:
        download_file(model_url, model_path, "Quantized INT8 Edge ONNX Model")
    else:
        print(f"Model already present: {model_path}")

    # 2. Download Config and Extract 38 Labels
    config_url = "https://huggingface.co/onnx-community/mobilenet_v2_1.0_224-plant-disease-identification-ONNX/raw/main/config.json"
    labels_path = os.path.join(models_dir, "labels.json")
    if not os.path.exists(labels_path):
        print("Fetching class label map...")
        req = urllib.request.Request(config_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            id2label = data.get("id2label", {})
            with open(labels_path, "w", encoding="utf-8") as f:
                json.dump(id2label, f, indent=2)
        print(f" -> Saved {len(id2label)} classes to {labels_path}")
    else:
        print(f"Labels already present: {labels_path}")

    # 3. Download Sample Leaf Images
    samples = [
        (
            "https://upload.wikimedia.org/wikipedia/commons/5/50/Apple_scab.jpg",
            os.path.join(sample_dir, "apple_scab.jpg"),
            "Apple Scab sample"
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Early_blight_on_tomato_leaf.JPG/800px-Early_blight_on_tomato_leaf.JPG",
            os.path.join(sample_dir, "tomato_early_blight.jpg"),
            "Tomato Early Blight sample"
        ),
        (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Healthy_apple_leaves.jpg/800px-Healthy_apple_leaves.jpg",
            os.path.join(sample_dir, "healthy_apple_leaf.jpg"),
            "Healthy Apple Leaf sample"
        )
    ]

    for url, path, desc in samples:
        if not os.path.exists(path):
            try:
                download_file(url, path, desc)
            except Exception as e:
                print(f"Warning: could not download {desc} ({e}). Generating test leaf image.")
                img = Image.new("RGB", (300, 300), color=(46, 125, 50))
                draw = ImageDraw.Draw(img)
                draw.ellipse([50, 30, 250, 270], fill=(76, 175, 80), outline=(27, 94, 32))
                draw.line([150, 30, 150, 270], fill=(27, 94, 32), width=3)
                img.save(path)
                print(f" -> Generated fallback sample: {path}")

    print("\nAll model and sample assets configured successfully!")

if __name__ == "__main__":
    main()

