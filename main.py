import sys

from PyQt5 import QtWidgets

from common_class import CommonObject

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    common_obj = CommonObject()
    # Отображаем главное окно
    common_obj.main_view.show()
    # Закрываем соединение с БД при выходе
    # app.aboutToQuit.connect(common_obj.db_model.close)
    sys.exit(app.exec_())
