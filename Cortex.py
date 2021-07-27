import math
from math import isclose
import time


def main(args):
    res = []
    ev = args["event"] if "event" in args else ""

    x = args["x"]
    y = args["y"]
    ang = args["angle"]
    ang1 = args["tank_angle"]
    ang2 = args["turret_angle"]

    x_size = 486
    y_size = 500

    # costants
    borderDistance = 25
    LAST_STEP = 4
    top_margin = 50
    bot_margin = y_size - 50

    # variables
    X_MEDIAN = x_size / 2
    Y_MEDIAN = y_size / 2
    panel = "left" if x < X_MEDIAN else "right"
    moveDistance = 50

    out_dict = dict()

    # get Panel
    corner = None
    if isInRange(ang1, 0, 90):
        corner = "right_bottom"
    elif isInRange(ang1, 90, 180):
        corner = "left_bottom"
    elif isInRange(ang1, 180, 270):
        corner = "left_top"
    elif isInRange(ang1, 270, 360):
        corner = "right_top"

    # get turret direction RELATIVE TO SHIP
    turret_corner = None
    if isInRange(ang2, 0, 90):
        turret_corner = "right_bottom"
    elif isInRange(ang2, 90, 180):
        turret_corner = "left_bottom"
    elif isInRange(ang2, 180, 270):
        turret_corner = "left_top"
    elif isInRange(ang2, 270, 360):
        turret_corner = "right_top"

    data = args.get("data", dict())
    STEP = args["data"].get("step", 0)

    if ev == "enemy-spot":
        enemy_y = args["enemy_spot"]["y"]
        enemy_x = args["enemy_spot"]["x"]
        enemy_ang = args["enemy_spot"]["angle"]

        seconds = time.time()
        data.update({
            "enemy": {
                "y": enemy_y,
                "x": enemy_x, "ang": enemy_ang,
                "time_sec": seconds}})

    ### SET STATUS
    if STEP == 0:
        if panel == "left" and x > borderDistance \
                or panel == "right" and x < x_size - borderDistance:

            if corner == "left_top" and isclose(ang1, 225) \
                    or corner == "left_bottom" and isclose(ang1, 135) \
                    or corner == "right_bottom" and isclose(ang1, 45) \
                    or corner == "right_top" and isclose(ang1, 315):
                STEP = 1
                data.update({"step": 1})

    if STEP == 1:
        if panel == "left" and x <= borderDistance + 1 \
                or panel == "right" and x >= x_size - borderDistance - 1:
            if corner == "left_top" and isclose(ang1, 225) or corner == "left_bottom" and isclose(ang1,
                                                                                                  135) or corner == "right_bottom" and isclose(
                ang1, 45) or corner == "right_top" and isclose(ang1, 315):
                STEP = 2
                data.update({"step": 2})

    if STEP == 2:
        if panel == "left" and x <= borderDistance + 1 \
                or panel == "right" and x >= x_size - borderDistance - 1:
            if isInRange(ang1, 89, 91) or isInRange(ang1, 269, 271):
                STEP = 3
                data.update({"step": 3})

    if STEP == 3:
        if (panel == "left" and (isInRange(ang, 360 - 2, 360) or isInRange(ang, 0, 2))) \
                or (panel == "right" and (isInRange(ang, 178, 182))):
            STEP = 4
            data.update({"step": 4})

    # STEP 0 ####################################################################
    ##########

    if ev not in ("enemy-spot") and STEP < LAST_STEP:

        if STEP == 0:

            ang_to_rotate, rot_dir = None, None

            if corner == "left_top":
                ang_to_rotate, rot_dir = getShipRotationParamsFromTargetAngle(ang1, 225)

            elif corner == "left_bottom":
                ang_to_rotate, rot_dir = getShipRotationParamsFromTargetAngle(ang1, 135)

            elif corner == "right_top":
                ang_to_rotate, rot_dir = getShipRotationParamsFromTargetAngle(ang1, 315)

            elif corner == "right_bottom":
                ang_to_rotate, rot_dir = getShipRotationParamsFromTargetAngle(ang1, 45)

            if ang_to_rotate:
                out_dict.update({rot_dir: ang_to_rotate})

            ### SHOOT if starting angle is on enemy starting position
            semi_angle = 5
            if (panel == "left" and (isInRange(ang, 360 - semi_angle, 360) or isInRange(ang, 0, semi_angle))) \
                    or (panel == "right" and (isInRange(ang, 180 - semi_angle, 180 + semi_angle))):
                out_dict.update({"shoot": True})

        if STEP == 1:

            if panel == "left":

                dir = "move_backwards"
                if isInRange(ang1, 90, 270):
                    dir = "move_forwards"

                enemy_ang = 0
                turretDir, degree = turretToAbsDegree(ang, enemy_ang)
                out_dict.update({dir: getIpotenusaFromCatetoAndAngoloOpposto(x - borderDistance, 45)})
                out_dict = updateTurretRotation(out_dict, turretDir, degree)

                if isInRange(ang, 360 - 15, 360) or isInRange(ang, 0, 15):
                    out_dict.update({"shoot": True})

            elif panel == "right":

                dir = "move_forwards"
                if isInRange(ang1, 90, 270):  # ???
                    dir = "move_backwards"

                enemy_ang = 180
                turretDir, degree = turretToAbsDegree(ang, enemy_ang)
                out_dict.update({dir: getIpotenusaFromCatetoAndAngoloOpposto(x_size - borderDistance - x, 45)})
                out_dict = updateTurretRotation(out_dict, turretDir, degree)

                if isInRange(ang, 180 - 15, 180 + 15):
                    out_dict.update({"shoot": True})

        if STEP == 2:
            r1 = getShipRotationParamsFromTargetAngle(ang1, 90)
            r2 = getShipRotationParamsFromTargetAngle(ang1, 270)

            r = r1 if r1[0] < r2[0] else r2

            ang_to_rotate = r[0]
            rot_dir = r[1]

            out_dict.update({rot_dir: ang_to_rotate})

            up_down = "up" if y > Y_MEDIAN else "down"

            # Direction depending from last time enemy spot
            if data.get("enemy", False):
                enemy_y = data["enemy"]["y"]
                enemy_y_time = data["enemy"]["time_sec"]
                elapsed_time = time.time() - enemy_y_time

                up_down = "down" if y < enemy_y and elapsed_time < 4 else "up"

            data.update({"up_down": up_down})

        if STEP == 3:

            out_dict = dict()
            absTargetDegree = 0 if panel == "left" else 180

            up_down = "down" if y < Y_MEDIAN else "up"
            moveDistance *= 4

            # Direction depending from last time enemy spot
            if data.get("enemy", False):
                enemy_y = data["enemy"]["y"]
                if isInSamePole(Y_MEDIAN, y, enemy_y):

                    enemy_y_time = data["enemy"]["time_sec"]
                    # elapsed_time = time.time() - enemy_y_time

                    if abs(y - enemy_y) < 60:
                        up_down = invertUpDown(up_down)

                    moveDistance = moveDistance / 8

            # should never reach this point: STEP 4 before wall-collide
            if ev == "wall-collide":
                up_down = invertUpDown(up_down)

                # targetAngle = ang + 90 if ang > 180 else ang - 90

            dir = getParamsToMove(up_down, ang1)

            data.update({"direction": dir, "up_down": up_down})
            out_dict.update({"shoot": True, "yell": "ALL IN MODE!"})
            out_dict = setDir(out_dict, dir, moveDistance)

            turretDir, degree = turretToAbsDegree(ang, absTargetDegree)
            out_dict = updateTurretRotation(out_dict, turretDir, degree)

            out_dict.update(out_dict)

    if STEP == 4:

        out_dict = dict()
        absTargetDegree = 0 if panel == "left" else 180

        turretDir, degree = turretToAbsDegree(ang, absTargetDegree)
        out_dict = updateTurretRotation(out_dict, turretDir, degree)

        up_down = data.get("up_down")

        if ev == "wall-collide":
            up_down = invertUpDown(up_down)

        dir = getParamsToMove(up_down, ang1)

        data.update({"direction": dir, "up_down": up_down})

        # ???
        history = data.get("spotHistory", [])
        if isRecentHistory(history, [0, 0, 0]):
            moveDistance *= 1.5
            out_dict.update({"shoot": True})
            out_dict = setDir(out_dict, dir, moveDistance)
            data.update({"radar": True})

            history.append(7)
            data.update({"spotHistory": history})

        else:
            data.update({"radar": False})
            if data.get("enemy") and abs(data.get("enemy").get("x", 9999) - x) < 80 \
                    and data.get("enemy") and abs(data.get("enemy").get("y", 9999) - y) < 20 \
                    and time.time() - data.get("enemy").get("time_sec", time.time() + 10) < 1:

                out_dict.update({"yell": "FULL FIRE!!!", "shoot": True})


            elif ev == "enemy-spot":
                if True:
                    moveDistance = 50

            out_dict.update({"shoot": True})
            out_dict = setDir(out_dict, dir, moveDistance)
            data.update({"up_down": up_down})

    ### Ending Flow...

    if ev == "enemy-spot" and STEP == 4:

        sh = data.get("spotHistory", [])
        sh.append(1)
        data.update({"spotHistory": sh})

    elif ev not in ("enemy-spot", "hit") and STEP == 4:

        sh = data.get("spotHistory", [])
        sh.append(0)
        data.update({"spotHistory": sh})

    # HISTORY CHECK
    angleH = 20

    if STEP == 4 \
            and (isInRange(ang, 0, angleH) or isInRange(ang, 360 - angleH, 360) or isInRange(ang, 180 - angleH,
                                                                                             180 + angleH)):

        history = data.get("spotHistory", [])

        conditions = ([1, 0],)

        historyConditions = (isRecentHistory(history, c) for c in conditions)

        if any(historyConditions):

            if not (len(history) <= 3 and history[0] == -1):

                data.update({"spotHistory": [-1]})

                up_down = invertUpDown(data.get("up_down", "up"))
                data.update({"up_down": up_down})

                dir = getParamsToMove(up_down, ang1)

                #?
                out_dict.update({"shoot": True})

                out_dict = setDir(out_dict, dir, moveDistance)

        # truncate history
        sh = truncateHistory(data.get("spotHistory", []), 10)
        data.update({"spotHistory": sh})

    ####################################################################################
    # PREPARE OUTPUT JSON

    out_dict.update({"data": data})
    res.append(out_dict)

    if out_dict.get("shoot", False) and STEP==4:
        res.append({"shoot": True})

    return {"body": res}


