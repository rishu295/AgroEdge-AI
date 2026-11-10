"""
test_pipeline.py
================
Smoke tests for the Edge AI Plant Disease Classifier and Soil Advisory.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image
from src.classifier import EdgePlantClassifier
from src.remedies import get_remedy
from src.soil_advisor import evaluate_soil_and_irrigation

def test_classifier_initialization():
    classifier = EdgePlantClassifier()
    assert classifier.session is not None, "ONNX Session should be initialized"
    assert len(classifier.labels) == 38, "Should load 38 PlantVillage classes"
    print("✅ Classifier initialization test passed!")

def test_inference_on_sample():
    classifier = EdgePlantClassifier()
    sample_path = os.path.join(os.path.dirname(__file__), "..", "sample_images", "apple_scab.jpg")
    img = Image.open(sample_path)
    res = classifier.predict(img)
    
    assert "prediction" in res
    assert "confidence" in res
    assert res["confidence"] > 0
    assert res["latency_ms"] > 0
    assert len(res["top_3"]) == 3
    print(f"✅ Inference test passed! (Predicted: {res['prediction']} in {res['latency_ms']} ms)")

def test_remedies_lookup():
    remedy = get_remedy("Apple Scab")
    assert "pathogen" in remedy
    assert "organic" in remedy
    assert "chemical" in remedy
    print("✅ Remedies lookup test passed!")

def test_soil_advisor():
    # Dry soil -> valve should activate
    res_dry = evaluate_soil_and_irrigation(soil_moisture=20.0, temperature=28.0, humidity=85.0, nitrogen=40, phosphorus=20, potassium=20)
    assert "ACTIVATED" in res_dry["valve_status"]
    assert "HIGH" in res_dry["disease_risk"]
    
    # Optimal soil -> valve should be standby
    res_opt = evaluate_soil_and_irrigation(soil_moisture=45.0, temperature=24.0, humidity=50.0, nitrogen=80, phosphorus=40, potassium=40)
    assert "STANDBY" in res_opt["valve_status"]
    print("✅ Soil advisory test passed!")

if __name__ == "__main__":
    test_classifier_initialization()
    test_inference_on_sample()
    test_remedies_lookup()
    test_soil_advisor()
    print("\n🎉 ALL PIPELINE TESTS PASSED!")
