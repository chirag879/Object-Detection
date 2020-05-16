# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--MULTI OBJECT TRACKER--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--

# To see the tracking first select the object which you want to track then press space and if you want to select
# more items then press space and repeat else press q to see the tracking

# Import required Libraries
import cv2
import sys
from random import randint

# Make a list of tracker types
tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

# Define the function to return the tracker API
def tracker_name(tracker_type):
    if tracker_type == tracker_types[0]:
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type == tracker_types[1]:
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == tracker_types[2]:
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == tracker_types[3]:
        tracker = cv2.TrackerTLD_create()
    elif tracker_type == tracker_types[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type == tracker_types[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_type == tracker_types[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type == tracker_types[7]:
        tracker = cv2.TrackerCSRT_create()

    else:
        tracker = None
        print("No Tracker Found")
        print("Choose from these trackers")
        for tr in tracker_types:
            print(tr)

    # Return the tracker
    return tracker

if __name__ == "__main__":
    print("Default Tracking algorithm is MOSSE \n"
          "Available algorithms are \n")
    for tr in tracker_types:
        print(tr)

    # Initialize the default tracker
    tracker_type = 'MOSSE'

    # Capturing the video
    cap = cv2.VideoCapture("vtest.avi")

    # Reading the first frame
    success, frame = cap.read()

    # Quit if not able to read the frame
    if not success:
        print("Cannot read the video")

    # Initialize boxes and colors with blank arrays
    rects = []
    colors = []

    # Loop
    while True:

        # Draw rectangles, select region of interest(roi) from a new window
        rect_box = cv2.selectROI('Multi-tracking', frame, False)
        rects.append(rect_box)
        colors.append((randint(64, 255), randint(64, 255)))
        print("Press q to stop selecting boxes and start multi-tracking")
        print("Press space key to select another box")

        # For closing the window
        if cv2.waitKey(0) & 0xff == ord('q'):
            break

    # Print the selected ROIs
    print(f'Selected boxes{rects}')

    # Create Multi-Tracker
    multitracker = cv2.MultiTracker_create()

    # Initialize Multi-tracker
    for rect_box in rects:
        multitracker.add(tracker_name(tracker_type), frame, rect_box)

    # Video & tracker
    # Loop
    while cap.isOpened():

        # Reading the video frames
        ret, frame = cap.read()

        # Update location objects
        success, boxes = multitracker.update(frame)

        # Draw the tracked objects
        for i, newbox in enumerate(boxes):
            pts1 = (int(newbox[0]), int(newbox[1]))
            pts2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, pts1, pts2, colors[i], 2, 1)

        # Display frame
        cv2.imshow('Multiracker', frame)

        # Close the frame
        if cv2.waitKey(20) & 0xff == 27:
            break

# Release the capture object & Destroy all the windows
cap.release()
cv2.destroyAllWindows()