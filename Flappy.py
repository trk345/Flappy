from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math, random

W_Width, W_Height = 500, 500

press_space = False  # to check if spacebar is pressed to start the game
temp = 0  # to store last upper pipe's horizontal part index
score = 0
pause = False  # for pause button
pipe_count = 0  # upper/lower pipe list's right vertical part index
lost = False
lost_upper_horizontal = False  # bird collision with upper pipe's horizontal part
lost_lower_horizontal = False  # bird collision with lower pipe's horizontal part
game_start_bird = False  # if false, will draw the bird
bird_up_speed = 40  # how much upward the bird will go when up arrow key is pressed
bird_down_speed = 6  # how much the bird goes down due to gravity
up_pressed = False
bird_radius = 12
bird_c = []  # bird coordinates
bird_eye = []  # bird's eye's coordinates
bird_beak = []  # bird's beak's coordinates
bird_wing = []
game_start_pipe = False
pipe_speed = 3  # speed at which pipes move left
pipe_width = 50
gap = 150  # distance between upper and lower pipes
d_b_p = 150  # distance between two side-by-side pipes
x_start = 350  # from where the first pipe will start
upper_pipes = []  # list of upper pipes' coordinates
lower_pipes = []  # list of lower pipes' coordinates
yrandom = []  # list of randomly generated y coordinates for pipes' horizontal parts

for i in range(5):  # create 5 pipes initially; this allows the game to run with a good speed
    yrandom.append(random.randint(-75, 245))
print('Press SPACE to Start')


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def draw_points(x, y, s, c1, c2, c3):
    glColor3f(c1, c2, c3)
    glPointSize(s)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


def draw_circle(r):
    cd = []
    x = r
    y = 0
    d = 1 - r
    while y <= x:
        if d < 0:
            d += 2 * y + 3
            y += 1
        else:
            d += 2 * y - 2 * x + 5
            y += 1
            x -= 1

        cd.append([x, y])
        cd.append([y, x])
        cd.append([-y, x])
        cd.append([-x, y])
        cd.append([-x, -y])
        cd.append([-y, -x])
        cd.append([y, -x])
        cd.append([x, -y])
    return cd