def changeDir(dir):
    return "move_forwards" if dir == "move_backwards" else "move_backwards"


def invertUpDown(up_down):
    return "up" if up_down == "down" else "down"


def isInRange(n, r1, r2):
    return r1 <= n <= r2


def getShipRotationParamsFromTargetAngle(ang_start, ang_target):
    if ang_start < ang_target:
        return ang_target - ang_start, "turn_right"
    elif ang_start > ang_target:
        return ang_start - ang_target, "turn_left"
    else:
        return 0, None  # ???


def getIpotenusaFromCatetoAndAngoloOpposto(cateto, angOpp):
    angOppRadians = math.radians(angOpp)
    return cateto / math.sin(angOppRadians)


# function to get direction to move "up" or "down"
def getParamsToMove(up_down, ang1):
    direct = "move_forwards"

    if up_down == "up":
        if isInRange(ang1, 89, 91):
            direct = "move_backwards"

    elif up_down == "down":
        if isInRange(ang1, 269, 271):
            direct = "move_backwards"

    return direct


def turretSearch(panel, ang):
    degree = 15

    # PANEL == "LEFT"
    if isInRange(ang, 180, 360):
        right_or_left = "turn_turret_right"
    else:
        right_or_left = "turn_turret_left"

    if panel == "right":
        right_or_left = invertRotation(right_or_left)

    return right_or_left, degree


