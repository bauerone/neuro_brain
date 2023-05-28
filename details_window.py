from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class DetailsWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Подробная информация о пациенте')

        wid = QWidget(self)
        self.setCentralWidget(wid)
