# Real-Time Helmet Detection System using YOLOv8 and ESP32

## Project Overview

This project is a Real-Time Helmet Detection System developed using YOLOv8, OpenCV, Python, and ESP32.

The system detects whether a rider is wearing a helmet using live webcam video and automatically controls LED indicators through ESP32.

The project is designed to improve road safety and reduce manual monitoring at traffic signals, toll booths, and campus entrances.

---

# Features

- Real-time helmet detection
- YOLOv8 object detection
- ESP32 hardware integration
- Serial communication between Python and ESP32
- Confidence filtering
- Temporal voting system
- Detection timeout handling
- False detection reduction
- Duplicate violation save prevention
- Automatic image saving
- Green / Red / Yellow LED indication

---

# Technologies Used

- Python
- YOLOv8
- OpenCV
- NumPy
- PySerial
- ESP32
- Arduino IDE

---

# Hardware Components

- ESP32
- Webcam
- LEDs
- Breadboard
- Laptop / PC

---

# Project Structure

```bash
helmet-detection-yolo-esp32/
│
├── app.py
├── README.md
├── Report.pdf
├── Synopsis.pdf
├── Presentation.pptx
├── screenshots/
├── violations/
```

---

# Working of the System

1. Webcam captures live video
2. YOLOv8 detects helmet/head objects
3. Detection logic processes confidence values
4. System decides:
   - Helmet → GREEN LED
   - No Helmet → RED LED
   - No Person / Detecting → YELLOW LED
5. Python sends state to ESP32 through serial communication
6. ESP32 controls LEDs
7. Violation images are automatically saved

---

# Detection States

| State | LED | Meaning |
|------|------|------|
| 1 | Green | Helmet Detected |
| 0 | Red | No Helmet |
| 2 | Yellow | Detecting / No Person |

---

# Advanced Features

## Confidence Filtering
Reduces false detections using confidence thresholds.

## Temporal Voting
Uses recent frame history to stabilize predictions.

## Detection Timeout
Maintains previous valid state briefly to avoid flickering.

## Duplicate Save Prevention
Prevents repeated saving of the same violation image.

## State Locking
Avoids rapid LED switching and unstable outputs.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/mulikniranjan-lgtm/helmet-detection-yolo-esp32.git
cd helmet-detection-yolo-esp32
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install ultralytics opencv-python numpy pyserial
```

---

# Run the Project

```bash
python app.py
```

---

# Model File

The trained YOLOv8 model (`best.pt`) is not included because of GitHub file size limitations.

Download Model:
https://drive.google.com/file/d/1mo7Dnq3iA6ruDs3NttVPBEs93AsrP3s0/view?usp=drive_link

After downloading:
- Place `best.pt` in the project folder

---

# Applications

- Traffic signal monitoring
- Toll booth monitoring
- Smart city systems
- College campus entry systems
- Road safety monitoring

---

# Future Scope

- Number plate detection
- Cloud database integration
- SMS alert system
- CCTV integration
- Mobile application support
- Smart traffic management system

---

# Team Members

- Raj Nitin Kumbhar
- Sanchita Ganesh Kumbhar
- Sayali Ratan Kumbhar
- Niranjan Nitin Mulik

---

# References

- OpenCV Documentation
- YOLOv8 Documentation
- ESP32 Technical Manual
- Research Papers on Helmet Detection

---

# License

This project is developed for educational and research purposes.