def findzone(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    if abs(dy) > abs(dx):
        if dy > 0 and dx >= 0:
            return 1
        elif dy > 0 and dx <= 0:
            return 2
        elif dy < 0 and dx <= 0:
            return 5
        else:
            return 6
    else:
        if dy >= 0 and dx > 0:
            return 0
        elif dy >= 0 and dx < 0:
            return 3
        elif dy <= 0 and dx < 0:
            return 4
        else:
            return 7


def drawline(x1, y1, x2, y2):
    zone = findzone(x1, y1, x2, y2)
    # print(zone)

    # Backward Map:
    if zone == 0:
        x1, x2 = x1, x2
        y1, y2 = y1, y2
    elif zone == 1:
        temp1, temp2 = x1, x2
        x1, x2 = y1, y2
        y1, y2 = temp1, temp2
    elif zone == 2:
        temp1, temp2 = x1, x2
        x1, x2 = y1, y2
        y1, y2 = -temp1, -temp2
    elif zone == 3:
        x1, x2 = -x1, -x2
        y1, y2 = y1, y2
    elif zone == 4:
        x1, x2 = -x1, -x2
        y1, y2 = -y1, -y2
    elif zone == 5:
        temp1, temp2 = x1, x2
        x1, x2 = -y1, -y2
        y1, y2 = -temp1, -temp2
    elif zone == 6:
        temp1, temp2 = x1, x2
        x1, x2 = -y1, -y2
        y1, y2 = temp1, temp2
    else:
        x1, x2 = x1, x2
        y1, y2 = -y1, -y2

    # print(x1,y1,x2,y2)
    dx = x2 - x1
    dy = y2 - y1
    # print(dy,dx)
    coordinates = []
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    # print(x1,x2)

    for x in range(int(x1), int(x2 + 1)):
        coordinates.append([x, y1])
        if d > 0:
            d = d + incNE
            # x += 1
            y1 += 1
        else:
            # x += 1
            d = d + incE
    # print(coordinates)

    # Forward Map:
    pixel = []
    for i in range(len(coordinates)):
        if zone == 0:
            x = coordinates[i][0]
            y = coordinates[i][1]
        elif zone == 1:
            x = coordinates[i][1]
            y = coordinates[i][0]
        elif zone == 2:
            x = -coordinates[i][1]
            y = coordinates[i][0]
        elif zone == 3:
            x = -coordinates[i][0]
            y = coordinates[i][1]
        elif zone == 4:
            x = -coordinates[i][0]
            y = -coordinates[i][1]
        elif zone == 5:
            x = -coordinates[i][1]
            y = -coordinates[i][0]
        elif zone == 6:
            x = coordinates[i][1]
            y = -coordinates[i][0]
        elif zone == 7:
            x = coordinates[i][0]
            y = -coordinates[i][1]

        pixel.append([x, y])
        # draw_points(x,y,s,c1,c2,c3)
        # draw_points(x,y,s)
    return pixel  # returns list of the line's coordinates


def bird():
    global bird_c, bird_eye, bird_beak, bird_wing, game_start_bird
    s = 3
    c1, c2, c3 = 1.0, 1.0, 0.0
    if game_start_bird == False:
        bird_c = draw_circle(bird_radius)
        bird_eye = draw_circle(3)
        bird_beak = draw_circle(2)
        wing_1 = drawline(-2, 0, -13, 12)
        wing_2 = drawline(-7, 0, -13, 12)
        bird_wing.append(wing_1)
        bird_wing.append(wing_2)

        game_start_bird = True

    for i in range(len(bird_c)):
        draw_points(bird_c[i][0], bird_c[i][1], s, c1, c2, c3)
    for i in range(len(bird_eye)):
        draw_points(bird_eye[i][0] + 5, bird_eye[i][1] + 5, s, 1.0, 1.0, 1.0)
    for i in range(len(bird_beak)):
        draw_points(bird_beak[i][0] + 15, bird_beak[i][1], s, 1.0, 0.0, 0.0)
    for i in range(len(bird_wing)):
        for j in range(len(bird_wing[i])):
            draw_points(bird_wing[i][j][0], bird_wing[i][j][1], 2, 1.0, 1.0, 1.0)


def pipes():
    # upper_pipes = [[[x,y],[x,y]...], [[x,y],[x,y]...], [[x,y],[x,y]...], ............]
    #                 horizontal        left_vertical     right_vertical hori, left, right, ....
    # lower_pipes same structure as upper_pipes
    global game_start_pipe, need_pipe, x_start, upper_pipes, lower_pipes
    s = 5  # pixel size
    c1, c2, c3 = 0.0, 0.8, 0.0  # pixel 3f color
    if game_start_pipe == False:
        for i in range(len(yrandom)):
            # for upper pipes
            upper_pipes.append(
                drawline(x_start, yrandom[i], x_start + pipe_width, yrandom[i]))  # horizontal part of pipe
            upper_pipes.append(drawline(x_start + 5, yrandom[i], x_start + 5, 250))  # left vertical part of pipe
            upper_pipes.append(drawline(x_start + pipe_width - 5, yrandom[i], x_start + pipe_width - 5,
                                        250))  # right vertical part pipe

            # for lower_pipes
            lower_pipes.append(
                drawline(x_start, yrandom[i] - gap, x_start + pipe_width, yrandom[i] - gap))  # horizontal part of pipe
            lower_pipes.append(drawline(x_start + 5, yrandom[i] - gap, x_start + 5, -250))  # left vertical part of pipe
            lower_pipes.append(drawline(x_start + pipe_width - 5, yrandom[i] - gap, x_start + pipe_width - 5,
                                        -250))  # right vertical part pipe

            x_start += pipe_width + d_b_p

        # print('start:',x_start)

        game_start_pipe = True

    for i in range(len(yrandom * 3)):  # yrandom*3 because len(upper_pipes) & len(lower_pipes) == len(yrandom)*3
        for j in range(0, len(upper_pipes[i])):
            draw_points(upper_pipes[i][j][0], upper_pipes[i][j][1], s, c1, c2, c3)

        for j in range(0, len(lower_pipes[i])):
            draw_points(lower_pipes[i][j][0], lower_pipes[i][j][1], s, c1, c2, c3)


def pipe():
    global x_start, upper_pipes, lower_pipes, need_pipe

    x_start = upper_pipes[-3][0][0] + pipe_width + d_b_p
    yrandom.append(random.randint(-100, 180))
    # print('here:',x_start)

    upper_pipes.append(drawline(x_start, yrandom[-1], x_start + pipe_width, yrandom[-1]))  # horizontal part of pipe
    upper_pipes.append(drawline(x_start + 5, yrandom[-1], x_start + 5, 250))  # left vertical part of pipe
    upper_pipes.append(
        drawline(x_start + pipe_width - 5, yrandom[-1], x_start + pipe_width - 5, 250))  # right vertical part pipe

    # for lower_pipes
    lower_pipes.append(
        drawline(x_start, yrandom[-1] - gap, x_start + pipe_width, yrandom[-1] - gap))  # horizontal part of pipe
    lower_pipes.append(drawline(x_start + 5, yrandom[-1] - gap, x_start + 5, -250))  # left vertical part of pipe
    lower_pipes.append(drawline(x_start + pipe_width - 5, yrandom[-1] - gap, x_start + pipe_width - 5,
                                -250))  # right vertical part pipe


def navbar():
    # backarrow
    b1 = drawline(-235, 230, -220, 245)
    b2 = drawline(-235, 230, -220, 215)
    b3 = drawline(-235, 230, -205, 230)
    for i in range(len(b1)):
        draw_points(b1[i][0], b1[i][1], 2, 0.1, 0.7, 0.8)
    for i in range(len(b2)):
        draw_points(b2[i][0], b2[i][1], 2, 0.1, 0.7, 0.8)
    for i in range(len(b3)):
        draw_points(b3[i][0], b3[i][1], 2, 0.1, 0.7, 0.8)

    # play/pause
    if pause == True:
        p1 = drawline(-10, 245, -10, 215)
        p2 = drawline(-10, 245, 20, 230)
        p3 = drawline(-10, 215, 20, 230)
        for i in range(len(p1)):
            draw_points(p1[i][0], p1[i][1], 2, 0.9, 0.7, 0.0)
        for i in range(len(p2)):
            draw_points(p2[i][0], p2[i][1], 2, 0.9, 0.7, 0.0)
        for i in range(len(p3)):
            draw_points(p3[i][0], p3[i][1], 2, 0.9, 0.7, 0.0)

    else:
        p1 = drawline(-5, 245, -5, 215)
        p2 = drawline(5, 245, 5, 215)
        for i in range(len(p1)):
            draw_points(p1[i][0], p1[i][1], 2, 0.9, 0.7, 0.0)
        for i in range(len(p2)):
            draw_points(p2[i][0], p2[i][1], 2, 0.9, 0.7, 0.0)

    # cross
    c1 = drawline(205, 245, 235, 215)
    c2 = drawline(205, 215, 235, 245)
    for i in range(len(c1)):
        draw_points(c1[i][0], c1[i][1], 2, 1.0, 0.0, 0.0)
    for i in range(len(c2)):
        draw_points(c2[i][0], c2[i][1], 2, 1.0, 0.0, 0.0)


def keyboardListener(key, x, y):
    global press_space
    if key == b' ':
        press_space = True
    # if key == b's':
    #     pass
    # if key==b's':
    #    print(3)
    # if key==b'd':
    #     print(4)

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global bird_c, bird_eye, bird_beak, bird_wing

    if key == GLUT_KEY_UP and press_space == True and lost == False and pause == False and bird_c[1][1] < 245:
        for i in range(len(bird_c)):
            bird_c[i][1] += bird_up_speed
        for i in range(len(bird_eye)):
            bird_eye[i][1] += bird_up_speed
        for i in range(len(bird_beak)):
            bird_beak[i][1] += bird_up_speed
        for i in range(len(bird_wing)):
            for j in range(len(bird_wing[i])):
                bird_wing[i][j][1] += bird_up_speed

    # if key == GLUT_KEY_DOWN:  # // down arrow key
    #     speed /= 2
    #     print("Speed Decreased")
    glutPostRedisplay()
    # if key==GLUT_KEY_RIGHT:

    # if key==GLUT_KEY_LEFT:

    # if key==GLUT_KEY_PAGE_UP:

    # if key==GLUT_KEY_PAGE_DOWN:

    # case GLUT_KEY_INSERT:
    #
    #
    # case GLUT_KEY_HOME:
    #
    # case GLUT_KEY_END:
    #


def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    global score, pause, lost, lost_upper_horizontal, lost_lower_horizontal
    global game_start_pipe, game_start_bird, x_start, pipe_count, press_space
    global bird_c, bird_eye, bird_beak, bird_wing, upper_pipes, lower_pipes, yrandom

    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):  # // 2 times?? in ONE click? -- solution is checking DOWN or UP
            c_x, c_y = convert_coordinate(x, y)
            # restart
            if -235 <= c_x <= -205 and 215 <= c_y <= 245:
                press_space = False
                lost = False
                pause = False
                lost_upper_horizontal = False
                lost_lower_horizontal = False
                game_start_bird = False
                game_start_pipe = False
                upper_pipes = []
                lower_pipes = []
                bird_c = []
                bird_beak = []
                bird_eye = []
                bird_wing = []
                x_start = 350
                score = 0
                pipe_count = 0
                yrandom = []  # list of randomly generated y coordinates
                for i in range(5):
                    yrandom.append(random.randint(-75, 245))
                print("Starting over!")
                print("Press SPACE to Start")


            # pause
            elif -10 <= c_x <= 20 and 215 <= c_y <= 245:
                if press_space == True:
                    if pause == False:
                        pause = True
                    else:
                        pause = False

            # exit
            elif 205 <= c_x <= 235 and 215 <= c_y <= 245:
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()

    # if button == GLUT_RIGHT_BUTTON:
    #     if state == GLUT_DOWN:

    # case GLUT_MIDDLE_BUTTON:
    #     //........

    glutPostRedisplay()


