from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QDateEdit, QPushButton, QTableWidget
from DB_Connect import create_connection
import mysql.connector

class TraVay_w(QMainWindow):
    def __init__(self, widget):
        super(TraVay_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.setup_connections()

    def load_ui(self):
        uic.loadUi('TraVay.ui', self)
        # Liên kết các phần tử giao diện với các thuộc tính Python
        self.Nhap_text = self.findChild(QLineEdit, 'Nhap_text')
        self.NgayTra_date = self.findChild(QDateEdit, 'NgayTra_date')
        self.Home = self.findChild(QPushButton, 'Home')
        self.TimKiem_bt = self.findChild(QPushButton, 'TimKiem_bt')
        self.ThanhToan = self.findChild(QPushButton, 'ThanhToan')
        self.table_TT = self.findChild(QTableWidget, 'table_TT')

    def setup_connections(self):
        self.Home.clicked.connect(self.Home_Form)
        self.TimKiem_bt.clicked.connect(self.tim_kiem)
        self.ThanhToan.clicked.connect(self.ThanhToan_Form)

    def Home_Form(self):
        self.widget.setCurrentIndex(1)

    def load_data(self, MaThue=None):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Thực hiện câu truy vấn
            if MaThue:
                query.execute("""
                    SELECT
                        tt_nguoithue.MaKhachHang,
                        tt_nguoithue.TenKH,
                        thuevay.NgayThue,
                        thuevay.NgayTra,
                        mathang.MaSanPham,
                        mathang.TenSanPham,
                        thuevay.SoLuong,
                        mathang.GiaBan
                    FROM
                        btlpy.tt_nguoithue
                    JOIN
                        btlpy.thuevay ON tt_nguoithue.MaKhachHang = thuevay.MaKhachHang
                    JOIN
                        btlpy.mathang ON thuevay.MaSanPham = mathang.MaSanPham
                    WHERE
                        tt_nguoithue.MaKhachHang LIKE %s and TrangThai = 'Đang Thuê';
                """, (f'%{MaThue}%',))

            rows = query.fetchall()
            self.table_TT.setRowCount(len(rows))
            self.table_TT.setColumnCount(8)
            self.table_TT.setHorizontalHeaderLabels(["mã khách hàng", "Tên KH", "Ngày Thuê", "Ngày Trả", "Mã Sản Phẩm", "Tên Sản Phẩm", "Số Lượng", "Đơn Giá"])
            for row_num, row_data in enumerate(rows):
                for col_num, col_data in enumerate(row_data):
                    self.table_TT.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            self.selected_user = None

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def ThanhToan_Form(self):
        MaThue = self.Nhap_text.text().strip()
        NgayTra = self.NgayTra_date.date().toString("yyyy-MM-dd")

        if not MaThue:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập Mã Thuê.")
            return

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Cập nhật ngày trả
            sql_update = "UPDATE thuevay SET NgayTra = %s WHERE MaKhachHang = %s;"
            query.execute(sql_update, (NgayTra, MaThue))
            # Update TrangThai
            sql_update_01 = "UPDATE btlpy.thuevay SET TrangThai ='Đã Trả' WHERE MaKhachHang = %s;"
            query.execute(sql_update_01, (MaThue,))
            # Update TrangThai
            sql_update_02 = """UPDATE btlpy.mathang AS mh
                                JOIN btlpy.thuevay AS tv ON mh.MaSanPham = tv.MaSanPham
                                SET mh.SoLuong = mh.SoLuong + tv.SoLuong
                                WHERE tv.MaKhachHang = %s AND tv.TrangThai = 'Đã Trả';"""
            query.execute(sql_update_02, (MaThue,))

            # Tính tổng tiền
            sql_select = """
                SELECT SUM(
                    DATEDIFF(thuevay.NgayTra, thuevay.NgayThue) * thuevay.SoLuong * mathang.GiaBan
                ) AS TienTong
                FROM
                    btlpy.thuevay
                JOIN
                    btlpy.mathang ON mathang.MaSanPham = thuevay.MaSanPham
                WHERE
                    thuevay.MaKhachHang = %s;
            """
            query.execute(sql_select, (MaThue,))
            result = query.fetchone()

            if result and result[0] is not None:
                TienTong = result[0]
                QMessageBox.information(self, "Thông Tin", f"Tổng tiền thuê: {TienTong:,} VND")
                sql_TK = "INSERT INTO thongke(Tien,Ngay) VALUES (%s,%s)"
                query.execute(sql_TK, (TienTong, NgayTra))

            else:
                QMessageBox.warning(self, "Thông Tin", "Không tìm thấy dữ liệu cho Mã Thuê này hoặc chưa có ngày trả.")

            db.commit()
            self.load_data(MaThue)

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def tim_kiem(self):
        MaThue = self.Nhap_text.text().strip()
        self.load_data(MaThue)
