from PyQt5.QtWidgets import QMessageBox
import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='123456',
            host='localhost',
            database='btlpy'
        )
        return connection
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Lỗi kết nối cơ sở dữ liệu", f"Lỗi: {err}")
        return None