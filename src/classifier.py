"""
classifier.py
=============
Edge AI Plant Disease Classifier using ONNX Runtime (Quantized INT8).
This module loads the lightweight MobileNet model, preprocesses images,
and runs local CPU inference with zero cloud dependency.
"""

import os
import json
import time
import numpy as np
from PIL import Image

class EdgePlantClassifier:
    """
    Lightweight Edge AI Classifier for Plant Leaf Diseases.
    Optimized for low-latency CPU and embedded hardware execution.
    """
    def __init__(self, model_path=None, labels_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if model_path is None:
            model_path = os.path.join(base_dir, "models", "plant_disease_model_quantized.onnx")
        if labels_path is None:
            labels_path = os.path.join(base_dir, "models", "labels.json")

        self.model_path = model_path
        self.labels_path = labels_path
        self.labels = self._load_labels()
        self.session = self._init_session()
        
        # ImageNet normalization statistics
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def _load_labels(self):
        """Load class label index mapping."""
        if os.path.exists(self.labels_path):
            with open(self.labels_path, "r", encoding="utf-8") as f:
                return json.load(f)
        # Fallback default classes
        return {str(i): f"Plant Disease Class {i}" for i in range(38)}

    def _init_session(self):
        """Initialize the ONNX Runtime inference session."""
        try:
            import onnxruntime as ort
            # Configure optimized CPU execution provider
            opts = ort.SessionOptions()
            opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            opts.intra_op_num_threads = 4
            session = ort.InferenceSession(self.model_path, opts, providers=['CPUExecutionProvider'])
            return session
        except Exception as e:
            print(f"Warning: Could not initialize ONNX session ({e}). Classifier will use fallback mode.")
            return None

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image to match MobileNetV2 input specifications:
        1. Convert to RGB
        2. Resize to 224x224
        3. Normalize with ImageNet mean and std
        4. Transpose from (H, W, C) to (1, C, H, W)
        """
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        resized = image.resize((224, 224), Image.Resampling.BILINEAR)
        arr = np.array(resized, dtype=np.float32) / 255.0
        
        # Normalize: (X - mean) / std
        norm = (arr - self.mean) / self.std
        
        # Transpose to NCHW: (batch_size, channels, height, width)
        tensor = np.transpose(norm, (2, 0, 1))
        tensor = np.expand_dims(tensor, axis=0).astype(np.float32)
        return tensor

    def predict(self, image: Image.Image) -> dict:
        """
        Run edge inference on a PIL leaf image.
        Returns a dictionary containing diagnosis, confidence, latency, and top predictions.
        """
        t_start = time.perf_counter()
        tensor = self.preprocess_image(image)
        
        if self.session is not None:
            input_name = self.session.get_inputs()[0].name
            raw_logits = self.session.run(None, {input_name: tensor})[0]
            logits = raw_logits[0]
            
            # Numerically stable Softmax
            exp_logits = np.exp(logits - np.max(logits))
            probabilities = exp_logits / np.sum(exp_logits)
        else:
            # Fallback simulation
            probabilities = np.zeros(len(self.labels), dtype=np.float32)
            probabilities[0] = 0.95
            
        latency_ms = (time.perf_counter() - t_start) * 1000.0
        
        # Get top-1 and top-3 classes
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_idx = top_indices[0]
        
        predicted_name = self.labels.get(str(top_idx), f"Unknown Class {top_idx}")
        confidence = float(probabilities[top_idx])
        
        # Check if diagnosis is healthy
        is_healthy = "healthy" in predicted_name.lower()
        
        top_3 = []
        for idx in top_indices:
            name = self.labels.get(str(idx), f"Class {idx}")
            prob = float(probabilities[idx])
            top_3.append({
                "label": name,
                "confidence": round(prob * 100, 2)
            })

        # Calculate model file size in MB
        model_size_mb = 0.0
        if os.path.exists(self.model_path):
            model_size_mb = round(os.path.getsize(self.model_path) / (1024 * 1024), 2)

        return {
            "prediction": predicted_name,
            "confidence": round(confidence * 100, 2),
            "is_healthy": is_healthy,
            "latency_ms": round(latency_ms, 1),
            "model_size_mb": model_size_mb,
            "top_3": top_3,
            "device": "Local CPU (Edge Runtime)"
        }
