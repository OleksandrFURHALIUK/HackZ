from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAction, QItemDelegate, QComboBox

import sys

from forms.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
