# Working with multiple figure windows and subplots
import matplotlib.pyplot as plt
import numpy as np

# t = np.arange(0.0, 2.0, 0.01)
# s1 = np.sin(2*np.pi*t)
# s2 = np.sin(4*np.pi*t)
#
# def createPlot():
#     fig = plt.figure(1)
#     subplot = fig.add_subplot(211)
#     subplot.plot(t, s1)
#     subplot2 = fig.add_subplot(212)
#     subplot2.plot(t, 2*s1)
#
#     fig.show()
#
#     # return fig
#
# # createPlot()
#
# def createPlot2():
#     plt.figure(2)
#     plt.subplot(211)
#     plt.plot(t, s1)
#     plt.subplot(212)
#     plt.plot(t, 2*s1)
#
#
# createPlot2()
# plt.show()




# plt.figure(1)
# plt.subplot(211)
# plt.plot(t, s1)
# plt.subplot(212)
# plt.plot(t, 2*s1)

# plt.figure(2)
# plt.plot(t, s2)

# now switch back to figure 1 and make some changes
# plt.figure(1)
# plt.subplot(211)
# plt.plot(t, s2, 's')
# ax = plt.gca()
# ax.set_xticklabels([])

# plt.show()






from plotfile import Plotter

app = Plotter(xval=range(0,10), yval=range(0,10))
plot = app.plotthing()
plt.show()