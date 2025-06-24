from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from guipy.plot import Ui_plotWindow


class PlotView(QMainWindow):
    signal_closed = pyqtSignal(object)

    def __init__(self):
        super(PlotView, self).__init__()
        self.ui = Ui_plotWindow()
        self.ui.setupUi(self)

        self.view_init()

    def view_init(self):
        self.plotWidget = PlotWidget(self.ui.centralwidget)
        self.plotWidget.setObjectName("plotWidget")
        self.plotWidget.setBackground('w')
        self.plotWidget.addLegend()
        self.ui.verticalLayout.addWidget(self.plotWidget)

    def draw_lin_var(self, lin_var):
        self.plotWidget.clear()
        if lin_var == None:
            return None
        terms = lin_var.terms
        for i in range(len(terms)):
            t = terms[i]
            self.draw_term(term=t, color_matrix=t.color, width=3, name=t.name)
        return "Ok"

    def draw_term(self, term, color_matrix, width, name):
        pen = pg.mkPen(color=(color_matrix[0], color_matrix[1], color_matrix[2]), width=width)
        self.plotWidget.plot([term.points[0].x, term.points[1].x], [0, 1], pen=pen)
        self.plotWidget.plot([term.points[1].x, term.points[2].x], [1, 1], pen=pen)
        self.plotWidget.plot([term.points[2].x, term.points[3].x], [1, 0], pen=pen, name=name)

    def draw_result(self, x, y, res, lv_res_name, res_name):
        self.plotWidget.clear()
        pen = pg.mkPen(color=(255, 77, 0), width=2)
        self.plotWidget.plot(x, y, pen=pen)
        pen = pg.mkPen(color=(25, 255, 25), width=2)
        self.plotWidget.plot([res, res], [0, 1.0], pen=pen, name = res_name)
        self.plotWidget.setTitle(lv_res_name)

    def draw_activization(self, x, y):
        self.plotWidget.clear()
        pen = pg.mkPen(color=(255, 77, 0), width=2)
        self.plotWidget.plot(x, y, pen=pen)

    def closeEvent(self, e):
        # print('cls')
        self.signal_closed.emit(self)
