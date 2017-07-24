import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from PyQt4 import QtCore
import math
import numpy as np

class Plotter(QtCore.QThread):
    def __init__(self, parent=None):
        super(Plotter, self).__init__(parent)

        # list of colors for plots
        self.COLORS = ['#ff0000', '#0000ff', '#ffff00', '#32cd32', '#ba55d3', '#87cefa', '#ffa500', '#ff1493', '#a020f0', '#00ced1', '#adff2f', '#ffd700', '#1e90ff', '#ff7f50', '#008000', '#ffc0cb', '#8a2be2']

    def topology_donut(self, labels, sizes, donut_colors):
        """
            Creates a donut chart showing the breakdown of the top 'num' topologies.

            Inputs:
            i. labels -- a list of labels outputted by top_freqs()[1]
            ii. sizes  -- a list of sizes outputted by top_freqs()[2]
            iii. donut_colors -- a list of colors outputted by donut_colors()

            Returns:
                A donut chart with the number of times a topology occurs and 'Other Topologies' for topologies that occur less than the
                most frequent 'num' topologies as the labels, and a list tops of the top 'num' scores.
        """

        # plots pie chart
        plt.rcParams['patch.edgecolor'] = '#000000'
        plt.pie(sizes, explode=None, labels=labels,
                colors=donut_colors, autopct=None, shadow=False)

        # create circle behind pie chart to outline it
        outer_circle = plt.Circle((0, 0), 1, color='#000000', fill=False, linewidth=1.25)

        # impose circle over pie chart to make a donut chart
        inner_circle = plt.Circle((0, 0), 0.65, color='#000000', fc='#ffffff', linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(inner_circle)
        fig.gca().add_artist(outer_circle)

        # set axes equal
        plt.axis('equal')

        # save plot
        plt.savefig("plots/topologyDonut.png", dpi=250)
        plt.clf()

        self.emit(QtCore.SIGNAL('DONUT_COMPLETE'))

    def topology_scatter(self, title, wins_to_tops, scatter_colors, y, subplotPosition=111):
        """
            Creates a scatter plot showing the topology as the y-axis and the window as the x-axis.

            Input:
                i. wins_to_tops   -- window to topology mapping outputted by windows_to_newick()[0]
                ii. scatter_colors -- list of colors outputted by topology_colors()[1]
                iii. y          -- list of y-axis values outputted by topology_colors()[2]

            Returns:
                A scatter plot with topologies as the x-axis and windows as the y-axis.
        """

        print wins_to_tops
        print scatter_colors
        print y

        ax = plt.subplot(subplotPosition)
        ax.set_title(title, fontsize=15)

        # area of plotted circles
        circleArea = math.pi * (3) ** 2

        # size y-axis on plot
        ax.set_yticks(np.arange(len(wins_to_tops) + 1, 0))

        # x-axis is window numbers
        x = wins_to_tops.keys()

        # for each index, and unique topology
        for (i, topology) in enumerate(set(wins_to_tops.values())):
            xc = [top for (j, top) in enumerate(x) if wins_to_tops.values()[j] == topology]
            yc = [top for (j, top) in enumerate(y) if wins_to_tops.values()[j] == topology]
            cols = [c for (j, c) in enumerate(scatter_colors) if wins_to_tops.values()[j] == topology]
            ax.scatter(xc, yc, s=circleArea, c=cols, alpha=1, edgecolors='#000000')
            ax.grid = True

        # labels axes
        ax.set_xlabel('Windows', fontsize=10)
        ax.set_ylabel('Top Newick Strings', fontsize=10)

        self.emit(QtCore.SIGNAL("SCATTER_COMPLETE"))

        return ax

    def stat_scatter(self, dataMap, title, xLabel, yLabel, subplotPosition=111):
        """
            Creates a scatter plot with the x-axis being the
            windows and the y-axis being the statistic to
            be graphed.

            Input:
                i. dataMap -- a mapping
                ii. name -- the name of the save file
                iii. title -- the title of the plot
                iv. xLabel -- the label for the x axis
                v. yLabel -- the label for the y axis

            Returns:
                A scatter plot with windows as the x-axis and a statistic as the y-axis.
        """

        ax = plt.subplot(subplotPosition)
        ax.set_title(title, fontsize=15)

        # sizes plot circles
        circleArea = math.pi * (3) ** 2

        # makes x values integers
        xValues = dataMap.keys()
        xIntegerValues = []

        for x in xValues:
            xIntegerValues.append(int(x))

        x = np.array(xIntegerValues)

        # get y values from dictionary and convert to an np array
        yValues = dataMap.values()
        y = np.array(yValues)

        # create scatter plot
        ax.scatter(x, y, s=circleArea, c='#000000', alpha=1)

        # label the axes
        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('y', fontsize=10)

        return ax

    def figureBarPlot(self, data, title, subplotPosition=111):
        """
            generates bar chart
        """

        ax = plt.subplot(subplotPosition)
        ax.set_title(title)
        numberOfBars = len(data)
        ind = np.arange(numberOfBars)  # the x locations for the groups
        width = .667  # the width of the bars
        colors = [(43.0 / 255.0, 130.0 / 255.0, 188.0 / 255.0), (141.0 / 255.0, 186.0 / 255.0, 87.0 / 255.0), (26.0 / 255.0, 168.0 / 255.0, 192.0 / 255.0), (83.5 / 255.0, 116.5 / 255.0, 44.5 / 255.0)]

        ax.bar(ind, data, width, color=colors)

        return ax

if __name__ == '__main__':  # if we're running file directly and not importing it
    p = Plotter()
    # p.figureBarPlot([1,2,3,4], 'name')
    a = {0: '(C,(G,O),H);', 1: '((C,G),O,H);', 2: '(C,(G,O),H);', 3: '(C,(G,O),H);', 4: '(C,(G,O),H);', 5: '(C,(G,O),H);', 6: '(C,(G,O),H);', 7: '(C,(G,O),H);', 8: '((C,G),O,H);', 9: '(C,(G,O),H);'}
    b = ['#ff0000', '#0000ff', '#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000', '#ff0000', '#0000ff', '#ff0000']
    c = [1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
    p.topology_scatter('henlo', a, b, c)
    plt.show()