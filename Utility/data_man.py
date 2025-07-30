import csv
import random
import time
from variables import par

t = 0
par['set'] = 0
par['read'] = 0

fieldnames = ['time [s]', 'Q_set [Nml/min]', 'Q_read [NmL/min']

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('data.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        line = {
            'time [s]': t,
            'Q_set [Nml/min]': par['set'],
            'Q_read [NmL/min': par['read']
        }

        csv_writer.writerow(line)

        t += 1
        par['set'] = par['set'] + random.randint(-10, +10)
        par['read'] = par['read'] + random.randint(-10, +10)

    time.sleep(1)
#
# x_value = 0
# total_1 = 1000
# total_2 = 1000
#
# fieldnames = ["x_value", "total_1", "total_2"]
#
# with open('data.csv', 'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()
#
# while True:
#     with open('data.csv', 'a', newline='') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#
#         info = {
#             "x_value": x_value,
#             "total_1": total_1,
#             "total_2": total_2
#         }
#
#         csv_writer.writerow(info)
#         print(x_value, total_1, total_2)
#
#         x_value += 1
#         total_1 = total_1 + random.randint(-6, 8)
#         total_2 = total_2 + random.randint(-5, 6)
#
#     time.sleep(1)