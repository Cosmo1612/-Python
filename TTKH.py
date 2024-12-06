from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QTableWidget
from DB_Connect import create_connection
import mysql.connector

class TTKH_w(QMainWindow):
    def __init__(self, widget):
        super(TTKH_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.load_data()
        self.Them_KH.clicked.connect(self.ThemKH_Form)
        self.Sua_KH.clicked.connect(self.SuaKH_Form)
        self.Xoa_KH.clicked.connect(self.XoaKH_Form)
        self.Home.clicked.connect(self.Home_Form)
        self.Table_KH.cellClicked.connect(self.load_selected_row)
        self.selected_user = None 

    def load_ui(self):
        uic.loadUi('TTKH.ui', self)
    def Home_Form(self):
        self.widget.setCurrentIndex(1)
    
    def ThemKH_Form(self):
        MaThue = self.MaThue_text.text()
        TenKhach = self.TenKhach_text.text()
        Phone = self.Phone_text.text()
        DiaChi = self.DiaChi_text.text()

        if not MaThue or not TenKhach or not Phone or not DiaChi:
            QMessageBox.warning(self, "Thêm khách hàng", "Vui lòng điền đầy đủ thông tin.")
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            sql_insert_01 = "INSERT INTO tt_nguoithue (MaKhachHang, TenKH, SDT, DiaChi) VALUES (%s, %s, %s, %s)"
            query.execute(sql_insert_01, (MaThue, TenKhach, Phone, DiaChi))
            db.commit()
            QMessageBox.information(self, "Thêm khách hàng", "Khách hàng mới đã được thêm thành công")
            self.load_data()  # Tải lại bảng sau khi thêm mới
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def SuaKH_Form(self):
        MaThue = self.MaThue_text.text()
        TenKhach = self.TenKhach_text.text()
        Phone = self.Phone_text.text()
        DiaChi = self.DiaChi_text.text()

        if not self.selected_user:
            QMessageBox.warning(self, "Chỉnh sửa", "Hãy chọn khách hàng để chỉnh sửa.")
            return

        if not MaThue or not TenKhach or not Phone or not DiaChi:
            QMessageBox.warning(self, "Chỉnh sửa", "Vui lòng điền đầy đủ thông tin.")
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Cập nhật thông tin người dùng
            sql_update_01 = "UPDATE tt_nguoithue SET MaKhachHang = %s, TenKH = %s, SDT = %s, DiaChi = %s WHERE MaKhachHang = %s"
            query.execute(sql_update_01, (MaThue, TenKhach, Phone, DiaChi, self.selected_user))
            db.commit()
            QMessageBox.information(self, "Chỉnh sửa", "Thông tin khách hàng đã được cập nhật thành công")
            self.load_data()  # Tải lại bảng sau khi cập nhật
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def XoaKH_Form(self):
        if not self.selected_user:
            QMessageBox.warning(self, "Xóa", "Hãy chọn khách hàng để xóa.")
            return

        reply = QMessageBox.question(self, "Xóa khách hàng", 
                                     f"Bạn có chắc muốn xóa khách hàng '{self.selected_user}' không?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Xóa thông tin người dùng
            sql_delete_01 = "DELETE FROM tt_nguoithue WHERE MaKhachHang = %s"
            query.execute(sql_delete_01, (self.selected_user,))
            db.commit()
            QMessageBox.information(self, "Xóa", "Khách hàng đã được xóa thành công")
            self.load_data()  # Tải lại bảng sau khi xóa
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def load_selected_row(self, row, column):
        # Lấy dữ liệu từ dòng đã chọn và điền vào các trường nhập liệu
        self.selected_user = self.Table_KH.item(row, 0).text()
        self.MaThue_text.setText(self.Table_KH.item(row, 0).text())
        self.TenKhach_text.setText(self.Table_KH.item(row, 1).text())
        self.Phone_text.setText(self.Table_KH.item(row, 2).text())
        self.DiaChi_text.setText(self.Table_KH.item(row, 3).text())

    def load_data(self):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            query.execute("SELECT MaKhachHang, TenKH, SDT, DiaChi from tt_nguoithue")
            rows = query.fetchall()

            self.Table_KH.setRowCount(len(rows))
            self.Table_KH.setColumnCount(4)
            self.Table_KH.setHorizontalHeaderLabels(["Mã Thuê", "Tên Khách Hàng", "Số điện thoại", "Địa chỉ"])

            for row_num, row_data in enumerate(rows):
                for col_num, col_data in enumerate(row_data):
                    self.Table_KH.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            self.selected_user = None  # Đặt lại lựa chọn

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def clear_inputs(self):
        # Xóa nội dung trong các trường nhập liệu
        self.MaThue_text.clear()
        self.TenKhach_text.clear()
        self.Phone_text.clear()
        self.DiaChi_text.clear()
        self.selected_user = None
