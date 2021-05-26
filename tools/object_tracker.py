import math
import cv2


class ObjectTracker:

    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 1

    def get_point(self, detection_boxes):
        x = detection_boxes[0]
        y = detection_boxes[1]
        return x, y

    def track_inside_field(self, result_frame, classes, scores, detection_boxes, field_contour):

        # Player
        player_index = [index for index, object_class in enumerate(classes) if object_class == 0]
        playersBoxes = detection_boxes[player_index]

        players_inside_field = []

        for playerBox in playersBoxes:

            x, y, w, h, = playerBox
            playerLeftUp = (x, y)

            player_inside_field = int(cv2.pointPolygonTest(field_contour, playerLeftUp, True))
            if player_inside_field >= 0:
                players_inside_field.append(playerBox)

        objects_bbs_ids = self.update(players_inside_field)

        return objects_bbs_ids

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object\
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)

                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()

        # return index players missing
        # objects_bbs_ids = self.give_me_back(objects_bbs_ids)

        return objects_bbs_ids

    def give_me_back(self, objects_bbs_ids):

        index_players = []

        for object in objects_bbs_ids:
            x, y, w, h, index_player = object

            index_players.append(index_player)
            index_missing = self.who_missing(index_players)

        for object in objects_bbs_ids:
            x, y, w, h, index_player = object
            if index_player > 4:
                object[4] = index_missing
            print(index_missing)

        return objects_bbs_ids

    def who_missing(self, index_players):
        if 1 not in index_players:
            return 1
        if 2 not in index_players:
            return 2
        if 3 not in index_players:
            return 3
        if 4 not in index_players:
            return 4
