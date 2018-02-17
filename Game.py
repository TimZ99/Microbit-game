from microbit import *
import random


class vars():
    stopped = True
    player_x = 0
    player_x_old = 0
    oldRowTime = 0
    currentLevel = 0
    score = 0
    emptyRowNeeded = True
    # [Y-axis player_x [Light status per X-axis player_x]]
    obstacles = [
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]
                 ]
    # [#level [speed, empty row]]
    level = [
             [1000, True],
             [800, True],
             [600, True],
             [400, True],
             [200, True]
             ]


def resetVars():
    # pre-set variables
    vars.stopped = True
    vars.player_x = 0
    vars.player_x_old = 0
    vars.oldRowTime = 0
    vars.currentLevel = 0
    vars.score = 0
    vars.emptyRowNeeded = True
    # [Y-axis player_x [Light status per X-axis player_x]]
    vars.obstacles = [
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]
                 ]
    # [#level [speed, empty row]]
    vars.level = [
             [1000, True],
             [800, True],
             [600, True],
             [400, True],
             [200, True]
             ]


def start():
    resetVars()
    display.scroll("3 2 1")
    vars.stopped = False
    display.set_pixel(0, 4, 9)


def stop(message, failed):
    print(message)
    if failed:
        display.clear()
        sleep(500)
        imgLoop = [
                   Image("00000:00000:00500:00000:00000"),
                   Image("00000:00000:00900:00000:00000"),
                   Image("00000:05550:05950:05550:00000"),
                   Image("00000:09990:09990:09990:00000"),
                   Image("55555:59995:59995:59995:55555"),
                   Image("99999:99999:99999:99999:99999"),
                   Image("00000:00000:00000:00000:00000"),
                   Image("50005:05050:00500:05050:50005"),
                   Image("90009:09090:00900:09090:90009"),
                   Image("50005:05050:00500:05050:50005"),
                   Image("90009:09090:00900:09090:90009"),
                   Image("50005:05050:00500:05050:50005"),
                   Image("90009:09090:00900:09090:90009")
                   ]
        display.show(imgLoop, loop=False, delay=300)
        display.clear()
    display.scroll("Score: " + str(int(vars.score)))
    vars.stopped = True


def checkForWholeRow():
    # if there is an obstacle on every pixel, remove 1 obstacle
    if vars.obstacles[0] == [8, 8, 8, 8, 8]:
        vars.obstacles[0][random.randrange(0, 4)] = 0


def setScore():
    # add halve a point when empty rows are used
    if vars.level[vars.currentLevel][1]:
        vars.score += 1/2
    else:
        vars.score += 1


# level up after score reaches a x amount of points
def setLevel():
    if int(vars.score) % 5 == 0 and vars.score / 5 <= 4:
        vars.currentLevel = int(vars.score / 5)
        print("Current level: " + str(vars.currentLevel))
    if int(vars.score) == 100:
        stop("Auto-stop: Highscore!", False)


# move all the obstacles one pixel down and create new row on top
def moveObstaclesDown():
    # get currect status of pixels
    for y in range(0, 4):
        for x in range(0, 5):
            vars.obstacles[y][x] = display.get_pixel(x, y)
    # insert new row
    vars.obstacles.insert(0, [0, 0, 0, 0, 0])
    # check if level requires empty row
    if vars.level[vars.currentLevel][1]:
        # check if empty row is needed
        if not vars.emptyRowNeeded:
            # set obstacles for new row
            for r in range(0, 5):
                vars.obstacles[0][r] = random.randrange(0, 9, 8)
            # check if the row is playable
            checkForWholeRow()
            # require empty row in next round
            vars.emptyRowNeeded = True
        # keep new row empty
        else:
            # require obstacles in the next row
            vars.emptyRowNeeded = False
    # level doesn't requiere empty rows
    else:
        # set obstacles for new row
        for r in range(0, 5):
            vars.obstacles[0][r] = random.randrange(0, 9, 8)
            # check if the row is playable
            checkForWholeRow()
    # remove rows when passed
    while len(vars.obstacles) >= 6:
        del vars.obstacles[-1]

    # show changes to player
    y = 0
    for row in vars.obstacles[0:4]:
        x = 0
        for col in row:
            display.set_pixel(x, y, col)
            x += 1
        y += 1
        x = 0

    # change score and level is needed
    setScore()
    setLevel()

    # update oldrowTime
    vars.oldRowTime = running_time()


def checkRowTime():
    # check if it's time to add a new row
    if vars.oldRowTime+vars.level[vars.currentLevel][0] <= running_time():
        return True
    else:
        return False


def checkForFail(pos):
    # check if current user player_x is equil to al obstacle
    if vars.obstacles[3][pos] == 8:
        # stop the game
        vars.stopped = True
        return True
    else:
        return False


# keep looping forever
while True:

    # decrease by 1 if button A was pressed and player is not on the edge
    if button_a.was_pressed() and vars.player_x > 0:
        vars.player_x -= 1

    # increase by 1 if button B  was pressed and player is not on the edge
    if button_b.was_pressed() and vars.player_x < 4:
        vars.player_x += 1

    # reset to 0 if you touch pin 0
    if pin0.is_touched():
        print("Start Game")
        start()

    # stop game if you touch pin 2
    if pin2.is_touched():
        stop("Manually stoped", False)

    if vars.stopped:
        # empty display
        display.clear()
        # default pixel to show that the game is operational
        display.set_pixel(2, 2, 9)
    elif checkForFail(vars.player_x):
        stop("Game over!", True)
    elif checkRowTime():
        moveObstaclesDown()
    elif vars.player_x != vars.player_x_old:
        # move users pixel
        display.set_pixel(vars.player_x_old, 4, 0)
        display.set_pixel(vars.player_x, 4, 9)
        vars.player_x_old = vars.player_x
    # avoid hogging all the CPU time / using too much power
    sleep(50)
