import sqlite3

class DbInterface:
    def __init__(self):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()

            sqlite_create_patients_table_query = '''CREATE TABLE patients (
                                                 id INTEGER PRIMARY KEY,
                                                 first_name TEXT NOT NULL,
                                                 last_name TEXT NOT NULL,
                                                 middle_name TEXT NOT NULL,
                                                 birth_date TEXT NOT NULL,
                                                 medical_id TEXT NOT NULL,
                                                 medical_history TEXT NOT NULL);'''
            
            cursor.execute(sqlite_create_patients_table_query)

            sqlite_create_diagnostics_table_query = '''CREATE TABLE diagnostics (
                                                    id INTEGER PRIMARY KEY,
                                                    patient_id INTEGER NOT NULL,
                                                    first_diagnosis TEXT NOT NULL,
                                                    final_diagnosis TEXT NOT NULL,
                                                    therapy TEXT NOT NULL,
                                                    date TEXT NOT NULL);'''
            
            cursor.execute(sqlite_create_diagnostics_table_query)

            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
        
    def add_patient(self, first_name, last_name, middle_name, birth_date, medical_id, medical_history):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_patient_query = """INSERT INTO patients
                                      (first_name, last_name, middle_name, birth_date, medical_id, medical_history)
                                      VALUES  ('%s', '%s', '%s', '%s', '%s', '%s');"""%(first_name, last_name, middle_name, birth_date, medical_id, medical_history)
        
        cursor.execute(sqlite_insert_patient_query)
        sqlite_connection.commit()
        sqlite_connection.close()

    def load_patients(self):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        sqlite_fetch_patients_query = """SELECT * FROM patients ORDER BY id ASC"""

        cursor.execute(sqlite_fetch_patients_query)
        patients = cursor.fetchall()
        sqlite_connection.close()

        return patients

    def load_patient(self, patient_id):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        sqlite_fetch_patients_query = """SELECT * FROM patients WHERE id=%s LIMIT 1"""%(patient_id)

        cursor.execute(sqlite_fetch_patients_query)
        patient = cursor.fetchone()
        sqlite_connection.close()

        return patient
    
    def last_patient(self):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()

        sqlite_fetch_patients_query = """SELECT * FROM patients ORDER BY id DESC LIMIT 1"""

        cursor.execute(sqlite_fetch_patients_query)
        patient = cursor.fetchone()
        sqlite_connection.close()

        return patient
    
    def add_diagnostic(self, patient_id, first_diagnosis, final_diagnosis, therapy, date):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_diagnostic_query = """INSERT INTO diagnostics
                                        (patient_id, first_diagnosis, final_diagnosis, therapy, date)
                                        VALUES  ('%s', '%s', '%s', '%s', '%s');"""%(patient_id, first_diagnosis, final_diagnosis, therapy, date)
        
        cursor.execute(sqlite_insert_diagnostic_query)
        sqlite_connection.commit()
        sqlite_connection.close()
    
    def find_diagnostics_for_patient(self, patient_id):
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        sqlite_find_diagnostics_query = """SELECT * FROM diagnostics WHERE patient_id=%s ORDER BY id ASC"""%(patient_id)

        cursor.execute(sqlite_find_diagnostics_query)
        diagnostics = cursor.fetchall()
        sqlite_connection.close()

        print(diagnostics)

        return diagnostics