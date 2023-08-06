import numpy as np
import place
import client
import field
import time
import pandas as pd

controllers = place.controllers

ball_samples = 5
last_dts = []
last_balls = []
ball_deceleration = 0.3 # m/s^-2

def future_ball():
    if len(last_balls) == ball_samples:
        ball = last_balls[-1]
        old_ball = last_balls[0]
        ball_speed = (ball - old_ball) / (np.sum(last_dts))
        speed = np.linalg.norm(ball_speed)

        if speed > 0.01:
            ball_direction = (ball_speed / speed)
            T = speed / ball_deceleration
            return ball + (speed*T - 0.5*ball_deceleration*(T**2))*ball_direction, speed
        else:
            return ball, 0
    else:
        return None, 0

def attack(robot, target='goal_blue', power=1.0, use_future_ball=True):
    if use_future_ball:
        ball, ball_speed = future_ball()
    else:
        ball = robot.ball()
        ball_speed = 0

    if ball is not None:
        distance = 0.15
        if type(target) is str and target == 'goal_blue':
            target = np.array([-field.length*0.65, 0.])
        elif type(target) is str and target == 'goal_red':
            target = np.array([field.length*0.65, 0.])
        vector = target - ball
        orientation = np.arctan2(vector[1], vector[0])
        position = ball - vector * distance /np.linalg.norm(vector)

        target_frame = place.frame(position[0], position[1], orientation)

        if place.goto(robot, target_frame) and ball_speed < 0.02:
            robot.control(250, 0, 0)
            time.sleep(0.5)
            robot.control(0, 0, 0)
            robot.kick(power)
            return True

    return False

red1 = controllers['red'].robots[1]
blue1 = controllers['blue'].robots[1]

def red1(robot, dt):  
    red1.t += dt

    if red1.state == 'attack':
        if attack(robot, 'goal_blue', 0.1):
            red1.state = 'rest'
            red1.t = 0
    elif red1.state == 'rest':
        if red1.t > 1.75:
            red1.state = 'attack'
        else:
            place.goto(robot, place.frame(0.5, 0.3, np.pi))
red1.state = 'attack'
red1.t = 0

def red2(robot, dt):
    ball = robot.ball()
    if ball is not None:
        y = min(field.goal_width/2, max(-field.goal_width/2, ball[1]))
        place.goto(robot, place.frame(field.length/2, y, np.pi))

def blue2(robot, dt):
    ball = robot.ball()
    if ball is not None:
        if ball[0] < -0.2:
            blue2.kicked = attack(robot, np.array([0.3, -0.2]), 0.1, use_future_ball=False) or blue2.kicked
        else:
            y = min(field.goal_width/2, max(-field.goal_width/2, ball[1]))
            place.goto(robot, place.frame(-field.length/2, y, 0))
blue2.kicked = False

def blue1(robot, dt):
    ball = robot.ball()
    if ball is not None:
        if blue2.kicked and ball[0] > -0.35:
            attack(robot, np.array([field.length*0.65, 0.15]))
        else:
            place.goto(robot, place.frame(0.3, -0.6, np.pi/4))

data = {'t': [], 'x': [], 'y': [], 'fx': [], 'fy': [], 'speed': [], 'dt': []}
start = time.time()

try:
    last_tick = time.time()

    def update(controller, dt):
        global last_balls, last_dts

        ball = controller.ball
        if ball is not None:
            last_balls.append(ball.copy())
            last_balls = last_balls[-ball_samples:]
            last_dts.append(dt)
            last_dts = last_dts[-ball_samples:]

            future, speed = future_ball()
            if future is not None:
                data['t'].append(time.time() - start)
                data['x'].append(ball[0])
                data['y'].append(ball[1])
                data['fx'].append(future[0])
                data['fy'].append(future[1])
                data['speed'].append(speed)
                data['dt'].append(np.sum(last_dts))

    controllers['red'].on_sub = update

    while True:
        dt = time.time() - last_tick
        last_tick = time.time()

        ball = controllers['red'].ball

        if ball is None:
            print('End, going to game config.')
            place.goto_configuration('game')
            place.stop_all()
            exit()

        red1(controllers['red'].robots[1], dt)
        red2(controllers['red'].robots[2], dt)
        blue1(controllers['blue'].robots[1], dt)
        blue2(controllers['blue'].robots[2], dt)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    df = pd.DataFrame(data)
    df.to_csv('log.csv')

print('Stopping...')
place.stop_all()