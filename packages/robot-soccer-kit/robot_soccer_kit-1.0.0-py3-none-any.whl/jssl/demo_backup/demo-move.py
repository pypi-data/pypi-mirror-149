import numpy as np
import place
import client
import field
import time

try:
    controllers = place.controllers

    robot = controllers['red'].robots[1]
    
    d = 0.3

    # Circle
    for a in range(300):
        x = a * np.pi * 2 / 300.
        c, s = np.cos(x), np.sin(x)
        place.goto(robot, place.frame(c*d, s*d, 0))
        time.sleep(0.02)

    place.goto_wait(robot, place.frame(d, 0, 0))

    place.goto_wait(robot, place.frame(0, d, -np.pi/2))
    place.goto_wait(robot, place.frame(0, -d, np.pi/2))
    place.goto_wait(robot, place.frame(-d, 0, np.pi))

    place.goto_wait(robot, place.frame(d, 0, 0))

    robot.control(100, 0, 0)
    time.sleep(1.25)
    robot.kick()
    place.goto_wait(robot, place.frame(d, 0, 0))

except Exception as e:
    print(e)
except KeyboardInterrupt:
    print('Interrupted')
    
place.stop_all()