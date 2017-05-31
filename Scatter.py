"""
Scatter Plot Function 
"""
import os
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def ml(info_file):
    likelihood = 0.0
    with open(info_file, 'r') as raxmlFile:
        info = raxmlFile.readlines()
        for line in info:
            words = line.split()
            for i in range(len(words)):
                if words[i] == 'Final':
                    likelihood = float(words[i + 4])
    return likelihood


def num_windows(directory):
    num = 0
    for filename in os.listdir(directory):
        if filename.endswith('.phylip'):
            num += 1
    return num

def scatter(num, likelihood)
area = math.pi * (5)**2

for i in range(1, num + 1):
    x = i
    y = likelihood / 100

    # changes color for different ranges
    if y <= 0.25:
        color = colors.hex2color('#0000FF')
    elif y > 0.25 and y <= 0.50:
        color = colors.hex2color('#00CC00')
    elif y > 0.50 and y <= 0.75:
        color = colors.hex2color('#FFFF00')
    elif y > 0.75 and y <= 1:
        color = colors.hex2color('#FF0000')

    plt.scatter(x, y, s = area, c = color, alpha = 1)

plt.show()
