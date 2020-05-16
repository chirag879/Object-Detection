# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--SINGLE OBJECT TRACKER--*--*--*--*--*--*--*--*--*--*--*--*--*--*--


# Import Libraries
import cv2

# Function for asking Tracking API from user
def ask_for_tracker():
    print('Hi! Which Tracker API would you like to choose')
    print('Enter 0 for BOOSTING')
    print('Enter 1 for MIL')
    print('Enter 2 for KCF')
    print('Enter 3 for TLD')
    print('Enter 4 for MEDIANFLOW')
    print('Enter 5 for GOTURN')
    print('Enter 6 for MOSSE')
    print('Enter 7 for CSRT')

    choice = input('Select your Choice: ')
    if choice == '0':
        tracker = cv2.TrackerBoosting_create()
    if choice == '1':
        tracker = cv2.TrackerMIL_create()
    if choice == '2':
        tracker = cv2.TrackerKCF_create()
    if choice == '3':
        tracker = cv2.TrackerTLD_create()
    if choice == '4':
        tracker = cv2.TrackerMedianFlow_create()
    if choice == '5':
        tracker = cv2.TrackerGOTURN_create()
    if choice == '6':
        tracker = cv2.TrackerMOSSE_create()
    if choice == '7':
        tracker = cv2.TrackerCSRT_create()

    # Return the tracker
    return tracker

# Tracker
tracker = ask_for_tracker()

# Tracker Name
tracker_name = str(tracker).split()[0][1:]

# Capturing the video
cap = cv2.VideoCapture("vtest.avi")

# Read the first frame
ret, frame = cap.read()

# Select Region Of Interest(ROI)
roi = cv2.selectROI(frame, False)

# Initialize the tracker
ret = tracker.init(frame, roi)

# Loop
while True:

    # Reading the captured video
    ret, frame = cap.read()

    # Update the tracker
    success, roi = tracker.update(frame)

    # roi -> from tuple to int
    (x, y, w, h) = tuple(map(int, roi))

    # Draw rectangles as tracker moves
    if success:

        # On tracking Success
        pts1 = (x, y)
        pts2 = (x+w, y+h)
        cv2.rectangle(frame, pts1, pts2, (255, 0, 255), 3)

    else:

        # On tracking Failure
        cv2.putText(frame, "Fail to track the object",
                    (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    # Display Tracker
    cv2.putText(frame, tracker_name, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    # Display result
    cv2.imshow(tracker_name, frame)

    # Exit with escape(esc) button
    if cv2.waitKey(50) & 0xff == 27:
        break

# Release the capture object & Destroy all the windows
cap.release()
cv2.destroyAllWindows()