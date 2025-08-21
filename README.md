# Face Attendance System

Sistem absensi berbasis pengenalan wajah menggunakan OpenCV dan face_recognition library. Aplikasi ini dapat mendeteksi wajah secara real-time melalui webcam dan secara otomatis mencatat kehadiran ke dalam file CSV dengan antarmuka GUI yang user-friendly.

## 🚀 Features

- Real-time face detection dan recognition menggunakan webcam
- GUI berbasis Tkinter dengan video feed langsung
- Automatic attendance logging ke file CSV
- Multi-threading untuk performa optimal
- Pencegahan duplikasi record harian
- Live attendance table display
- Support untuk multiple face encodings
- Error handling dan logging comprehensive

## 📋 Requirements

### System Requirements
- Python 3.7+
- Webcam/Camera device
- Minimum 4GB RAM
- Windows/Linux/macOS

### Python Libraries
```bash
pip install opencv-python face-recognition numpy pillow tkinter
```

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone [repository-url]
cd face-attendance-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Face Images
```bash
mkdir images
# Add face images to images/ directory
# Format: person_name.jpg (e.g., john_doe.jpg, jane_smith.jpg)
```

## 📁 Project Structure

```
face-attendance-system/
│
├── main.py                    # Main application file
├── images/                    # Directory for face images
│   ├── person1.jpg
│   ├── person2.jpg
│   └── ...
├── attendance_log.csv         # Generated attendance records
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

## 🚀 Usage

### 1. Add Face Images
- Place clear face images in the `images/` directory
- Name format: `firstname_lastname.jpg` or `employee_id.jpg`
- Ensure good lighting and clear face visibility
- One face per image for best results

### 2. Run Application
```bash
python main.py
```

### 3. Using the Interface
1. Click **"Start Attendance"** to begin face detection
2. Position faces in front of the camera
3. System will automatically detect and record attendance
4. View real-time attendance in the table
5. Click **"Stop Attendance"** to pause detection

## 📊 Features Detail

### Face Recognition Engine
- **Detection Algorithm**: face_recognition library with dlib backend
- **Encoding Method**: 128-dimensional face embeddings
- **Matching Threshold**: Configurable distance-based matching
- **Performance Optimization**: Frame resizing for faster processing

### Attendance System
- **Duplicate Prevention**: One record per person per day
- **CSV Logging**: Automatic background logging with threading
- **Real-time Display**: Live updates in GUI table
- **Data Format**: Name, Date (YYYY-MM-DD), Time (HH:MM:SS)

### GUI Components
- **Video Feed**: Real-time camera display with face detection overlay
- **Attendance Table**: Live view of recorded attendance
- **Control Buttons**: Start/Stop functionality
- **Status Indicators**: Visual feedback for system state

### Configuration Parameters
- **Camera Index**: Change camera source in `cv2.VideoCapture(0)`
- **Detection Sensitivity**: Adjust face_distance threshold
- **UI Theme**: Customize Tkinter styling
- **File Formats**: Modify CSV output format

## 📝 CSV Output Format

```csv
Name,Date,Time
john_doe,2024-01-15,09:30:25
jane_smith,2024-01-15,09:31:10
```
## 📧 Contact

- Email: zidannalfarizi@gmail.com
- GitHub: [zidanlf](https://github.com/zidanlf)
- LinkedIn: [Zidan Alfarizi](www.linkedin.com/in/zidanalfarizi)
