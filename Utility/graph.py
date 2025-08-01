import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# plt.style.use('fivethirtyeight')
#
# x_vals = []
# y_vals = []

# index = count()


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['time [s]']
    y1 = data['Q_set [Nml/min]']
    y2 = data['Q_read [NmL/min']

    plt.cla()

    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')

    plt.legend(loc='upper left')
    plt.tight_layout()


a = FuncAnimation(plt.gcf(), animate, interval=1000)
# ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()

# while True:
#     time.sleep(5)
#     ani = FuncAnimation(plt.gcf(), animate, interval=1000)
#
#     plt.tight_layout()
#     plt.show()
