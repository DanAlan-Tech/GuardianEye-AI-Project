import time
import cv2
from ultralytics import YOLO


def start_security_tracker(video_source=0, alert_threshold_seconds=15):

    model = YOLO("yolov8n.pt")


    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"[-] Error: Could not open video source {video_source}")
        return


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

   
        results = model.track(
            source=frame,
            tracker="bytetrack.yaml",
            persist=True,
            classes=[0, 2, 7],
            verbose=False,
        )

        ids_in_current_frame = set()

    
        if results and results.boxes and results.boxes.id is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            track_ids = results.boxes.id.cpu().numpy().astype(int)
            class_ids = results.boxes.cls.cpu().numpy().astype(int)

            for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                ids_in_current_frame.add(track_id)
                x1, y1, x2, y2 = map(int, box)
                class_name = model.names[class_id]

           
                if track_id not in active_tracks:
                   
                    active_tracks[track_id] = {
                        "first_seen": current_time,
                        "last_seen": current_time,
                    }
                    duration = 0.0
                else:
                
                    active_tracks[track_id]["last_seen"] = current_time
                    duration = (
                        active_tracks[track_id]["last_seen"]
                        - active_tracks[track_id]["first_seen"]
                    )

          
                if duration >= alert_threshold_seconds:
              
                    color = (0, 0, 255)
                    label = (
                        f"⚠️ ALERT: {class_name.upper()} #{track_id} ({int(duration)}s)"
                    )
               
                else:
                   
                    color = (
                        (0, 255, 0) if class_name == "person" else (255, 0, 0)
                    )
                    label = f"{class_name.upper()} #{track_id} ({int(duration)}s)"

            
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

     
        expired_tracks = []
        for track_id, timestamps in active_tracks.items():
            if track_id not in ids_in_current_frame:
                if current_time - timestamps["last_seen"] > 5.0:
                    expired_tracks.append(track_id)

        for track_id in expired_tracks:
            del active_tracks[track_id]


        cv2.imshow("GuardianEye AI - Live Threat Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    start_security_tracker(video_source=0, alert_threshold_seconds=15)
