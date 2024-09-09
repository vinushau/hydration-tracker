# Hydration Tracker

## Description

**Hydration Tracker** is a Python-based computer vision project that helps users monitor their water intake by detecting sips through the webcam. It tracks the number of sips and reminds users to drink water at regular intervals to ensure they stay hydrated. This tool aims to promote healthy hydration habits by providing visual reminders and sound alerts.

## Features

- Detects sips of water using the camera.
- Tracks total sips and the estimated water volume consumed.
- Provides customizable reminder intervals (default: every 12 minutes) with sound notifications.
- Displays reminder messages on the video feed.
- Allows users to track hydration goals (default: 5 sips/hour).
- Real-time updates on the camera feed for time since the last sip and sip count.

## How It Works

- The program captures video input through your webcam.
- It uses circle detection to identify sips of water based on a cup's shape.
- When a sip is detected, a bell sound is played, and the sip count is updated.
- If no sip is detected within the reminder interval, a notification sound is played, and a reminder message appears on the screen.
- The program can be minimized and will still run in the background.
- Press `ESC` to exit the program.

## How To Run

1. Clone the repository to your local machine.

2. Navigate to the project directory:

   ```bash
   cd hydration-tracker
   ```

3. Install the required dependencies:

   ```bash
   pip install opencv-python numpy pygame
   ```

4. To run the program, execute the following command:

   ```bash
    python main.py
   ```

## Requirements

- Ensure that you have a webcam built into or connected to your computer.
- Make sure you have the sound files (`tone-beep.wav` and `ding.wav`) in the same directory as main.py. The sound files are already included in the repository.

## Computer Vision Usage

### Real-Time Video Capture:
- The program uses OpenCV to capture video from your webcam. This is done using `cv2.VideoCapture(0)`, which accesses the first connected camera.
- The video feed is processed frame by frame, allowing the program to analyze each frame for relevant visual data.

### Image Processing:
- Each video frame is converted to grayscale using `cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)` to simplify the image. Detecting circles is easier in a single color channel (grayscale) than in full color.
- OpenCV's `cv2.HoughCircles()` function is used to detect circles in the grayscale image. This function uses a technique called the **Hough Circle Transform** to find circular shapes based on edge detection.

### Sip Detection:
- The program looks for circles with a radius smaller than 50 pixels, which corresponds to the bottom of a water bottle or cup as seen by the camera.
- Once a circle of this size is detected, the program assumes that a sip of water has been taken. It then updates the count of sips and the total volume of water consumed.

### Visual and Audio Feedback:
- When a sip is detected, the program:
  - Prints a message in the console.
  - Plays a sound.
  - Visually overlays text on the video feed to show the current sip count, seconds since last water sip, and the drinking goal.

## Customization

- Modify the `reminder_interval` variable to set a custom time between reminders.
- Update the `sips_goal_per_hour` variable to set your personal hydration goal.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits

- **tone-beep.wav** by pan14 – [Attribution 4.0](https://freesound.org/s/263133/)
- **ding.wav** by tim.kahn – [Attribution 4.0](https://freesound.org/s/91926/)
