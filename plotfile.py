import matplotlib.pyplot as plt

class Plotter(object):
    def __init__(self, xval=None, yval=None):
        self.xval = xval
        self.yval = yval

    def plotthing(self):
        f = plt.figure()
        sp = f.add_subplot(111)
        sp.plot(self.xval, self.yval, 'o-')
        plt.savefig('henlo')
        return f