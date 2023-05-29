from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QIcon, QAction
from diagnostic_window import DiagnosticWindow
from details_window import DetailsWindow
from db_interface import DbInterface
import sys

class MainWindow(QMainWindow):
    db = DbInterface()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('СИСТЕМА РАСПОЗНАВАНИЯ ПАТОЛОГИЙ В МОЗГЕ')
        self.setGeometry(100, 100, 600, 400)

        patients = self.db.load_patients()

        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)

        self.table.setColumnCount(6)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)

        self.table.setHorizontalHeaderLabels(['id в БД', 'Имя', 'Фамилия', 'Отчество', 'Дата рождения', 'Номер полиса'])
        self.table.setRowCount(len(patients))

        row = 0
        for e in patients:
            self.table.setItem(row, 0, QTableWidgetItem(str(e[0])))
            self.table.setItem(row, 1, QTableWidgetItem(e[1]))
            self.table.setItem(row, 2, QTableWidgetItem(e[2]))
            self.table.setItem(row, 3, QTableWidgetItem(e[3]))
            self.table.setItem(row, 4, QTableWidgetItem(e[4]))
            self.table.setItem(row, 5, QTableWidgetItem(e[5]))
            row += 1

        dock = QDockWidget('Новый пациент')
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)


        self.first_name = QLineEdit(form)
        self.last_name = QLineEdit(form)
        self.middle_name = QLineEdit(form)
        self.birth_date = QDateEdit(calendarPopup=True)
        self.medical_id = QLineEdit(form)
        self.medical_history = QTextEdit(form)

        layout.addRow('Имя:', self.first_name)
        layout.addRow('Фамилия:', self.last_name)
        layout.addRow('Отчество', self.middle_name)
        layout.addRow('Дата рождения', self.birth_date)
        layout.addRow('Страховой полис', self.medical_id)
        layout.addRow('История болезни', self.medical_history)

        btn_add = QPushButton('Добавить')
        btn_add.clicked.connect(self.add_patient)
        layout.addRow(btn_add)

        # add delete & edit button
        toolbar = QToolBar('main toolbar')
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)


        delete_action = QAction(QIcon('./assets/delete.png'), '&Delete', self)
        delete_action.triggered.connect(self.delete)
        toolbar.addAction(delete_action)

        details_action = QAction(QIcon('./assets/details.png'), '&Show details', self)
        details_action.triggered.connect(self.show_details_window)
        toolbar.addAction(details_action)

        diagnostic_action = QAction(QIcon('./assets/diagnostic.png'), '&Show diagnostic', self)
        diagnostic_action.triggered.connect(self.show_diagnostic_window)
        toolbar.addAction(diagnostic_action)

        dock.setWidget(form)


    def delete(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Внимание','Выберите запись для удаления')

        button = QMessageBox.question(
            self,
            'Подтверждение',
            'Вы уверены, что хотите удалить выбранную запись?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            self.table.removeRow(current_row)

    def show_details_window(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Внимание', 'Выберите запись для отображения детальной информации')
        
        self.details_window = DetailsWindow()
        self.details_window.show()
    
    def show_diagnostic_window(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Внимание','Выберите запись для отображения окна диагностики')
        
        self.diagnostic_window = DiagnosticWindow(self.table.model().data(self.table.model().index(current_row, 0)))
        self.diagnostic_window.show()

    def valid(self):
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        middle_name = self.middle_name.text().strip()
        birth_date = self.birth_date.text().strip()
        medical_id = self.medical_id.text().strip()
        medical_history = self.medical_history.toPlainText().strip()

        
        if not first_name:
            QMessageBox.critical(self, 'Ошибка', 'Введите имя')
            self.first_name.setFocus()
            return False

        if not last_name:
            QMessageBox.critical(self, 'Ошибка', 'Введите фамилию')
            self.last_name.setFocus()
            return False
        
        if not middle_name:
            QMessageBox.critical(self, 'Ошибка', 'Введите отчество')
            self.middle_name.setFocus()
            return False

        if not birth_date:
            QMessageBox.critical(self, 'Ошибка', 'Введите правильный возраст')
            self.birth_date.setFocus()
            return False

        if not medical_id:
            QMessageBox.critical(self, 'Ошибка', 'Введите полис')
            self.medical_id.setFocus()
            return False

        if not medical_history:
            QMessageBox.critical(self, 'Ошибка', 'Введите полис')
            self.medical_history.setFocus()
            return False

        return True

    def reset(self):
        self.first_name.clear()
        self.last_name.clear()
        self.middle_name.clear()
        self.birth_date.clear()
        self.medical_id.clear()
        self.medical_history.clear()

    def add_patient(self):
        if not self.valid():
            return
        
        self.db.add_patient(
            self.first_name.text().strip(),
            self.last_name.text().strip(),
            self.middle_name.text().strip(),
            self.birth_date.text().strip(),
            self.medical_id.text().strip(),
            self.medical_history.toPlainText().strip()
        )

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(
            row, 0, QTableWidgetItem(self.first_name.text().strip())
        )
        self.table.setItem(
            row, 1, QTableWidgetItem(self.last_name.text().strip())
        )
        self.table.setItem(
            row, 2, QTableWidgetItem(self.middle_name.text().strip())
        )
        self.table.setItem(
            row, 3, QTableWidgetItem(self.birth_date.text().strip())
        )
        self.table.setItem(
            row, 4, QTableWidgetItem(self.medical_id.text().strip())
        )

        self.reset()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())