import time
import math
import cv2
from ultralytics import YOLO

class BehavioralThreatTracker:
    def __init__(self, video_source=0, alert_thresholds=None):
     
        self.model = YOLO("yolov8n-pose.pt")
        self.cap = cv2.VideoCapture(video_source)
        
     
        self.thresholds = alert_thresholds or {
            "loiter_seconds": 12.0,       
            "pace_box_radius": 80,        
            "hidden_hand_conf": 0.4,      
            "hide_duration_threshold": 3.0 
        }
        
    
        self.memory = {}

    def calculate_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def process_stream(self):
        print("[*] Behavioral AI Security Module Active.")
        print("[*] Monitoring: Loitering, Pacing, and Concealed Hands. Press 'q' to exit.\n")
        
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break

            current_time = time.time()
            
         
            results = self.model.track(
                source=frame, 
                persist=True, 
                tracker="bytetrack.yaml", 
                verbose=False
            )
            
            current_frame_ids = set()

            if results and results[0].boxes and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.cpu().numpy().astype(int)
                
            
                keypoints_data = results[0].keypoints.data.cpu().numpy()

                for box, track_id, keypoints in zip(boxes, track_ids, keypoints_data):
                    current_frame_ids.add(track_id)
                    x1, y1, x2, y2 = map(int, box)
                    centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
                    
                
                    if track_id not in self.memory:
                        self.memory[track_id] = {
                            "first_seen": current_time,
                            "last_position": centroid,
                            "loiter_start": current_time,
                            "hidden_hand_start": None,
                            "threats": set()
                        }
                    
                    track = self.memory[track_id]
                    track["threats"].clear() 

              
                    spatial_drift = self.calculate_distance(centroid, track["last_position"])
                    
                    if spatial_drift > self.thresholds["pace_box_radius"]:
                    
                        track["loiter_start"] = current_time
                        track["last_position"] = centroid
                    else:
                       
                        loiter_duration = current_time - track["loiter_start"]
                        if loiter_duration >= self.thresholds["loiter_seconds"]:
                            track["threats"].add(f"LOITERING ({int(loiter_duration)}s)")

                 
                    left_wrist_conf = keypoints[9][2]
                    right_wrist_conf = keypoints[10][2]
                    
                 
                    hands_hidden = (left_wrist_conf < self.thresholds["hidden_hand_conf"] or 
                                    right_wrist_conf < self.thresholds["hidden_hand_conf"])
                    
                    if hands_hidden:
                        if track["hidden_hand_start"] is None:
                            track["hidden_hand_start"] = current_time
                        else:
                            hidden_duration = current_time - track["hidden_hand_start"]
                            if hidden_duration >= self.thresholds["hide_duration_threshold"]:
                                track["threats"].add("HIDDEN HANDS")
                    else:
                        track["hidden_hand_start"] = None

               
                    if track["threats"]:
                        color = (0, 0, 255) 
                        label = f"⚠️ ALERT #{track_id}: " + " | ".join(track["threats"])
                    else:
                        color = (0, 255, 0) 
                        label = f"Person #{track_id}"

               
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                 
                    for wrist_idx in:
                        hx, hy, h_conf = keypoints[wrist_idx]
                        if h_conf > self.thresholds["hidden_hand_conf"]:
                            cv2.circle(frame, (int(hx), int(hy)), 4, (255, 255, 0), -1)

            expired_tracks = [tid for tid, data in self.memory.items() if tid not in current_frame_ids]
            for tid in expired_tracks:
                del self.memory[tid]

            cv2.imshow("Behavioral AI Threat Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = BehavioralThreatTracker(video_source=0)
    tracker.process_stream()
