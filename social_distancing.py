import sys
import cv2
import argparse
from people_counter import Face, PeopleCounter


def main_loop(calibration: int, threshold: int, output_in_inches: bool = False, camera_index: int = 0, ):
    """
    Main loop of the run process it handles all the cv2 calls, shows a video output and draws alla data on screen.

    Parameters
    ----------
    calibration: int
        The calibration value used to evaluate subject distances
    threshold: int
        Threshold value to trigger alarm
    output_in_inches: Bool
        Used to determine the measure unit
    camera_index: int
        Open CV index of the Camera to use. Usually it is 0

    See Also
    --------
    calibration
        Function to evaluate the calibration value

    """
    measure_unit = "cm"
    if output_in_inches:
        measure_unit = "in"

    # Load the cascade
    frontal_face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    while True:
        try:
            # Read the frame
            _, img = cap.read()
            frontal_faces = detect_faces(img, frontal_face_cascade)
            faces = []

            # Draw the rectangle around each face
            for frontal_face in frontal_faces:
                face = Face(frontal_face, calibration)
                cv2.rectangle(img, (face.x, face.y), (face.x + face.w, face.y + face.h), (0, 255, 0), 2)
                cv2.drawMarker(img, (face.centroid_x, face.centroid_y), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 1, 2,
                               cv2.LINE_AA)
                cv2.putText(img, f"{face.distance} {measure_unit}", (face.x, face.y - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4, cv2.LINE_AA)
                cv2.putText(img, f"{face.distance} {measure_unit}", (face.x, face.y - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                for other_face in faces:
                    # estimate the 3D distance between centroids
                    distance_between_people = PeopleCounter.distance_in_space(face, other_face)

                    if distance_between_people < threshold:
                        cv2.line(img,
                                 (face.centroid_x, face.centroid_y),
                                 (other_face.centroid_x, other_face.centroid_y),
                                 (0, 0, 255),
                                 2,
                                 cv2.LINE_AA)
                        line_center = (int((other_face.centroid_x + face.centroid_x) / 2) - 10,
                                       int((other_face.centroid_y + face.centroid_y) / 2) - 10)
                        cv2.putText(img, f"{distance_between_people} {measure_unit}", line_center,
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 0), 4, cv2.LINE_AA)
                        cv2.putText(img, f"{distance_between_people} {measure_unit}", line_center,
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 255, 255), 2, cv2.LINE_AA)

                faces.append(face)

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


def calibrate(distance: float, camera_index: int = 0):
    """
    Function to calculate the calibration value used to evaluate the subject distance using triangle similarity.

    Parameters
    ----------
    distance: float
        Known distance of the subject from the camera

    camera_index: int
        Open CV index of the Camera to use. Usually it is 0

    Notes
    -----
    The triangle similarity is calculated using the detected subject width in pixel (P), the known width of the
    subject (W) and the known distance from the camera (D) as:

    S = (P * D) / W

    We can use this data to calculate any later distance using the new subject width in pixel (P') as:

    D' = (W * S) / P'

    If we replace S from the previous formula

    D' = (W * ((P * D) / W)) / P'

    If we approximate the width of any subject as similar

    D' = ((W / W) (P * D)) / P' = (P * D) / P'

    So our Calibration number could be defined as

    C = (P * D)  => D' = C / P'

    See Also
    --------
    Face.distance

    """
    # Load the cascade
    frontal_face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    counter = 0
    total = 0

    for counter in range(1, 1001):
        try:
            # Read the frame
            _, img = cap.read()
            frontal_faces = detect_faces(img, frontal_face_cascade)

            for frontal_face in frontal_faces:
                # _, _, w1, _, _, _, _, _ = get_face_data(frontal_face)
                face = Face(frontal_face, None)
                counter += 1
                total += face.w

            if counter % 100 == 0:
                print(f"{counter / 10}%", end="\r", flush=True)
        except KeyboardInterrupt:
            break
    print()
    print(f"{int(round(total * distance / counter)) }")
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    sys.exit()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Social distancing demo")
    subparsers = parser.add_subparsers(dest="operation")

    calibrate_parser = subparsers.add_parser("calibrate", help="Calibrate your camera")
    calibrate_parser.add_argument("--distance", "-d", required=True, type=float,
                                  help="Distance of the calibration face from camera", default=0)
    calibrate_parser.add_argument("--videocameraindex", "-v", required=False, type=int,
                                  help="Video camera index", default=0)
    run_parser = subparsers.add_parser("run", help="Run social distancing demo")
    run_parser.add_argument("--calibrationresult", "-c", required=True, type=int,
                            help="Result from the calibration operation.")
    run_parser.add_argument("--threshold", "-t", required=False, type=int, help="Threshold value to trigger alarm",
                            default=150)
    run_parser.add_argument("--inches", dest="inches", action="store_true")
    run_parser.add_argument("--videocameraindex", "-v", required=False, type=int, help="Video camera index", default=0)

    args = parser.parse_args()

    if args.operation == 'calibrate':
        calibrate(distance=args.distance, camera_index=args.videocameraindex)
    elif args.operation == "run":
        main_loop(calibration=args.calibrationresult,
                  threshold=args.threshold,
                  output_in_inches=args.inches,
                  camera_index=args.videocameraindex)


if __name__ == '__main__':
    parse_arguments()
