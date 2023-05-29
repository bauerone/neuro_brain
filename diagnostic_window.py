from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from db_interface import DbInterface
from datetime import date

class DiagnosticWindow(QMainWindow):
    def __init__(self, patient_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.patient = DbInterface().load_patient(patient_id)
        self.setWindowTitle("Диагностика")

        wid = QWidget(self)
        self.setCentralWidget(wid)

        layout = QGridLayout()

        left_column = QWidget()
        left_column_layout = QVBoxLayout()
        left_column_layout.alignment = Qt.AlignmentFlag.AlignTop
        left_column.setLayout(left_column_layout)

        right_column = QWidget()
        right_column_layout = QVBoxLayout()
        right_column.setLayout(right_column_layout)

        self.patient_label = QLabel('Пациент:')
        left_column_layout.addWidget(self.patient_label)

        self.patient_name = QLabel('%s %s %s'%(self.patient[2], self.patient[1], self.patient[3]))
        left_column_layout.addWidget(self.patient_name)

        self.medical_id_label = QLabel('Номер полиса:')
        left_column_layout.addWidget(self.medical_id_label)

        self.medical_id = QLabel(self.patient[5])
        left_column_layout.addWidget(self.medical_id)

        self.first_diagnosis_label = QLabel('Первичный диагноз:')
        right_column_layout.addWidget(self.first_diagnosis_label)

        self.first_diagnosis = QTextEdit()
        self.first_diagnosis.setReadOnly(True)
        right_column_layout.addWidget(self.first_diagnosis)

        self.final_diagnosis_label = QLabel('Окончательный диагноз:')
        right_column_layout.addWidget(self.final_diagnosis_label)

        self.final_diagnosis = QTextEdit()
        right_column_layout.addWidget(self.final_diagnosis)

        self.therapy_label = QLabel('Лечение:')
        right_column_layout.addWidget(self.therapy_label)

        self.therapy = QTextEdit()
        right_column_layout.addWidget(self.therapy)

        self.choose_image_button = QPushButton("Выбрать изображение")
        self.choose_image_button.clicked.connect(self.getfiplaceholder)
        left_column_layout.addWidget(self.choose_image_button)

        self.placeholder = QLabel()    
        left_column_layout.addWidget(self.placeholder)

        layout.addWidget(left_column, 0, 0)
        layout.addWidget(right_column, 0, 1)

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.save_diagnostic)
        layout.addWidget(self.save_button, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        wid.setLayout(layout)
            
    def getfiplaceholder(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Выбрать файл', 
            'c:\\',"Поддерживаемые форматы файлов (*.jpg *.gif *.png)")
        self.placeholder.setPixmap(QPixmap(fname))
        self.first_diagnosis.append("Найдена патология")

    def save_diagnostic(self):
        db = DbInterface()
        db.add_diagnostic(self.patient[0],
                          self.first_diagnosis.toPlainText().strip(),
                          self.final_diagnosis.toPlainText().strip(),
                          self.therapy.toPlainText().strip(),
                          date.today().strftime("%m-%d-%Y"))
        