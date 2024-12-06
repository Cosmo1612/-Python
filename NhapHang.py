from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from DB_Connect import create_connection
import mysql.connector

class NhapHang_w(QMainWindow):
    def __init__(self,widget):
        super(NhapHang_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.ThemMH.clicked.connect(self.ThemMH_Form)
        self.SuaMH.clicked.connect(self.SuaMH_Form)
        self.XoaMH.clicked.connect(self.XoaMH_Form)
        self.Home.clicked.connect(self.Home_Form)
        self.table_NhapHang.cellClicked.connect(self.load_selected_row)
        self.selected_user = None 
        self.load_data()
    
    def Home_Form(self):
        self.widget.setCurrentIndex(1)
    def load_ui(self):
        uic.loadUi('NhapHang.ui', self)

    def ThemMH_Form(self):
        MaSP = self.MaSP_text.text()
        TenSP = self.TenSP_text.text()
        SoLuong = self.SoLuong_text.text()
        GiaNhap = self.GiaNhap_text.text()
        GiaBan = self.GiaBan_text.text()
        GhiChu = self.GhiChu_text.text()

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            sql_insert_01 = "INSERT INTO mathang (MaSanPham,TenSanPham,SoLuong,GiaNhap,GiaBan,GhiChu) VALUES (%s, %s, %s, %s, %s, %s)"
            query.execute(sql_insert_01, (MaSP, TenSP,SoLuong,GiaNhap,GiaBan,GhiChu))
            db.commit()
            QMessageBox.information(self, "Thêm Mặt Hàng", "Mặt Hàng mới đã được thêm thành công")
            self.load_data()  # Reload the table after insertion
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def SuaMH_Form(self):
        MaSP = self.MaSP_text.text()
        TenSP = self.TenSP_text.text()
        SoLuong = self.SoLuong_text.text()
        GiaNhap = self.GiaNhap_text.text()
        GiaBan = self.GiaBan_text.text()
        GhiChu = self.GhiChu_text.text()

        if not self.selected_user:
            QMessageBox.warning(self, "Chỉnh sửa", "Hãy chọn mặt hàng để chỉnh sửa.")
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Cập nhật thông tin người dùng
            sql_update_01 = "UPDATE mathang SET MaSanPham = %s,TenSanPham = %s,SoLuong = %s,GiaNhap = %s,GiaBan = %s,GhiChu = %s WHERE MaSanPham = %s"
            query.execute(sql_update_01, (MaSP, TenSP,SoLuong,GiaNhap,GiaBan,GhiChu, self.selected_user))
            db.commit()
            QMessageBox.information(self, "Chỉnh sửa", "Thông tin mạt hàng đã được cập nhật thành công")
            self.load_data()  # Reload the table after updating
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def XoaMH_Form(self):
        if not self.selected_user:
            QMessageBox.warning(self, "Xóa", "Hãy chọn mặt hàng để xóa.")
            return

        reply = QMessageBox.question(self, "Xóa mặt hàng", 
                                     f"Bạn có chắc muốn xóa mặt hàng '{self.selected_user}' không?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Xóa thông tin người dùng
            sql_delete_01 = "DELETE FROM mathang WHERE MaSanPham = %s"
            query.execute(sql_delete_01, (self.selected_user,))
            db.commit()
            QMessageBox.information(self, "Xóa", "Mặt Hàng đã được xóa thành công")
            self.load_data()  # Reload the table after deletion
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def load_selected_row(self, row, column):
        # Lấy dữ liệu từ dòng đã chọn và điền vào các trường nhập liệu
        self.selected_user = self.table_NhapHang.item(row, 0).text()
        self.MaSP_text.setText(self.table_NhapHang.item(row, 0).text())
        self.TenSP_text.setText(self.table_NhapHang.item(row, 1).text())
        self.SoLuong_text.setText(self.table_NhapHang.item(row, 2).text())
        self.GiaNhap_text.setText(self.table_NhapHang.item(row, 3).text())
        self.GiaBan_text.setText(self.table_NhapHang.item(row, 4).text())
        self.GhiChu_text.setText(self.table_NhapHang.item(row, 5).text())
    def load_data(self):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            query.execute("SELECT MaSanPham, TenSanPham, SoLuong, GiaNhap, GiaBan, GhiChu FROM mathang")
            rows = query.fetchall()
            
            self.table_NhapHang.setRowCount(len(rows))
            self.table_NhapHang.setColumnCount(6)
            self.table_NhapHang.setHorizontalHeaderLabels(["Mã Sản Phẩm", "Tên Sản Phẩm", "Số Lượng", "Giá Nhập","Giá Bán", "Ghi Chú"])

            for row_num, row_data in enumerate(rows):
                for col_num, col_data in enumerate(row_data):
                    self.table_NhapHang.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            self.selected_user = None  # Reset selection

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def clear_inputs(self):
        # Xóa nội dung trong các trường nhập liệu
        self.MaSP_text.clear()
        self.TenSP_text.clear()
        self.SoLuong_text.clear()
        self.GiaNhap_text.clear()
        self.GiaBan_text.clear()
        self.GhiChu_text.clear()
        self.selected_user = None