"""
Scatter Plot Generator
"""
import os
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def num_windows(directory):
    """
    Counts the number of windows created
    for use in x-axis of the scatter plot.

    Input:
    directory -- folder containing window files

    Returns:
    A count of the number of window files.
    """
    num = 0

    for filename in os.listdir(directory):
        if filename.endswith('.phylip'):
            num += 1

    return num


def ml(num, directory):
    """
    Reads info file to find Final ML Optimization
    Likelihood for use in y-axis of the scatter plot.

    Input:
    num       -- count outputted by num_windows
    directory -- RAxML folder containing info files

    Returns:
    The Likelihood number.
    """
    likelihood = []

    while len(likelihood) <= num:
        for filename in os.listdir(directory):
            if os.path.splitext(filename)[0] == "RAxML_info":
                with open(os.path.join(directory, filename), 'r') as raxmlFile:
                    info = raxmlFile.readlines()
                    for line in info:
                        words = line.split()
                        for i in range(len(words)):
                            if words[i] == 'Final':
                                likelihood.append(float(words[i + 4]))

    return likelihood


def scatter(num, likelihood):
    """
    Creates a scatter plot for use in the
    visualization tool.

    Input:
    num        -- count outputted by num_windows
    likelihood -- number outputted by ml

    Returns:
    A scatter plot with num as the x-axis and
    likelihood as the y-axis.
    """
    area = math.pi * (5)**2

    for i in range(1, num + 1):
        x = i
        y = float(likelihood[i]) / 100

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

    plt.savefig("Plot.png")

# print num_windows('windows'), ml(num_windows('windows'), 'RAx_Files')
# scatter(num_windows('windows'), ml(num_windows('windows'), 'RAx_Files'))
