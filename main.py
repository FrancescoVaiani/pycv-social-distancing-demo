import os
import sys
import cv2
import math
import argparse


def main_loop(calibration: int, camera_index: int = 0):
    # Load the cascade
    frontal_face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    cap = cv2.VideoCapture(camera_index)

    while True:
        try:
            # Read the frame
            _, img = cap.read()
            frontal_faces = detect_faces(img, frontal_face_cascade)

            # Draw the rectangle around each face
            for i in range(len(frontal_faces)):
                x1, y1, w1, h1, centroid_x_1, centroid_y_1, centroid_w_1, centroid_h_1 = get_face_data(frontal_faces[i])
                distance_1 = round(calibration / w1, 1)
                cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                cv2.drawMarker(img, (centroid_x_1, centroid_y_1), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 1, 2,
                               cv2.LINE_AA)
                cv2.putText(img, "{} cm".format(distance_1), (x1, y1 - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4, cv2.LINE_AA)
                cv2.putText(img, "{} cm".format(distance_1), (x1, y1 - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                if i == 0:
                    continue
                for k in range(i):
                    # prendere i dati del volto precedente
                    x2, y2, w2, h2, centroid_x_2, centroid_y_2, centroid_w_2, centroid_h_2 = get_face_data(
                        frontal_faces[k])
                    distance_2 = round(calibration / w2, 1)
                    # trovare distanza dei centroidi sul piano parallelo alla camera
                    centroid_w_12 = abs(centroid_w_1 - centroid_w_2)
                    centroid_h_12 = abs(centroid_h_1 - centroid_h_2)
                    projection_size_squared = pow(centroid_w_12, 2) + pow(centroid_h_12, 2)
                    # trovare distanza tra i centroidi sul piano parallelo al terreno
                    projection_distance_between_people_squared = pow(abs(distance_1 - distance_2), 2)

                    # trovare distanza tridimensionale tra i centroidi
                    distance_between_people = round(
                        math.sqrt(projection_size_squared + projection_distance_between_people_squared), 2)

                    if distance_between_people < 150:
                        cv2.line(img, (centroid_x_1, centroid_y_1), (centroid_x_2, centroid_y_2), (0, 0, 255), 2,
                                 cv2.LINE_AA)
                        line_center = (
                        int((centroid_x_2 + centroid_x_1) / 2) - 10, int((centroid_y_2 + centroid_y_1) / 2) - 10)
                        cv2.putText(img, "{} cm".format(distance_between_people), line_center, cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 0), 4, cv2.LINE_AA)
                        cv2.putText(img, "{} cm".format(distance_between_people), line_center, cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 255, 255), 2, cv2.LINE_AA)

            total = len(frontal_faces)
            print("{} {} detected"
                  .format((str(total) if total > 0 else "No"),
                          ("person" if total == 1 else "people")),
                  end="\r", flush=True)
            cv2.putText(img, str(total), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(img, str(total), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # Display
            cv2.imshow('img', img)
            # Stop if escape key is pressed
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        except KeyboardInterrupt:
            break
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    sys.exit()


def detect_faces(img, frontal_face_cascade):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return frontal_face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )


def get_face_data(face):
    (x, y, w, h) = face
    (centroid_w, centroid_h) = (int(w / 2), int(h / 2))
    (centroid_x, centroid_y) = (x + centroid_w, y + centroid_h)
    return x, y, w, h, centroid_x, centroid_y, centroid_w, centroid_h


def calibrate(camera_index: int = 0):
    # Load the cascade
    frontal_face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    cap = cv2.VideoCapture(camera_index)

    counter = 0
    total = 0

    while True:
        try:
            # Read the frame
            _, img = cap.read()
            frontal_faces = detect_faces(img, frontal_face_cascade)

            # Draw the rectangle around each face
            for i in range(len(frontal_faces)):
                x1, y1, w1, h1, centroid_x_1, centroid_y_1, centroid_w_1, centroid_h_1 = get_face_data(frontal_faces[i])
                counter += 1
                total += w1

            if counter % 100 == 0:
                print(counter)

            if counter == 1000:
                break
        except KeyboardInterrupt:
            break

    print(total / counter)
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    sys.exit()

def parse_arguments():
    parser =argparse.ArgumentParser(description="Social distancing demo")
    subparsers = parser.add_subparsers(dest="operation")

    calibrate_parser = subparsers.add_parser("calibrate", help="Calibrate your camera")
    calibrate_parser.add_argument("--videocameraindex", "-v", required=False, type=int, help="Video camera index", default=0)
    run_parser = subparsers.add_parser("run", help="Run social distancing demo")
    run_parser.add_argument("--calibrationresult", "-c", required=True, type=int, help="Result from the calibration operation. Es.11812")
    run_parser.add_argument("--videocameraindex", "-v", required=False, type=int, help="Video camera index", default=0)

    args = parser.parse_args()

    if args.operation == 'calibrate':
        calibrate(camera_index=args.videocameraindex)
    elif args.operation == "run":
        main_loop(calibration=args.calibrationresult, camera_index=args.videocameraindex)


if __name__ == '__main__':
    try:
        parse_arguments()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