def turretToAbsDegree(ang_start, ang_target):

    if ang_start < ang_target:
        right_or_left = "turn_turret_right"
    else:
        right_or_left = "turn_turret_left"

    degree = abs(ang_start - ang_target)

    if degree > 180:
        right_or_left = invertRotation(right_or_left)
        degree = 360 - degree

    return right_or_left, degree


def invertRotation(right_or_left):
    return "turn_turret_left" if right_or_left == "turn_turret_right" else "turn_turret_right"


def truncateHistory(listHistory, max_size):
    return listHistory[-max_size:] if listHistory else listHistory


def isRecentHistory(list, sub_list):
    return list[-len(sub_list):] == sub_list


# RETURN: dict with commands
def radar(up_down, panel, ang_start, ang_target):
    # se la nave sale  ruota la torretta 45 verso l'alto, se non lo vede inverti direzione

    ang_target = ang_target % 360

    if panel == "left":
        if up_down == "up":
            right_or_left, degree = turretToAbsDegree(ang_start, 360 - ang_target)
        else:
            right_or_left, degree = turretToAbsDegree(ang_start, ang_target)
    else:
        if up_down == "up":
            right_or_left, degree = turretToAbsDegree(ang_start, 180 - ang_target)
        else:
            right_or_left, degree = turretToAbsDegree(ang_start, 180 + ang_target)

    return right_or_left, degree


def updateTurretRotation(out_dict, right_or_left, degree):
    out_dict.pop("turn_turret_left", None)
    out_dict.pop("turn_turret_right", None)
    out_dict.update({right_or_left: degree})
    return out_dict


def isInSamePole(Y_MEDIAN, y, enemy_y):
    if enemy_y == False:
        return False

    return y > Y_MEDIAN + 10 and enemy_y > Y_MEDIAN + 10 or y < Y_MEDIAN - 10 and enemy_y < Y_MEDIAN - 10

def setDir(out_dict, dir, moveDistance):
    out_dict.pop("move_forwards", None)
    out_dict.pop("move_backwards", None)
    out_dict.update({dir: moveDistance})
    return out_dict