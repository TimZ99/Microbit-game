from microbit import *
import random

# pre-set variables
stopped = True
position = 0
oldPosition = 0
oldRowTime = 0
currentLevel = 0
score = 0

# speed, empty row
level = [
         [1000, True],
         # [1000, False],
         [800, True],
         [600, True],
         [400, True],
         [200, True]
         ]
obstacles = [
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]
             ]


def start():
    display.scroll("3 2 1")
    global stopped
    stopped = False
    global position
    position = 0
    global oldPosition
    oldPosition = 0
    global score
    score = 0
    global currentLevel
    currentLevel = 0
    global obstacles
    obstacles = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    display.set_pixel(position, 4, 9)


def failed():
    print("Failed Game")
    global score
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
    display.scroll("Score: " + str(int(score)))
    sleep(500)
    display.scroll(str(int(score)))


def stop():
    print("Stopped Game")
    display.scroll("Score: " + str(int(score)))
    global stopped
    stopped = True


def checkForWholeRow():
    global obstacles

    # if there is an obstacle on every pixel, remove 1 obstacle
    if obstacles[0] == [8, 8, 8, 8, 8]:
        obstacles[0][random.randrange(0, 4)] = 0


def setScore():
    global score
    global level
    global currentLevel

    # add halve a point when empty rows are used
    if level[currentLevel][1]:
        score += 1/2
    else:
        score += 1


# level up after score reaches a x amount of points
def setLevel():
    global score
    global level
    global currentLevel
    if int(score) == 5:
        currentLevel = 1
        print("Level up!")
    elif int(score) == 10:
        currentLevel = 2
        print("Level up!")
    elif int(score) == 15:
        currentLevel = 3
        print("Level up!")
    elif int(score) == 20:
        currentLevel = 4
        print("Level up!")
    elif int(score) == 100:
        stop()
        print("Auto-stop: Highscore!")
    print("Score: "+str(int(score)))


# state of game > boolean is empty row is needed
emptyRow = True


# move all the obstacles one pixel down and create new row on top
def moveOneDown():
    global emptyRow
    global obstacles
    global level
    global currentLevel

    # get currect status of pixels
    for y in range(0, 4):
        for x in range(0, 5):
            obstacles[y][x] = display.get_pixel(x, y)

    # insert new row
    obstacles.insert(0, [0, 0, 0, 0, 0])

    # check if level requires empty row
    if level[currentLevel][1]:
        # check if empty row is needed
        if not emptyRow:
            # set obstacles for new row
            for r in range(0, 5):
                obstacles[0][r] = random.randrange(0, 9, 8)
            # check if the row is playable
            checkForWholeRow()
            # require empty row in next round
            emptyRow = True
        # keep new row empty
        else:
            # require obstacles in the next row
            emptyRow = False
    # level doesn't requiere empty rows
    else:
        # set obstacles for new row
        for r in range(0, 5):
            obstacles[0][r] = random.randrange(0, 9, 8)
            # check if the row is playable
            checkForWholeRow()
    # remove rows when passed
    while len(obstacles) >= 6:
        del obstacles[-1]

    print(obstacles)
    print("Currect position: "+str(position))

    # show changes to player
    y = 0
    for row in obstacles[0:4]:
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
    global oldRowTime
    oldRowTime = running_time()


def checkRowTime():
    global oldRowTime
    global currentLevel
    global level

    # check if it's time to add a new row
    if oldRowTime+level[currentLevel][0] <= running_time():
        return True
    else:
        return False


def checkForFail(pos):
    global obstacles

    # check if current user position is equil to al obstacle
    if obstacles[3][pos] == 8:
        global stopped
        # stop the game
        stopped = True
        return True
    else:
        return False


# keep looping forever
while True:

    # decrease by 1 if button A was pressed
    if button_a.was_pressed():
        position = position - 1

    # increase by 1 if button B  was pressed
    if button_b.was_pressed():
        position = position + 1

    # reset to 0 if you touch pin 0
    if pin0.is_touched():
        print("Start Game")
        start()

    # stop game if you touch pin 2
    if pin2.is_touched():
        stop()

    # stop counter from going less than 0
    if position < 0:
        position = 0

    # stop counter from going more than 4
    if position > 4:
        position = 4

    if stopped:
        # empty display
        display.clear()
        # default pixel to show that the game is operational
        display.set_pixel(2, 2, 9)
    elif checkForFail(position):
        failed()
    elif checkRowTime():
        moveOneDown()
    elif position != oldPosition:
        # move users pixel
        display.set_pixel(oldPosition, 4, 0)
        display.set_pixel(position, 4, 9)
        oldPosition = position
    # avoid hogging all the CPU time / using too much power
    sleep(50)
