from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QDateEdit, QLineEdit, QPushButton, QTableWidget
from DB_Connect import create_connection
import mysql.connector

class ThongKe_w(QMainWindow):
    def __init__(self, widget):
        super(ThongKe_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.Home.clicked.connect(self.Home_Form)
        self.TimKiemTT.clicked.connect(self.tim_kiem)
        self.selected_user = None

    def load_ui(self):
        uic.loadUi('ThongKe.ui', self)
        self.table_ThongTin = self.findChild(QTableWidget, 'table_ThongTin')
        self.NgayDau_date = self.findChild(QDateEdit, 'NgayDau_date')
        self.NgayCuoi_date = self.findChild(QDateEdit, 'NgayCuoi_date')
        self.NhapTT_text = self.findChild(QLineEdit, 'NhapTT_text')
        self.TimKiemTT = self.findChild(QPushButton, 'TimKiemTT')
        self.Home = self.findChild(QPushButton, 'Home')

    def Home_Form(self):
        self.widget.setCurrentIndex(1)

    def load_data(self, ThongTin=None):
        NgayDau = self.NgayDau_date.date().toString("yyyy-MM-dd")
        NgayCuoi = self.NgayCuoi_date.date().toString("yyyy-MM-dd")
        db = create_connection()
        if db is None:
            QMessageBox.critical(self, "Lỗi", "Không thể kết nối tới cơ sở dữ liệu")
            return

        with db.cursor() as query:
            try:
                # 1
                if ThongTin == "Tổng tiền":
                    query.execute("SELECT Tien,Ngay FROM thongke")
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(2)
                    self.table_ThongTin.setHorizontalHeaderLabels([ "Tổng Tiền", "Ngày"])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 2
                elif ThongTin == "Tổng tiền từ ngày":
                    query.execute("SELECT Tien,Ngay FROM thongke WHERE Ngay BETWEEN %s AND %s", (NgayDau, NgayCuoi))
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(2)
                    self.table_ThongTin.setHorizontalHeaderLabels([ "Tổng Tiền", "Ngày"])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 3
                elif ThongTin == "Váy được thuê":
                    query.execute("""SELECT mathang.MaSanPham, mathang.TenSanPham, thuevay.SoLuong,thuevay.NgayThue FROM btlpy.thuevay 
                                        join btlpy.mathang on mathang.MaSanPham = thuevay.MaSanPham 
                                        WHERE  thuevay.TrangThai = 'Đang Thuê' and
                                         thuevay.NgayTra BETWEEN %s AND %s""", (NgayDau, NgayCuoi))
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(4)
                    self.table_ThongTin.setHorizontalHeaderLabels(["Mã Sản phẩm", "Tên Váy", "Số Lượng","Ngày Thuê"])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 4
                elif ThongTin == "Váy Đã Trả":
                    query.execute("""SELECT mathang.MaSanPham, mathang.TenSanPham, thuevay.SoLuong,thuevay.NgayTra FROM btlpy.thuevay 
                                        join btlpy.mathang on mathang.MaSanPham = thuevay.MaSanPham 
                                        WHERE  thuevay.TrangThai = 'Đã Trả' and
                                         thuevay.NgayTra BETWEEN %s AND %s""", (NgayDau, NgayCuoi))
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(4)
                    self.table_ThongTin.setHorizontalHeaderLabels(["Mã Sản phẩm", "Tên Váy", "Số Lượng","Ngày Trả"])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 5
                elif ThongTin == "Tổng váy đang thuê":
                    query.execute("""Select Sum(thuevay.soluong) from btlpy.thuevay where  thuevay.TrangThai = 'Đã Thuê'""")
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(1)
                    self.table_ThongTin.setHorizontalHeaderLabels(["Tổng váy thuê"])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 6 
                elif ThongTin == "Tổng váy đang thuê từ":
                    query.execute("""Select Sum(thuevay.soluong) from btlpy.thuevay where  thuevay.TrangThai = 'Đã Thuê' and thuevay.NgayTra BETWEEN %s AND %s""", (NgayDau, NgayCuoi))
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(1)
                    self.table_ThongTin.setHorizontalHeaderLabels(["Tổng váy thuê" ])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 7 
                elif ThongTin == "Tổng váy đã trả":
                    query.execute("""Select Sum(thuevay.soluong) from btlpy.thuevay where  thuevay.TrangThai = 'Đã Trả'""")
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(1)
                    self.table_ThongTin.setHorizontalHeaderLabels(["Tổng váy trả"])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                # 8
                elif ThongTin == "Tổng váy đã trả từ":
                    query.execute("""Select Sum(thuevay.soluong) from btlpy.thuevay where  thuevay.TrangThai = 'Đã Trả' and thuevay.NgayTra BETWEEN %s AND %s""", (NgayDau, NgayCuoi))
                    rows = query.fetchall()
                    self.table_ThongTin.setRowCount(len(rows))
                    self.table_ThongTin.setColumnCount(1)
                    self.table_ThongTin.setHorizontalHeaderLabels(["Tổng váy trả" ])

                    for row_num, row_data in enumerate(rows):
                        for col_num, col_data in enumerate(row_data):
                            self.table_ThongTin.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
                else:
                    QMessageBox.warning(self, "Không tìm Thấy", "Không tìm thấy thông tin cần tìm")

            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")

        db.close()

    def tim_kiem(self):
        ThongTin = self.NhapTT_text.text().strip()
        self.load_data(ThongTin)
