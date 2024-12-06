from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from DB_Connect import create_connection
import mysql.connector

class MatHang_w(QMainWindow):
    def __init__(self, widget):
        super(MatHang_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.load_data()
        # self.table_MatHang.cellClicked.connect(self.load_selected_row)
        self.TimKiem.clicked.connect(self.tim_kiem)  # Nút tìm kiếm
        self.Home.clicked.connect(self.Home_Form)
        self.selected_user = None  # Theo dõi người dùng được chọn để chỉnh sửa/xóa
        

    def load_ui(self):
        uic.loadUi('MatHang.ui', self)

    def Home_Form(self):
        self.widget.setCurrentIndex(1)

    # def load_selected_row(self, row, column):
    #     # Lấy dữ liệu từ dòng đã chọn và điền vào các trường nhập liệu
    #     self.selected_user = self.table_MatHang.item(row, 0).text()
    #     self.TenVay_text.setText(self.table_MatHang.item(row, 1).text())
        
    def load_data(self, search_term=None):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            if search_term:
                query.execute("""
                    SELECT MaSanPham, TenSanPham, SoLuong, GiaNhap, GiaBan, GhiChu 
                    FROM mathang 
                    WHERE TenSanPham LIKE %s OR MaSanPham LIKE %s
                """, (f'%{search_term}%', f'%{search_term}%'))
            else:
                query.execute("""
                    SELECT MaSanPham, TenSanPham, SoLuong, GiaNhap, GiaBan, GhiChu 
                    FROM mathang
                """)

            rows = query.fetchall()

            self.table_MatHang.setRowCount(len(rows))
            self.table_MatHang.setColumnCount(6)
            self.table_MatHang.setHorizontalHeaderLabels(["Mã Sản Phẩm", "Tên Sản Phẩm", "Số Lượng", "Giá Nhập", "Giá Bán", "Ghi Chú"])

            for row_num, row_data in enumerate(rows):
                for col_num, col_data in enumerate(row_data):
                    self.table_MatHang.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            self.selected_user = None  # Đặt lại lựa chọn

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def clear_inputs(self):
        # Xóa nội dung trong các trường nhập liệu
        self.TenVay_text.clear()
        self.selected_user = None

    def tim_kiem(self):
        search_term = self.TenVay_text.text()
        self.load_data(search_term)
