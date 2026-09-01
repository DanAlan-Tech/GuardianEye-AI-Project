<div align="center">

# GuardianEye AI: Edge-Based Personal Safety Monitor

An open-source, AI-powered personal safety system designed to detect, track, and alert users to physical threats in real time. Running locally on a Raspberry Pi with a live camera feed, this project aims to protect individuals from stalkers, being followed, or planned physical ambushes.

---

### 👁️ Project Overview

Traditional security systems are reactive—recording incidents *after* they happen. **GuardianEye AI** is designed to be proactive. By combining low-power edge computing with real-time computer vision, the system analyzes a person's surroundings to identify pre-attack indicators and persistent trailing behavior before a confrontation occurs.

---

### 🛡️ Core Features

| Feature | Technology | Defensive Purpose |
| :--- | :---: | :--- |
| **Persistent Follow Detection** | Multi-Object Tracking (SORT/DeepSORT) | Identifies if the same person or vehicle remains behind the user across multiple turns or locations. |
| **Pre-Attack Indicator Alerting** | Behavioral AI / Pose Estimation | Detects suspicious physical anomalies, such as pacing, loitering near a path, hidden hands, or sudden aggressive pacing. |
| **Concealed Weapon Detection** | Object Detection (YOLOv8-Nano) | Scans for exposed or brandished firearms, knives, or blunt instruments in the camera's field of view. |
| **Silent Alert System** | Bluetooth / LoRa / Wi-Fi | Sends immediate, haptic smartphone notifications or emergency GPS coordinates to trusted contacts without alerting the threat. |
| **Privacy-First Processing** | Local Edge Computing | Runs 100% locally on the device. No video data is sent to the cloud, ensuring absolute privacy for the user. |

---

### 🏗️ Hardware Architecture

To keep the system wearable or portable (backpack-mounted), the prototype targets low-weight, high-efficiency hardware:

* **Processing Unit:** Raspberry Pi 5 (8GB)
* **AI Acceleration:** Raspberry Pi AI Kit (Hailo-8L M.2 AI module, 13 TOPS) or Google Coral USB Accelerator
* **Camera Input:** Raspberry Pi Camera Module 3 (Wide-angle) or an inconspicuous USB body-cam
* **Power Supply:** 5V/5A Power Bank (USB-PD compatible)

---

### 💻 Target Software Stack

* **Operating System:** Raspberry Pi OS (64-bit Bookworm)
* **Core Language:** Python 3.11+
* **AI Inference Framework:** Hailo TAPPAS or OpenVINO (optimized for edge hardware)
* **Computer Vision:** OpenCV & PyTorch Lite
* **Model Base:** Custom-trained YOLOv8-Nano / YOLOv11-Nano (quantized to INT8)

---

### 📈 Current Roadmap

* [ ] **Phase 1:** Hardware assembly and benchmarking baseline live video capture on Raspberry Pi 5.
* [ ] **Phase 2:** Train and deploy a lightweight YOLO model optimized for weapon and person tracking on edge devices.
* [ ] **Phase 3:** Develop the "Counter-Surveillance" algorithm to calculate distance, time-tracked, and path correlation for follow detection.
* [ ] **Phase 4:** Build the mobile companion app interface for real-time haptic alerts.

---

⚠️ **Disclaimer & Safety Notice:** This project is an aspiring research concept aimed at personal defense augmentation. It is not a replacement for situational awareness, professional security, or law enforcement.

</div>
