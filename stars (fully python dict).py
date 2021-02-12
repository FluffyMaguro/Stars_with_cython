import math
import time
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


INTERVAL = 0.001 # How long is the duration of one iteration
STEP = 10000 # Number of iterations between showing them onscreen
ARROW_COEF = 50 # Coefficient for arrow display
SIZE = 500 # Size of visible field

stars = list()

def Star(x, y, vx, vy, m, name):
    s = {'x':x,'y':y,'ax':0,'ay':0,'vx':vx,'vy':vy,'m':m,'name':name}
    stars.append(s)
    return s


def update_speed(d):
    for star in stars:
        if star == d:
            continue

        # Calculate acceleration 
        dirx = star['x'] - d['x']
        diry = star['y'] - d['y']
        r2 = dirx**2 + diry**2
        a = star['m'] / r2 #Using natural units so G=1

        # # Project acceleration into components
        if dirx == 0:
            d['ax'] = 0
        elif dirx > 0:
            d['ax'] = a * (((r2 - diry**2 )/ r2) ** 0.5)
        else:
            d['ax'] = a * (((r2 - diry**2 )/ r2) ** 0.5) * (-1)

        if diry == 0:
            d['ay'] = 0
        elif diry > 0:
            d['ay'] = a * (((r2 - dirx**2 )/ r2) ** 0.5)
        else:
            d['ay'] = a * (((r2 - dirx**2 )/ r2) ** 0.5) * (-1)

        # # Update speeds
        d['vx'] += INTERVAL * d['ax']
        d['vy'] += INTERVAL * d['ay']


def update_position(d):
    d['x'] += d['vx'] * INTERVAL
    d['y'] += d['vy'] * INTERVAL

# Define stars
s1 = Star(0,0, vx=0, vy=0, m=50, name='star1')
s2 = Star(2000,0, vx=0, vy=0.002, m=20, name='star2')

# Prepare visuals
fig, ax = plt.subplots(figsize=(10, 8))

previous_positions_x = list()
previous_positions_y = list()

def animate(i):
    # Update speeds and positions of stars
    start = time.time()
    for _ in range(STEP):
        for star in stars:
            update_speed(star)
        for star in stars:
            update_position(star)
    end = time.time()
    print(f"Calculations took {end-start:.2f} seconds | {STEP/(end-start):_.2f} per second")

    # Get new coordinates
    x = [s['x'] for s in stars]
    y = [s['y'] for s in stars]
    sizes = [s['m'] for s in stars]
    names = [s['name'] for s in stars]

    # Plot
    ax.clear()
    plt.scatter(x, y, s=sizes)
    plt.scatter(previous_positions_x, previous_positions_y, color='k', s=0.1)
    for i, name in enumerate(names):
        plt.text(x[i]+10, y[i]+10, names[i])
        plt.arrow(x[i], y[i], ARROW_COEF*stars[i]['vx'], ARROW_COEF*stars[i]['vy'], color='b')
        plt.arrow(x[i], y[i], 10*ARROW_COEF*stars[i]['ax'], 10*ARROW_COEF*stars[i]['ay'], color='r')

    # Save trajectories
    previous_positions_x.extend(x)
    previous_positions_y.extend(y)


ani = FuncAnimation(fig, animate, interval=1)
plt.tight_layout()
plt.show()