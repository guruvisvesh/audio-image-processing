# 🎧 Audio & Image Processing System

## 📌 Overview
This project combines **image processing and audio signal processing** techniques using Python. It captures images from a camera, applies edge detection, and performs advanced audio operations like time-scaling, mixing, and system property analysis.

---

## 🎯 Features

### 🖼️ Image Processing
- Capture image using webcam
- Convert to grayscale
- Perform edge detection (Canny)
- Save processed images

### 🔊 Audio Processing
- Load and process audio signals
- Time-scale audio (speed up / slow down)
- Mix vocal and background music
- Normalize audio output
- Save processed audio files

---

## 🧠 Concepts Used
- OpenCV (Image Processing)
- NumPy (Signal manipulation)
- FFT (Frequency analysis)
- Linear systems properties:
  - Linearity
  - Time invariance

---

## ⚙️ Tech Stack
- Python
- OpenCV
- NumPy
- Matplotlib
- SoundDevice
- SoundFile

---

## 🚀 How It Works

### 📸 Image Pipeline
1. Capture image from camera
2. Convert to grayscale
3. Apply edge detection
4. Save output images

### 🎵 Audio Pipeline
1. Load vocal & background audio
2. Apply time scaling
3. Mix signals
4. Normalize output
5. Save processed audio

---

## 📊 Outputs
- Grayscale image
- Edge-detected image
- Time-scaled audio
- Mixed audio output

---

## ▶️ How to Run

```bash
pip install opencv-python numpy matplotlib sounddevice soundfile
python src/audio_processing.py
python src/camera.py
