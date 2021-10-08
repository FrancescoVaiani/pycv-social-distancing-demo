import math

from . import Face


class PeopleCounter:
    @staticmethod
    def _distance_from_camera_squared(f1: Face, f2: Face):
        """
        Estimates the squared distance between the centroids and the plane parallel to the camera

        Parameters
        ----------
        f1: Face
            Face data of first subject
        f2: Face
            Face data of second subject

        Returns
        -------
        int
            Distance between the centroids on vertical plane squared
        """

        centroid_w_12 = abs(f1.centroid_w - f2.centroid_w)
        centroid_h_12 = abs(f1.centroid_h - f2.centroid_h)
        return pow(centroid_w_12, 2) + pow(centroid_h_12, 2)

    @staticmethod
    def _distance_from_ground_squared(f1: Face, f2: Face):
        """
        Estimates the squared distance between the centroid and the plane parallel to the ground

        Parameters
        ----------
        f1: Face
            Face data of first subject
        f2: Face
            Face data of second subject

        Returns
        -------
        int
            Distance between the centroids on the horizontal plane squared
        """

        return pow(abs(f1.distance - f2.distance), 2)

    @staticmethod
    def distance_in_space(f1: Face, f2: Face):
        """
        Estimates the distance of the two centroids using the pythagorean theorem

        Parameters
        ----------
        f1: Face
            Face data of first subject
        f2: Face
            Face data of second subject

        Returns
        -------
        int
            Distance of the centroids using the pythagorean theorem
        """

        distance_squared = PeopleCounter._distance_from_camera_squared(f1, f2) + PeopleCounter._distance_from_ground_squared(f1, f2)
        return round(math.sqrt(distance_squared), 2)
