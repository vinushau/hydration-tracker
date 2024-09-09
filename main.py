import cv2
import time
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Suppress Pygame's welcome message
import pygame 

# Initialize pygame mixer
pygame.mixer.init()

# tone-beep.wav by pan14 -- https://freesound.org/s/263133/ -- License: Attribution 4.0
sip_sound = pygame.mixer.Sound('tone-beep.wav') 
# ding.wav by tim.kahn -- https://freesound.org/s/91926/ -- License: Attribution 4.0
reminder_sound = pygame.mixer.Sound('ding.wav') 

# Prints welcome message to the user in the console
def print_welcome_message():
    message = """
    ==================================================
    Welcome to the Hydration Tracker!
    ==================================================

    This program helps you track your water intake by detecting sips through your camera.
    It will monitor your drinking habits and remind you to drink water regularly. Run this
    program as you do your regular day-to-day activies or work on your computer to remind you
    to drink water.

    Here's some background info:
    - The recommended water intake is about 2 liters per day for the average adult.
    - To maintain good hydration, the program will track your sips and aim for 5 sips/hour (1 sip every 12 mins).

    How it works:
    - The program detects sips using your computer's camera.
    - When a sip of water is detected, you will hear a bell sound.
    - If no sip is detected for 12 minutes, you'll hear a notification sound and a reminder message will be displayed.
    - If you work on your computer, you can minimze the video window and the program will still function as normal.
    - Press 'ESC' to exit the program at any time.

    Tips: 
    - To improve sip detection, make sure you are under good lighting for your camera.
    - It is preffered to have decent webcam quality and a solid/clean background to avoid errors.

    Stay hydrated!

    ==================================================
    """
    print(message)

# Initialize video capture and variables
cap = cv2.VideoCapture(0)
sip = 0 # Total number of sips
total_volume = 0 # Total ml of water consumed
sip_volume = 20  # Estimated volume per sip (in ml)
initialTime = int(time.time())
timeSinceSip = 0 
reminder_interval = 720  # Reminder every 12 mins
sips_goal_per_hour = 5  # Goal: 5 sips per hour

# Timer for the reminder
last_reminder_time = int(time.time())

# Flag for the reminder sound
played_reminder_sound = False

# Print the welcome message
print_welcome_message()

while True:
    # Capture the current frame
    _, frame = cap.read()
    actualTime = int(time.time())
    timeSinceSip = actualTime - initialTime
    timeSinceLastReminder = actualTime - last_reminder_time

    image = frame.copy() # Copy frame for processing

    # Convert to grayscale for circle detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use HoughCircles to detect circles (bottom of the water cup) in the grayscale image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

    # Detect circles (sips) and track water intake
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            if r < 50 and timeSinceSip > 6:  # Bottom of water cup detected (small circle of 50px)
                sip += 1
                total_volume += sip_volume  # Update total volume
                initialTime = int(time.time())  # Reset time since last sip
                print(f"Sip detected! You drank {sip} sip(s) and consumed {total_volume} ml of water.")
                
                # Check if the user has reached the sip goal for the hour
                if sip % sips_goal_per_hour == 0 and sip != 0:
                    print(f"Goal of {sips_goal_per_hour} sips per hour reached! Keep it up!")

                sip_sound.play()

                # Reset reminder timer when a sip is detected
                last_reminder_time = int(time.time())
                played_reminder_sound = False  # Reset reminder sound flag

    # Check if reminder needs to be displayed
    if timeSinceLastReminder >= reminder_interval:
        reminder_message = (f"Time to drink water! It's been {timeSinceLastReminder} seconds. ")
        cv2.putText(image, reminder_message, (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (68, 68, 239), 2)
        
        # Play reminder sound if it hasn't been played recently
        if not played_reminder_sound:
            reminder_sound.play()
            played_reminder_sound = True
    else:
        played_reminder_sound = False  # Reset flag if within reminder interval

    # Display the frame with information
    fps_label = (f"Total sips: {sip}, Goal: {sips_goal_per_hour} sips per hour, "
                 f"Time since last sip: {timeSinceSip}s")
    cv2.putText(image, fps_label, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
    cv2.putText(image, fps_label, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (252, 243, 165), 2)

    # Show the reminder message if the time since the last sip exceeds the reminder interval
    if timeSinceLastReminder >= reminder_interval:
        cv2.putText(image, reminder_message, (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (68, 68, 239), 2)

    # Display the frame with information
    cv2.imshow("Hydration Tracker", image)

    # Exit loop when ESC key is pressed
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the video capture, close OpenCV windows, and close pygame
cap.release()
cv2.destroyAllWindows()
pygame.quit()
