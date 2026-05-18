# Smart Helmet Detection System
# Second Year Project
# Technologies: YOLOv8, OpenCV, ESP32, Python

import cv2
import serial
import time
import os
import datetime
from collections import deque
from ultralytics import YOLO

# ================= ESP32 =================
try:
    esp32 = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("ESP32 Connected")
except:
    esp32 = None
    print("ESP32 NOT connected")

# ================= MODEL =================
model = YOLO("best.pt")
cap = cv2.VideoCapture(0)

# ================= SETTINGS =================
HELMET_CONF = 0.89
HEAD_CONF = 0.60

STATE_HOLD_TIME = 3
DETECTION_TIMEOUT = 2

# ================= MEMORY =================
decision_buffer = deque(maxlen=5)
last_valid_state = '2'
last_detection_time = time.time()

# ================= STATE LOCK =================
locked_state = '2'
state_start_time = time.time()

# ================= SAVE =================
SAVE_FOLDER = "violations"
os.makedirs(SAVE_FOLDER, exist_ok=True)

saved_positions = []
POSITION_THRESHOLD = 120
COOLDOWN_TIME = 10

frame_count = 0

print("Press ESC to exit")

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    helmet_detected = False
    head_detected = False

    # Run model every 2 frames
    if frame_count % 2 == 0:
        results = model(frame, verbose=False)
    else:
        results = []

    for r in results:
        for box in r.boxes:

            conf = float(box.conf[0])
            label = model.names[int(box.cls[0])].lower()

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # ================= SIZE FILTER =================
            w, h = x2 - x1, y2 - y1
            if w < 50 or h < 50:
                continue

            # ================= CENTER FILTER =================
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            fh, fw = frame.shape[:2]

            if not (fw*0.2 < cx < fw*0.8 and fh*0.2 < cy < fh*0.8):
                continue

            # ================= HELMET FILTER =================
            if label == "helmet" and conf > HELMET_CONF:

                #  Reject if too big (false helmet)
                area = w * h
                if area > 0.25 * (fw * fh):
                    continue

                helmet_detected = True
                cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)

            # ================= HEAD FILTER =================
            elif label == "head" and conf > HEAD_CONF:
                head_detected = True
                cv2.rectangle(frame, (x1,y1),(x2,y2),(0,0,255),2)

    
    if helmet_detected and not head_detected:
        current_state = '1'
        text = "HELMET -> GREEN"
        color = (0,255,0)

        last_valid_state = '1'
        last_detection_time = time.time()

    elif head_detected:
        current_state = '0'
        text = "NO HELMET -> RED"
        color = (0,0,255)

        last_valid_state = '0'
        last_detection_time = time.time()

        # SAVE VIOLATION
        cx = frame.shape[1] // 2
        cy = frame.shape[0] // 2
        now = time.time()

        already_saved = False
        for (px, py, t) in saved_positions:
            dist = ((cx-px)**2 + (cy-py)**2)**0.5
            if dist < POSITION_THRESHOLD and (now-t) < COOLDOWN_TIME:
                already_saved = True
                break

        if not already_saved:
            filename = os.path.join(
                SAVE_FOLDER,
                f"no_helmet_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            cv2.imwrite(filename, frame)
            print("Saved:", filename)

            saved_positions.append((cx, cy, now))
            if len(saved_positions) > 50:
                saved_positions.pop(0)

    else:
        # ================= MEMORY =================
        if time.time() - last_detection_time < DETECTION_TIMEOUT:
            current_state = last_valid_state

            if current_state == '1':
                text = "HELMET (HOLD)"
                color = (0,255,0)
            else:
                text = "NO HELMET (HOLD)"
                color = (0,0,255)
        else:
            current_state = '2'
            text = "DETECTING -> YELLOW"
            color = (0,255,255)

    # ================= TEMPORAL VOTING =================
    decision_buffer.append(current_state)
    current_state = max(set(decision_buffer), key=decision_buffer.count)

    # ================= STATE LOCK =================
    if current_state != locked_state:
        if time.time() - state_start_time > STATE_HOLD_TIME:
            locked_state = current_state
            state_start_time = time.time()

            if esp32:
                esp32.write(locked_state.encode())

    # ================= DISPLAY =================
    cv2.putText(frame, text, (20,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow("ULTIMATE ACCURATE SYSTEM", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

if esp32:
    esp32.close()