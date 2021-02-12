import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import pyximport
pyximport.install(language_level=0)
from source import Star, update_star_positions, get_arrows
"""
Different simulation implementations:

1. Python class             ~   200 000 /s
2. Python dict              ~   250 000 /s
3. Cython dict              ~   755 000 /s   (pythonic)
4. Cython list              ~ 1 248 000 /s
5. Cython class             ~ 1 300 000 /s   (internally struct)
6. Cython class + optimiz   ~ 3 122 000 /s   (declaring star iter as Star type)

"""


def main():
    STEP = 50000  # Number of iterations between showing them onscreen
    VELOC_COEF = 50  # Coefficient for arrow display
    ACCEL_COEF = 50000
    SIZE = 500  # Size of visible field

    # Define stars
    stars = []
    star1 = Star(x=0, y=0, vx=0, vy=0, m=50, name='star1')
    stars.append(star1)
    star2 = Star(x=1000, y=0, vx=0, vy=0.002, m=20, name='star2')
    stars.append(star2)
    star3 = Star(x=0, y=1000, vx=-0.02, vy=0, m=35, name='star3')
    stars.append(star3)
    star4 = Star(x=1000, y=1000, vx=-0.02, vy=0.002, m=35, name='star4')
    stars.append(star4)

    # Prepare visuals
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)

    previous_positions_x = list()
    previous_positions_y = list()

    def animate(i):
        # Update speeds and positions of stars
        start = time.time()
        x, y, sizes, names = update_star_positions(STEP)
        end = time.time()
        print(
            f"Calculations took {end-start:.2f} seconds | {STEP/(end-start):_.0f} per second"
        )

        # Plot
        ax.clear()
        plt.scatter(x, y, s=sizes)
        plt.scatter(previous_positions_x,
                    previous_positions_y,
                    color='k',
                    s=0.1)

        lvx, lvy, lax, lay = get_arrows(
        )  # Gets information about stars speed and accelerations
        m = 10

        for i, name in enumerate(names):
            plt.text(x[i], y[i], names[i])
            # plt.arrow(x[i], y[i], min(VELOC_COEF*lvx[i],m), min(VELOC_COEF*lvy[i],m), color='b')
            # plt.arrow(x[i], y[i], min(ACCEL_COEF*lax[i],m), min(ACCEL_COEF*lay[i],m), color='r')

        # Save trajectories
        previous_positions_x.extend(x)
        previous_positions_y.extend(y)

    animation = FuncAnimation(fig, animate, interval=1, save_count=500)
    plt.tight_layout()

    # Save or show
    # animation.save('anim.mp4', fps=15, bitrate=2000)
    plt.show()


main()