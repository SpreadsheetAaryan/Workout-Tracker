# Workout Tracker

A desktop app that counts reps from your webcam and logs workouts. You teach it what the two ends of a movement look like (for example, arm extended and arm contracted in a bicep curl), it trains a small classifier on those frames, and then it counts a rep each time it sees you go from one position to the other.

Built in June 2025 with Python, OpenCV, Tkinter, scikit-learn and SQLite.

## How it works

1. **Collect examples.** With the webcam running, press **Extended** or **Contracted** to save the current frame for that position. Frames are saved as 150x150 grayscale images in folders `1/` and `2/`.
2. **Train.** **Train Model** fits a scikit-learn `LinearSVC` on the raw pixels of those frames. Each frame is augmented with a horizontal flip, a vertical flip and a 90-degree rotation.
3. **Count.** With **Toggle Counting** on, each live frame is classified. A rep is counted once the model has seen both the extended and the contracted position.
4. **Log.** Enter the exercise, sets, reps and date and press **Log Exercise** to save it to a local SQLite database (`fit.db`). **View Workout** shows past entries, and there is a built-in stopwatch for rest periods.

Because the classifier works on raw pixels rather than body keypoints, it is sensitive to lighting, background and where you stand. It works best when you collect a few dozen frames of each position in the same spot you will exercise in. No accuracy numbers have been measured.

## Run it

Requires Python 3.9+ and a webcam.

```bash
git clone https://github.com/SpreadsheetAaryan/Workout-Tracker.git
cd Workout-Tracker
pip install -r requirements.txt
python main.py
```

## Files

```
main.py    entry point
app.py     Tkinter UI, rep-counting logic, SQLite workout log
cam.py     threaded webcam capture
model.py   LinearSVC training and prediction on grayscale frames
```
