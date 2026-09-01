import time
import cv2
from ultralytics import YOLO


def start_security_tracker(video_source=0, alert_threshold_seconds=15):
    # 1. Load the lightweight YOLOv8-Nano model
    model = YOLO("yolov8n.pt")

    # 2. Initialize live camera stream
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"[-] Error: Could not open video source {video_source}")
        return

    # 3. ANTI-STALKING MEMORY BANK
    # Structure: { track_id: {"first_seen": timestamp, "last_seen": timestamp} }
    active_tracks = {}

    print("[*] GuardianEye Anti-Stalking Tracker Active.")
    print(f"[*] Threat Threshold: {alert_threshold_seconds} consecutive seconds.")
    print("[*] Press 'q' to quit safely.\n")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("[-] End of video stream or failed to grab frame.")
            break

        current_time = time.time()

        # 4. RASPBERRY PI OPTIMIZATION: Class Filtering
        # 0 = person, 2 = car, 7 = truck (COCO dataset indices)
        results = model.track(
            source=frame,
            tracker="bytetrack.yaml",
            persist=True,
            classes=[0, 2, 7],
            verbose=False,
        )

        # Track IDs seen in *this specific frame*
        ids_in_current_frame = set()

        # 5. Extract and analyze tracking targets
        if results and results.boxes and results.boxes.id is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            track_ids = results.boxes.id.cpu().numpy().astype(int)
            class_ids = results.boxes.cls.cpu().numpy().astype(int)

            for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                ids_in_current_frame.add(track_id)
                x1, y1, x2, y2 = map(int, box)
                class_name = model.names[class_id]

                # --- TIME-PERSISTENCE TRACKING LOGIC ---
                if track_id not in active_tracks:
                    # New entity discovered: log initial timestamps
                    active_tracks[track_id] = {
                        "first_seen": current_time,
                        "last_seen": current_time,
                    }
                    duration = 0.0
                else:
                    # Existing entity: update last seen time and calculate total duration
                    active_tracks[track_id]["last_seen"] = current_time
                    duration = (
                        active_tracks[track_id]["last_seen"]
                        - active_tracks[track_id]["first_seen"]
                    )

                # Assign visual colors based on threat duration
                if duration >= alert_threshold_seconds:
                    # Flashing Red Alert box if target exceeds safety threshold
                    color = (0, 0, 255)
                    label = (
                        f"⚠️ ALERT: {class_name.upper()} #{track_id} ({int(duration)}s)"
                    )
                    # Production Note: Hook up your GPIO alarm or text notifier right here
                else:
                    # Green for safe humans, Blue for vehicles
                    color = (
                        (0, 255, 0) if class_name == "person" else (255, 0, 0)
                    )
                    label = f"{class_name.upper()} #{track_id} ({int(duration)}s)"

                # Render box and dynamic time tag onto screen
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                )

        # 6. MEMORY CLEANUP: Flush lost tracks
        # If an ID is missing from the frame for more than 5 seconds, remove it 
        # so it doesn't cause false positive accumulation if seen much later.
        expired_tracks = []
        for track_id, timestamps in active_tracks.items():
            if track_id not in ids_in_current_frame:
                if current_time - timestamps["last_seen"] > 5.0:
                    expired_tracks.append(track_id)

        for track_id in expired_tracks:
            del active_tracks[track_id]

        # 7. Render output stream
        cv2.imshow("GuardianEye AI - Live Threat Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Test with default camera. Triggers alert if an entity follows for 15 seconds.
    start_security_tracker(video_source=0, alert_threshold_seconds=15)
