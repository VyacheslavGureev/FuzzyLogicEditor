from main_controller import MainController
from main_model import MainModel
from main_view import MainView
from plot_view import PlotView


class CommonObject():
    def __init__(self):
        super(CommonObject, self).__init__()

        # Создаем модели
        self.main_model = MainModel()

        # Создаем виды
        self.main_view = MainView()
        self.plot_views = {}
        self.plot_view = PlotView()
        self.plot_views['lin_var'] = self.plot_view

        # Создаем контроллеры
        self.main_controller = MainController(self.main_view, self.plot_views, self.create_plot_view, self.main_model)

        self.main_view.signal_view_init.emit()

    def create_plot_view(self):
        return PlotView()


class PltsViews():
    def __init__(self):
        self.plots = {}

    def create_plot_view(self):
        plt = PlotView()
        plt.signal_closed.connect(self.del_plt)
        self.plots[plt] = plt
        return plt

    def del_plt(self, plt):
        del self.plots[plt]
