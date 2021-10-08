class Face:
    """
    Data object representing the subject face

    Attributes
    ----------
    x: int
        x coordinate of the topmost leftmost point of the face square
    y: int
        y coordinate of the topmost leftmost point of the face square
    w: int
        width the face square
    h: int
        height the face square
    centroid_w: int
        distance of the centroid from the leftmost border of the face square
    centroid_h: int
        distance of the centroid from the topmost border of the face square
    centroid_x: int
        x coordinate of the centroid
    centroid_y: int
        y coordinate of the centroid
    distance: int
        distance of the subject from the camera using triangle similarity
    """

    def __init__(self, cv2_face: tuple, calibration):
        """
        Parameters
        ----------
        cv2_face
            Face data from cv2
        calibration: int
            Value from the calibration function, used to evaluate subject instance

        See Also
        --------
        calibrate
        """
        (self.x, self.y, self.w, self.h) = cv2_face
        (self.centroid_w, self.centroid_h) = (self.w // 2, self.h // 2)
        (self.centroid_x, self.centroid_y) = (self.x + self.centroid_w, self.y + self.centroid_h)
        if calibration:
            self.distance = round(calibration / self.w, 1)
