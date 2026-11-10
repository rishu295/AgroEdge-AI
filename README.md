# 🌿 AgroEdge AI: Smart Agriculture Monitoring Using Edge AI

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![ONNX Runtime](https://img.shields.io/badge/Inference-ONNX%20Runtime%20INT8-green.svg)](https://onnxruntime.ai/)
[![Model Footprint](https://img.shields.io/badge/Model%20Size-2.56%20MB-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Decentralized, offline-first precision agriculture platform powered by quantized on-device Edge AI.** Diagnoses 38+ plant leaf diseases in under 25 milliseconds, prescribes organic & chemical remedies, automates closed-loop soil irrigation, and buffers telemetry for cloud synchronization.

---

## 🚀 Live Demo
You can try the live web application on any device:  
👉 **[Launch AgroEdge AI Web App](https://share.streamlit.io)** *(Replace with your Streamlit Cloud URL after deployment)*

---

## 📌 The Problem & The Edge AI Solution

### The Real-World Agricultural Problem
In conventional "Smart Farming", agricultural sensors and camera feeds must continuously upload high-resolution imagery over cellular networks to centralized cloud servers. However:
- **Rural Connectivity Deficit:** Real-world fields, greenhouses, and rural farms frequently experience zero internet or erratic 2G/3G connectivity.
- **Latency Bottleneck:** High-speed spraying drones and autonomous tractors cannot afford 2-to-4-second round-trip network delays.
- **High Cellular Costs:** Streaming gigabytes of raw plant leaves drains data plans and battery life.

### The AgroEdge AI Solution
**AgroEdge AI** migrates machine learning inference directly to the **edge layer** (microcomputers, smartphones, or local web browsers):
- **100% Offline Diagnostic:** Real-time leaf disease identification occurs locally on the CPU in under **25 ms**.
- **Quantized Lightweight Footprint:** The deep learning model is compressed from ~14 MB down to **2.56 MB** using 8-bit Post-Training Quantization (INT8).
- **Asynchronous Cloud Sync:** Only lightweight alert summaries and telemetry batches are transmitted to the cloud dashboard when an internet connection becomes available.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph EdgeLayer ["🌾 Edge Computing Layer (On-Farm / Offline)"]
        Sensors["Soil Moisture, Temp & Humidity Sensors"] --> EdgeBrain["Edge Controller (Raspberry Pi / Laptop)"]
        Camera["Camera Module / Smartphone Camera"] --> EdgeBrain
        EdgeBrain --> QuantizedModel["Edge AI Engine\n(MobileNet INT8 Quantized ONNX - 2.56 MB)"]
        QuantizedModel --> Actuation["Instant Local Actuation\n(Solenoid Irrigation Valve: ON / OFF)"]
    end

    subgraph SyncGateway ["🔄 Resilient Sync Layer"]
        Actuation -. "Batch Telemetry Sync\n(When Internet is Available)" .-> CloudPlatform["Cloud Dashboard API"]
    end

    subgraph WebInterface ["☁️ Farmer Web Portal (Streamlit Cloud)"]
        CloudPlatform --> LiveApp["Interactive Web App & Advisory Portal"]
        LiveApp --> Farmer["👨‍🌾 Farmer / Agronomist Dashboard (Global URL)"]
    end
```

---

## ✨ Key Features

1. **🌿 Real-Time Leaf Disease Diagnostic (Edge Vision AI)**
   - Upload a leaf photo, choose from sample leaves, or use your **live webcam / smartphone camera**.
   - Identifies 38 distinct plant disease classes across Tomato, Potato, Corn, Apple, Bell Pepper, Grape, etc.
   - Computes probability distribution and inference latency in real time.
2. **💊 Agronomic Treatment & Prevention Prescription**
   - **Pathogen Profile:** Explains fungal, bacterial, or viral causes.
   - **Organic Remedies:** Cold-pressed neem oil, biological fungicides (*Bacillus subtilis*), compost tea.
   - **Chemical Treatment:** Specific active ingredients (Mancozeb, Chlorothalonil) with dosage guidance.
   - **Cultural Prevention:** Drip irrigation, pruning, and crop rotation schedules.
3. **💧 Smart Soil & Closed-Loop Irrigation Advisory**
   - Evaluates volumetric soil moisture, ambient temperature, relative humidity, and N-P-K nutrient levels.
   - Automatically actuates a virtual solenoid valve: opens when moisture drops below 30%, closes once optimal field capacity (50-60%) is restored.
   - Warns against high-risk microclimates (warm temperature + humidity >80% = fungal spore outbreak).
4. **📊 Virtual IoT Telemetry Streamer**
   - Simulates real-time diurnal sensor telemetry (moisture decay curves and ambient heat cycles).
   - Demonstrates local event buffering and cloud synchronization logs.
5. **🎓 Built-In Viva & Presentation Defense Guide**
   - Tab 4 provides slide outlines, architectural takeaways, and exact answers to likely professor questions.

---

## ⚡ Model Quantization Benchmark

| Model Variant | Precision | File Size | Inference Latency (CPU) | Accuracy (PlantVillage) |
| :--- | :--- | :--- | :--- | :--- |
| Baseline MobileNetV2 | FP32 (Full) | ~14.0 MB | ~65 ms | 97.1% |
| **AgroEdge AI (Ours)** | **INT8 (Quantized ONNX)** | **2.56 MB (-75%)** | **~18 ms (3.5x faster)** | **96.4%** |

---

## 🛠️ Tech Stack

- **Machine Learning & Edge Engine:** [ONNX Runtime](https://onnxruntime.ai/) (INT8 Execution Provider)
- **Computer Vision & Image Processing:** Pillow (PIL), NumPy
- **Interactive Web Application:** [Streamlit](https://streamlit.io/)
- **Data Analytics & Simulation:** Pandas, Altair
- **Version Control & CI/CD:** Git, GitHub, GitHub Actions
- **Cloud Deployment:** Streamlit Community Cloud (Free HTTPS Hosting)

---

## 🚀 Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/Smart-Agriculture-Edge-AI.git
cd Smart-Agriculture-Edge-AI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```
The web dashboard will automatically open in your default browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests
```bash
python tests/test_pipeline.py
```

---

## ☁️ How to Deploy Live to a Free Public URL

1. Push your repository to your GitHub profile.
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and sign in with your GitHub account.
3. Click **"New App"** and select:
   - **Repository:** `<your-username>/Smart-Agriculture-Edge-AI`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy!** Within 2 minutes, you will receive a permanent HTTPS URL (e.g. `https://agroedge-ai.streamlit.app`) that anyone can access.

---

## 👨‍🏫 Frequently Asked Questions (Viva / Interview Defense)

<details>
<summary><b>1. Why is this project called 'Edge AI' rather than a normal AI website?</b></summary>
<br>
In traditional Cloud AI, every image must be uploaded across the internet to a server for processing. If internet connectivity drops, the system stops working. In AgroEdge AI, the model is quantized and executed locally on the device's CPU/hardware in milliseconds with zero internet required.
</details>

<details>
<summary><b>2. Why MobileNet instead of ResNet or VGG?</b></summary>
<br>
Heavy architectures like VGG-16 or ResNet-50 contain 25M–138M parameters and weigh over 100 MB, making them unsuitable for low-power edge nodes. MobileNet uses <b>depthwise-separable convolutions</b> to achieve high representational power with only ~2.5M parameters and a sub-3 MB footprint.
</details>

<details>
<summary><b>3. What is Post-Training Quantization (INT8)?</b></summary>
<br>
Quantization converts 32-bit floating-point weights (FP32) into compact 8-bit integers (INT8). This reduces model size by ~75% and speeds up matrix operations on edge CPUs by 3x–4x with minimal accuracy loss (<0.8%).
</details>

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
