import numpy as np
import place
import client
import field
import time

controller = client.Controller()
place.goto_configuration('side')
place.goto_configuration('dots')

try:
    robots = [
        ['red', 1, 0],
        ['red', 2, np.pi/2],
        ['blue', 1, np.pi],
        ['blue', 2, 3*np.pi/2]
    ]

    alpha = 0
    dist = 0.3
    while alpha < 6:
        ball = controllers['red'].ball
        if ball is not None:
            alpha += 0.02
            for color, index, offset in robots:
                x, y = ball[0] + dist*np.cos(alpha+offset), ball[1] + dist*np.sin(alpha+offset)
                orientation = np.arctan2(ball[1]-y, ball[0]-x)
                robot = controllers[color].robots[index]
                place.goto(robot, place.frame(x, y, orientation))
                

        time.sleep(0.05)

    place.goto_configuration('dots')
    place.goto_configuration('side')


except Exception as e:
    print(e)
except KeyboardInterrupt:
    print('Interrupted')
    
place.stop_all()