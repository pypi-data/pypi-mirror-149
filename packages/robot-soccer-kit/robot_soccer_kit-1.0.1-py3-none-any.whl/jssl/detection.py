import numpy as np
import cv2
import zmq
import time
from .field import Field


class Detection:
    def __init__(self):

        # Publishing server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.set_hwm(1)
        self.socket.bind("tcp://*:7557")

        # ArUco parameters
        self.arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        # arucoParams.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_APRILTAG

        self.arucoItems = {
            # Corners
            0: ['c1', (0, 255, 0)],
            1: ['c2', (0, 255, 0)],
            2: ['c3', (0, 255, 0)],
            3: ['c4', (0, 255, 0)],

            # Green
            4: ['green1', (0, 128, 0)],
            5: ['green2', (0, 128, 0)],

            # Blue
            6: ['blue1', (128, 0, 0)],
            7: ['blue2', (128, 0, 0)],

            # Generic objects
            8: ['obj1', (128, 128, 0)],
            9: ['obj2', (128, 128, 0)],
            10: ['obj3', (128, 128, 0)],
            11: ['obj4', (128, 128, 0)],
            12: ['obj5', (128, 128, 0)],
            13: ['obj6', (128, 128, 0)],
            14: ['obj7', (128, 128, 0)],
            15: ['obj8', (128, 128, 0)],
        }

        # Ball detection parameters (HSV thresholds)
        self.lower_orange = np.array([0, 150, 150])
        self.upper_orange = np.array([25, 255, 255])

        # Detection output
        self.markers = {}
        self.last_updates = {}
        self.ball = None
        self.no_ball = 0
        self.field = Field()

    def detectAruco(self, image, image_debug = None):

        (corners, ids, rejected) = cv2.aruco.detectMarkers(image,
                                                           self.arucoDict,
                                                           parameters=self.arucoParams)

        new_markers = {}

        if len(corners) > 0:
            for (markerCorner, markerID) in zip(corners, ids.flatten()):
                if markerID not in self.arucoItems:
                    continue

                corners = markerCorner.reshape((4, 2))

                # Draw the bounding box of the ArUCo detection
                item = self.arucoItems[markerID][0]

                if item[0] == 'c':
                    self.field.set_corner_position(item, corners)

                if image_debug is not None:
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    itemColor = self.arucoItems[markerID][1]
                    cv2.line(image_debug, topLeft, topRight, itemColor, 2)
                    cv2.line(image_debug, topRight, bottomRight, itemColor, 2)
                    cv2.line(image_debug, bottomRight, bottomLeft, itemColor, 2)
                    cv2.line(image_debug, bottomLeft, topLeft, itemColor, 2)

                    # Compute and draw the center (x, y)-coordinates of the
                    # ArUco marker
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(image_debug, (cX, cY), 4, (0, 0, 255), -1)
                    fX = int((topLeft[0] + topRight[0]) / 2.0)
                    fY = int((topLeft[1] + topRight[1]) / 2.0)
                    cv2.line(image_debug, (cX, cY), (fX, fY), (0, 0, 255), 2)

                    cv2.putText(image_debug, item, (cX-8, cY+4),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, itemColor, 2)

                if self.field.calibrated() and item[0] != 'c':
                    new_markers[item] = self.field.pose_of_tag(corners)
                    self.last_updates[item] = time.time()

        self.field.update_homography(image)
        self.markers = new_markers

    def detectBall(self, image, image_debug):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        
        output = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
        num_labels = output[0]
        stats = output[2]
        centroids = output[3]

        candidates = []
        for k in range(1, num_labels):
            if stats[k][4] > 3:
                candidates.append(list(centroids[k]))
                if len(candidates) > 16:
                    break

        if len(candidates):
            best = None
            bestPx = None
            bestDist = None
            self.no_ball = 0

            for point in candidates:
                if self.field.calibrated():
                    pos = self.field.pos_of_gfx(point)
                else:
                    pos = point

                if self.ball:
                    dist = np.linalg.norm(np.array(pos) - np.array(self.ball))
                else:
                    dist = 0

                if best is None or dist < bestDist:
                    bestDist = dist
                    best = pos
                    bestPx = point

            if image_debug is not None and best:
                cv2.circle(image_debug, (int(bestPx[0]), int(
                    bestPx[1])), 3, (255, 255, 0), 3)

            if self.field.calibrated():
                self.ball = best
        else:
            self.no_ball += 1
            if self.no_ball > 10:
                self.ball = None

    def getDetection(self):
        return {
            'ball': self.ball,
            'markers': self.markers,
            'calibrated': self.field.calibrated(),
            'see_whole_field': self.field.see_whole_field
        }

    def publish(self):
        self.socket.send_json(self.getDetection(), flags=zmq.NOBLOCK)
