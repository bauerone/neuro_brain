from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from db_interface import DbInterface

class DetailsWindow(QMainWindow):
    def __init__(self, patient_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.patient = DbInterface().load_patient(patient_id)

        self.setWindowTitle('Подробная информация о пациенте')

        wid = QWidget(self)
        self.setCentralWidget(wid)

        layout = QGridLayout()

        left_column = QWidget()
        left_column_layout = QVBoxLayout()
        left_column_layout.alignment = Qt.AlignmentFlag.AlignTop
        left_column.setLayout(left_column_layout)

        self.patient_label = QLabel('Пациент: %s %s %s'%(self.patient[2], self.patient[1], self.patient[3]))
        left_column_layout.addWidget(self.patient_label)

        self.birthday_label = QLabel('Дата рождения: %s'%(self.patient[4]))
        left_column_layout.addWidget(self.birthday_label)

        self.medical_id_label = QLabel('Номер полиса: %s'%(self.patient[5]))
        left_column_layout.addWidget(self.medical_id_label)

        self.medical_history_label = QLabel('История болезни:')
        left_column_layout.addWidget(self.medical_history_label)

        self.medical_history = QTextEdit()
        self.medical_history.setReadOnly(True)
        self.medical_history.setText(self.patient[6])
        left_column_layout.addWidget(self.medical_history)

        right_column = QTableWidget()
        right_column.setColumnCount(4)
        right_column.setColumnWidth(0, 150)
        right_column.setColumnWidth(1, 150)
        right_column.setColumnWidth(2, 150)
        right_column.setColumnWidth(3, 150)

        self.diagnostics = DbInterface().find_diagnostics_for_patient(self.patient[0])

        right_column.setHorizontalHeaderLabels(['Дата', 'Первичный диагноз', 'Конечный диагноз', 'Лечение'])
        right_column.setRowCount(len(self.diagnostics))

        row = 0
        for e in self.diagnostics:
            right_column.setItem(row, 0, QTableWidgetItem(e[5]))
            right_column.setItem(row, 1, QTableWidgetItem(e[2]))
            right_column.setItem(row, 2, QTableWidgetItem(e[3]))
            right_column.setItem(row, 3, QTableWidgetItem(e[4]))
            row += 1

        layout.addWidget(left_column, 0, 0)
        layout.addWidget(right_column, 0, 1)
        wid.setLayout(layout)
        

