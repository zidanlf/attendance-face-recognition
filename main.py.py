import cv2
import face_recognition
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import glob
import csv
import threading
import queue


class FaceAttendance:
    def __init__(self, master):
        self.master = master
        master.title("Face Attendance System")

        # Initialize face recognition
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images("images/")

        # Create GUI elements
        self.label = tk.Label(master, text="Face Attendance System", font=("Arial", 16))
        self.label.pack(pady=10)

        # Video feed label
        self.video_label = tk.Label(master)
        self.video_label.pack(pady=10)

        # Table for attendance records
        self.attendance_tree = ttk.Treeview(master)
        self.attendance_tree["columns"] = ("1", "2", "3")
        self.attendance_tree.column("#0", width=200)
        self.attendance_tree.column("1", width=200)
        self.attendance_tree.column("2", width=200)
        self.attendance_tree.heading("#0", text="Name")
        self.attendance_tree.heading("1", text="Date")
        self.attendance_tree.heading("2", text="Time")
        self.attendance_tree.pack(pady=20)

        # Start button
        self.start_button = tk.Button(master, text="Start Attendance", command=self.start_attendance)
        self.start_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(master, text="Stop Attendance", command=self.stop_attendance, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Initialize camera and attendance list
        self.cap = cv2.VideoCapture(0)
        self.attendance_records = []
        self.attendance_queue = queue.Queue()
        self.is_running = False

        # CSV logging thread
        self.csv_thread = threading.Thread(target=self.csv_logging_worker, daemon=True)
        self.csv_thread.start()

    def start_attendance(self):
        """Start face recognition and record attendance."""
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.detect_faces()

    def detect_faces(self):
        """Detect faces in video stream."""
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Unable to access the camera.")
            return

        # Detect faces
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc

            # Draw rectangle and name
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Record attendance if not already recorded today
            if name != "Unknown" and not self.is_already_recorded(name):
                current_date = datetime.now().strftime("%Y-%m-%d")
                current_time = datetime.now().strftime("%H:%M:%S")
                record = (name, current_date, current_time)
                
                # Add to records and queue for CSV logging
                self.attendance_records.append(record)
                self.attendance_queue.put(record)

                # Add the record directly to the Treeview (GUI)
                self.master.after(0, self.update_treeview, name, current_date, current_time)
                print(f"Recorded: {name}, Date: {current_date}, Time: {current_time}")

        # Convert frame for Tkinter
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=pil_img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Schedule next detection
        self.master.after(10, self.detect_faces)

    def stop_attendance(self):
        """Stop attendance detection."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.video_label.configure(image='')

    def update_treeview(self, name, date, time):
        """Thread-safe method to update Treeview"""
        self.attendance_tree.insert("", "end", text=name, values=(date, time))

    def csv_logging_worker(self):
        """Worker thread for logging attendance to CSV"""
        csv_filename = 'attendance_log.csv'
        
        # Create CSV file with headers if it doesn't exist
        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Name', 'Date', 'Time'])
        
        while True:
            # Wait for new attendance record
            record = self.attendance_queue.get()
            
            # Append to CSV
            try:
                with open(csv_filename, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(record)
                print(f"Logged to CSV: {record}")
            except Exception as e:
                print(f"Error logging to CSV: {e}")
            
            # Mark task as done
            self.attendance_queue.task_done()

    def is_already_recorded(self, name):
        """Check if a name is already recorded today."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        return any(record[0] == name and record[1] == current_date for record in self.attendance_records)


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize factor for faster detection
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """Load and encode all images in the specified directory."""
        image_files = glob.glob(os.path.join(images_path, "*.*"))

        print(f"{len(image_files)} images found for encoding.")

        for img_path in image_files:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Extract the name from the filename
            filename = os.path.splitext(os.path.basename(img_path))[0]
            try:
                encoding = face_recognition.face_encodings(rgb_img)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(filename)
            except IndexError:
                print(f"Warning: No face detected in {img_path}. Skipping this file.")

        print("Encoding complete.")

    def detect_known_faces(self, frame):
        """Detect faces in a frame and match them with known faces."""
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces and compute face encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the closest match if available
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Scale back face locations to match original frame size
        face_locations = (np.array(face_locations) / self.frame_resizing).astype(int)
        return face_locations, face_names


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendance(root)
    root.mainloop()