def display():
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0);  # //color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # //load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # //initialize the matrix
    glLoadIdentity()
    # //now give three info
    # //1. where is the camera (viewer)?
    # //2. where is the camera looking?
    # //3. Which direction is the camera's UP direction?
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    navbar()
    pipes()
    bird()

    glutSwapBuffers()


def animate():
    # //codes for any changes in Models, Camera
    glutPostRedisplay()
    global score, lost, lost_upper_horizontal, lost_lower_horizontal, bird_c, bird_eye, bird_beak, bird_wing
    global pipe_count, x_start, yrandom, upper_pipes, lower_pipes, need_pipe, temp, press_space

    if press_space == True and lost == False and pause == False:
        for i in range(len(bird_c)):
            bird_c[i][1] -= bird_down_speed
        for i in range(len(bird_eye)):
            bird_eye[i][1] -= bird_down_speed
        for i in range(len(bird_beak)):
            bird_beak[i][1] -= bird_down_speed
        for i in range(len(bird_wing)):
            for j in range(len(bird_wing[i])):
                bird_wing[i][j][1] -= bird_down_speed
        if bird_c[5][1] <= -245:
            lost = True

        for i in range(0, (len(yrandom) * 3)):
            for j in range(0, len(upper_pipes[i])):
                upper_pipes[i][j][0] -= pipe_speed

            for j in range(0, len(lower_pipes[i])):
                lower_pipes[i][j][0] -= pipe_speed

            if (i + 1) % 3 == 0 and upper_pipes[i][0][0] < -290:  # if a pipe's right vertical part
                # goes to the left side of the screen, destroy it (pop) and create a new one (append)
                # i+1 to make the index of right vert part a multiple of 3

                # print(f"length before pop: {len(upper_pipes)//3}")
                upper_pipes.pop(i)  # right vertical
                upper_pipes.pop(i - 1)  # left vertical
                upper_pipes.pop(i - 2)  # bottom
                lower_pipes.pop(i)  # right vertical
                lower_pipes.pop(i - 1)  # left vertical
                lower_pipes.pop(i - 2)  # bottom
                yrandom.pop(i - 2)
                pipe_count -= 3
                # print(f"length after pop: {len(upper_pipes) // 3}")
                # print('hmm')  #to check if pipe pop and append worked
                pipe()  # builds a new pipe
                # print(f"length after piped: {len(upper_pipes) // 3}")

                break  # as new pipe appended, list now has pipes with new indices,
                # so get outta current loop

            for j in range(1, len(upper_pipes) - 4, 3):  # bird collsion with upper pipe's left vertical part
                if upper_pipes[j][0][0] - 15 <= bird_beak[0][0] <= upper_pipes[j][0][0] + 15:
                    for k in range(len(upper_pipes[j])):
                        if bird_c[0][1] == upper_pipes[j][k][1]:
                            lost = True
                    if lost == True:
                        break

            if lost == False:
                for j in range(1, len(lower_pipes) - 4, 3):  # bird collsion with lower pipe's left vertical part
                    if lower_pipes[j][0][0] - 15 <= bird_beak[0][0] <= lower_pipes[j][0][0] + 15:
                        for k in range(len(lower_pipes[j])):
                            if bird_c[0][1] == lower_pipes[j][k][1]:
                                lost = True
                                break
                        if lost == True:
                            break

            if lost == False:
                for j in range(0, len(upper_pipes) - 3, 3):  # bird collision with upper pipe's horizontal part
                    if upper_pipes[j][0][0] - 3 <= bird_c[0][0] <= upper_pipes[j][-1][0] + 3 or upper_pipes[j][0][0] - 3 <= bird_c[3][0] <= upper_pipes[j][-1][0] + 3:
                        for k in range(len(upper_pipes[j])):
                            if upper_pipes[j][k][1] - 10 <= bird_c[1][1] <= upper_pipes[j][k][1] + 3:
                                lost = True
                                lost_upper_horizontal = True
                                temp = j
                                # print(temp)
                                break
                        if lost == True:
                            break

            if lost == False:
                for j in range(0, len(lower_pipes) - 3, 3):  # bird collision with lower pipe's horizontal part
                    if lower_pipes[j][0][0] - 3 <= bird_c[0][0] <= lower_pipes[j][-1][0] + 3 or lower_pipes[j][0][0] - 3 <= bird_c[3][0] <= lower_pipes[j][-1][0] + 3:
                        for k in range(len(lower_pipes[j])):
                            if lower_pipes[j][k][1] - 5 <= bird_c[5][1] <= lower_pipes[j][k][1] + 5:
                                lost = True
                                lost_lower_horizontal = True
                                break
                        if lost == True:
                            break

            # print(pipe_count)
            if lost == False:  # bird crosses pipe and score increases(this is good logic code)
                if bird_c[3][0] > upper_pipes[pipe_count + 2][0][0]:
                    score += 1
                    pipe_count += 3
                    # print(f"Pipe_count:{pipe_count//3}")
                    # print(f"Upper_pipes len: {len(upper_pipes)}")
                    print(f"Score: {score}")

            # print(f"upper_pipes[(score*3)+2][0][0]: {upper_pipes[(score*3)+2][0][0]}")
            # print(f"Pipe count: {pipe_count}")
            # if lost == False:
            # pipe crosses origin and score increases:
            #     if upper_pipes[(pipe_count)+2][0][0] < 0: #this also works, but this is a bit too easy
            #         # print(upper_pipes[(pipe_count*3)+2][0][0])
            #         print(f"Pipe count: {pipe_count}")
            #         pipe_count += 3
            #         score += 1
            #         print(f"Score: {score}")
            # print(f"Upper: {len(upper_pipes)}")
            # print(f"pipes: {pipe_count}")



    elif lost == True and press_space == True:  # if bird collides with a pipe, i.e. lost == True
        print(f"Game Over! Your Score: {score}")
        press_space = False
        if lost_upper_horizontal == True:  # if collided with upper pipe's horizontal,
            # go down till reaching lower pipe's horizontal

            # print(f"Temp: {temp}")
            if bird_c[5][1] >= (yrandom[temp // 3] - gap) + 2:
                for i in range(len(bird_c)):
                    bird_c[i][1] -= bird_down_speed
                for i in range(len(bird_eye)):
                    bird_eye[i][1] -= bird_down_speed
                for i in range(len(bird_beak)):
                    bird_beak[i][1] -= bird_down_speed
                for i in range(len(bird_wing)):
                    for j in range(len(bird_wing[i])):
                        bird_wing[i][j][1] -= bird_down_speed

        elif lost_lower_horizontal == True:  # if collided with lower pipe's horizontal or touched floor,
            # stay still
            pass
        else:
            if bird_c[5][1] > -245:  # if collided with upper/lower pipe's left horizontal part,
                # go down till reaching the floor

                for i in range(len(bird_c)):
                    bird_c[i][1] -= bird_down_speed
                for i in range(len(bird_eye)):
                    bird_eye[i][1] -= bird_down_speed
                for i in range(len(bird_beak)):
                    bird_beak[i][1] -= bird_down_speed
                for i in range(len(bird_wing)):
                    for j in range(len(bird_wing[i])):
                        bird_wing[i][j][1] -= bird_down_speed

    if lost == True and press_space == False and lost_upper_horizontal == True and bird_c[5][1] >= (yrandom[temp // 3] - gap) + 2:
        # print('yeet')
        for i in range(len(bird_c)):
            bird_c[i][1] -= bird_down_speed
        for i in range(len(bird_eye)):
            bird_eye[i][1] -= bird_down_speed
        for i in range(len(bird_beak)):
            bird_beak[i][1] -= bird_down_speed
        for i in range(len(bird_wing)):
            for j in range(len(bird_wing[i])):
                bird_wing[i][j][1] -= bird_down_speed

    elif lost == True and press_space == False and lost_upper_horizontal == False and lost_lower_horizontal == False and bird_c[5][1] > -245:
        # print('hola')
        for i in range(len(bird_c)):
            bird_c[i][1] -= bird_down_speed
        for i in range(len(bird_eye)):
            bird_eye[i][1] -= bird_down_speed
        for i in range(len(bird_beak)):
            bird_beak[i][1] -= bird_down_speed
        for i in range(len(bird_wing)):
            for j in range(len(bird_wing[i])):
                bird_wing[i][j][1] -= bird_down_speed

def init():
    # //clear the screen
    glClearColor(0, 0, 0, 0)
    # //load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    # //initialize the matrix
    glLoadIdentity()
    # //give PERSPECTIVE parameters
    gluPerspective(104, 1, 1, 1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    # //near distance
    # //far distance


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # //Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Extreme Flappy Bird")
init()

glutDisplayFunc(display)  # display callback function
glutIdleFunc(animate)  # what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()  # The main loop of OpenGL
