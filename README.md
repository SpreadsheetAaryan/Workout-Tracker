# Workout Tracker 🏋️‍♂️  
Train, track, and analyze your workouts using computer vision and machine learning.

[![Project Demo](https://img.shields.io/badge/Watch-Demo-red)](https://youtu.be/zd0G3uwaul4?si=89-RomV_qXvx4VIf)

## Description  
This project is a desktop-based workout tracking application built using Python, OpenCV, Tkinter, and SQLite. It allows users to train a machine learning model to recognize specific exercises using pose estimation, then track reps, sets, and workouts in real-time.

The application uses:
- `OpenCV` for capturing and analyzing webcam video.
- `Tkinter` for the user interface.
- `Scikit-learn` with `LinearSVC` for the machine learning model.
- `SQLite` for tracking user workout data persistently.

---

## 🎯 Features

- 🧠 **Train Your Own Exercise Model**: Teach the app to recognize custom workouts by recording your own movements.
- 📈 **Real-Time Rep Counter**: Detect and count reps using webcam input.
- 🗓️ **Workout History Tracking**: View your past workouts, sets, reps, and performance over time.
- 🗄️ **SQL-Backed Persistence**: Store all workouts and user data in a local SQLite database.
- 🖥️ **Simple UI**: Clean and intuitive interface using Tkinter.
- 🎥 **Webcam-Based Feedback**: Get visual cues on form detection while exercising.

---

## 🛠️ Installation and Setup

Follow these steps to get started:

### 1. Clone the Repository
```bash
git clone https://github.com/SpreadsheetAaryan/Workout-Tracker.git
cd Workout-Tracker
pip install -r requirements.txt
python main.py

```
## 📊 How the AI Works

### 🏋️‍♂️ Data Collection
- You can train the app on your own movements (e.g., squats, curls, etc.).
- Pose landmarks are extracted from video frames using OpenCV.

### 📐 Feature Extraction
- Key body point angles and positions are used as features.
- These are labeled according to your exercise (e.g., pushup, squat, curl).

### 🧠 Model Training
- A `LinearSVC` model from `scikit-learn` is trained on your labeled data.
- Model accuracy improves the more data you provide during the training phase.

### 🎯 Real-Time Tracking
- The trained model predicts your exercise form in real-time.
- It counts reps based on movement patterns and posture thresholds.




