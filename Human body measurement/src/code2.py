import cv2
import numpy as np
import math

refPt = []
metre_pixel_x = 0
metre_pixel_y = 0
window_name1 = "image"

def click_and_crop(event, x, y, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))

def get_distance(image):
    global refPt
    refPt = []

    while True:
        cv2.imshow(window_name1, image)
        if len(refPt) == 2:
            break
        k = cv2.waitKey(1) & 0xFF
    cv2.destroyAllWindows()

    if len(refPt) == 2:
        pixel_dist_y = abs(refPt[0][1] - refPt[1][1])
        pixel_dist_x = abs(refPt[0][0] - refPt[1][0])

        actual_y = metre_pixel_y * pixel_dist_y
        actual_x = metre_pixel_x * pixel_dist_x

        actual_dist = math.sqrt(actual_y**2 + actual_x**2)
        return actual_dist

    return 0

def get_points(img):
    points = []
    img_to_show = img.copy()

    def draw_circle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img_to_show, (x, y), 2, (255, 0, 0), -1)
            points.append((x, y))  # Add the points to the list

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', img.shape[0], img.shape[1])
    cv2.setMouseCallback('image', draw_circle)

    while 1:
        cv2.imshow('image', img_to_show)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    return points

def get_real_world_distance(points, m_x, m_y):
    pixel_dist_y = abs(points[0][1] - points[1][1])
    pixel_dist_x = abs(points[0][0] - points[1][0])
    actual_y = m_y * pixel_dist_y
    actual_x = m_x * pixel_dist_x
    actual_dist = math.sqrt(actual_y**2 + actual_x**2)
    return actual_dist

def measure_waist(image):
    global metre_pixel_x, metre_pixel_y
    # Resize the frame to improve processing speed
    scale_percent = 50  # adjust as needed
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_frame = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    points = get_points(resized_frame)
    if len(points) == 2:
        actual_dist = get_real_world_distance(points, metre_pixel_x, metre_pixel_y)
        return actual_dist
    return 0

# Open a connection to the camera (camera index 0 by default)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Placeholder: Add more code to process the frame or perform measurements
    # Example: Call the function to get the waist measurement
    waist_measurement = measure_waist(frame)

    # Display the frame with measurements
    cv2.putText(frame, f"Waist Measurement: {waist_measurement:.2f} units", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
