from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtCore, QtGui, QtWidgets
import os

class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
            ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
            ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
            ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
            ('Custom Button', 'custom btn hover txt', 'warning', 'configure_subplots'),
            )
        # self.toolitems = [t for t in self.toolitems if
        #              t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
        NavigationToolbar.__init__(self, canvas_, parent_)

    def _icon(self, name):
        print name
        pm = QtGui.QPixmap(os.path.join(self.basedir, name))
        if hasattr(pm, 'setDevicePixelRatio'):
            pm.setDevicePixelRatio(self.canvas._dpi_ratio)
        return QtGui.QIcon(pm)

    def pan(self):
        NavigationToolbar.pan(self)
        self.mode = "henlo!"  # <--- whatever you want to replace "pan/zoom" goes here
        self.set_message(self.mode)