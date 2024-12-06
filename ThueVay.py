from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QComboBox, QPushButton, QTableWidgetItem
from DB_Connect import create_connection
import mysql.connector

class ThueVay_w(QMainWindow):
    def __init__(self, widget):
        super(ThueVay_w, self).__init__()
        self.widget = widget
        self.load_ui()  # Tải giao diện từ file .ui
        self.setup_connections()  # Thiết lập các kết nối sự kiện
        self.load_user_combobox()  # Tải dữ liệu vào ComboBox
        self.Them_TV.clicked.connect(self.ThemTV_Form)
        self.Them_TT.clicked.connect(self.ThemTT_Form)
        self.table_ThueVay.cellClicked.connect(self.load_selected_row)
        self.Clear_Data.clicked.connect(self.Clear_Data_From)
        self.selected_user = None
        self.load_data()

    def load_ui(self):
        uic.loadUi('ThueVay.ui', self)
        # Kết nối các phần tử UI với các thuộc tính trong Python
        self.TenSP_text = self.findChild(QLineEdit, 'TenSP_text')
        self.DonGia_text = self.findChild(QLineEdit, 'DonGia_text')
        self.MaSP_cbx = self.findChild(QComboBox, 'MaSP_cbx')
        self.Home = self.findChild(QPushButton, 'Home')

    def setup_connections(self):
        # Kết nối nút bấm và ComboBox với các phương thức
        self.Home.clicked.connect(self.Home_Form)
        self.MaSP_cbx.currentIndexChanged.connect(self.load_user_from_combobox)

    def Home_Form(self):
        # Chuyển về trang chính (index 1)
        self.widget.setCurrentIndex(1)

    def load_user_combobox(self):
        db = create_connection()  # Tạo kết nối đến cơ sở dữ liệu
        if db is None:
            return

        with db.cursor() as cursor:
            try:
                cursor.execute("SELECT MaSanPham FROM mathang")
                products = cursor.fetchall()

                self.MaSP_cbx.clear()
                self.MaSP_cbx.addItem("Chọn sản phẩm")  # Mục mặc định

                for product in products:
                    self.MaSP_cbx.addItem(product[0])

            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")

        db.close()

    def load_user_from_combobox(self):
        # Cập nhật các trường dựa trên lựa chọn ComboBox
        selected_product = self.MaSP_cbx.currentText()
        if selected_product == "Chọn sản phẩm" or not selected_product:
            self.clear_inputs()
            return

        db = create_connection()  # Tạo kết nối đến cơ sở dữ liệu
        if db is None:
            return

        with db.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT TenSanPham, GiaBan FROM mathang WHERE MaSanPham = %s",
                    (selected_product,)
                )
                product_data = cursor.fetchone()

                if product_data:
                    self.TenSP_text.setText(product_data[0])
                    self.DonGia_text.setText(str(product_data[1]))  # Ensure text fields get strings

            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")

        db.close()

    def load_selected_row(self, row, column):
        # Lấy dữ liệu từ dòng đã chọn và điền vào các trường nhập liệu
        self.selected_user = self.table_ThueVay.item(row, 0).text()
        self.MaThue_text.setText(self.table_ThueVay.item(row, 0).text())
        self.Ten_text.setText(self.table_ThueVay.item(row, 1).text())
        self.SDT_text.setText(self.table_ThueVay.item(row, 2).text())
        self.DiaChi_text.setText(self.table_ThueVay.item(row, 3).text())

    def load_data(self, MaThue=None):
        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            if MaThue:
                query.execute("""
                    SELECT tt_nguoithue.MaKhachHang, tt_nguoithue.TenKH, tt_nguoithue.SDT, tt_nguoithue.DiaChi,
                       thuevay.NgayThue, mathang.MaSanPham, mathang.TenSanPham, thuevay.SoLuong, mathang.GiaBan,thuevay.TrangThai 
                    FROM btlpy.tt_nguoithue 
                    JOIN btlpy.thuevay ON tt_nguoithue.MaKhachHang = thuevay.MaKhachHang
                    JOIN btlpy.mathang ON thuevay.MaSanPham = mathang.MaSanPham
                    WHERE tt_nguoithue.MaKhachHang LIKE %s and tt_nguoithue.MaKhachHang != '';
                """, (f'%{MaThue}%',))
            else:
                query.execute("""
                    SELECT tt_nguoithue.MaKhachHang, tt_nguoithue.TenKH, tt_nguoithue.SDT, tt_nguoithue.DiaChi,
                        thuevay.NgayThue, mathang.MaSanPham, mathang.TenSanPham, thuevay.SoLuong, mathang.GiaBan,thuevay.TrangThai 
                    FROM btlpy.tt_nguoithue 
                    JOIN btlpy.thuevay ON tt_nguoithue.MaKhachHang = thuevay.MaKhachHang 
                    JOIN btlpy.mathang ON thuevay.MaSanPham = mathang.MaSanPham;
                """)

            rows = query.fetchall()
            self.table_ThueVay.setRowCount(len(rows))
            self.table_ThueVay.setColumnCount(10)
            self.table_ThueVay.setHorizontalHeaderLabels(["Mã thuê", "Tên KH", "SDT", "Địa Chỉ", "Ngày Thuê", "Mã Sản Phẩm", "Tên Sản Phẩm", "Số Lượng", "Đơn Giá","Trạng Thái"])

            for row_num, row_data in enumerate(rows):
                for col_num, col_data in enumerate(row_data):
                    self.table_ThueVay.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            self.selected_user = None

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def ThemTT_Form(self):
        MaThue = self.MaThue_text.text()
        Ten = self.Ten_text.text()
        SDT = self.SDT_text.text()
        DiaChi = self.DiaChi_text.text()
        
        if MaThue =='':
            QMessageBox.critical(self, "Lỗi", "Bạn chưa nhập mã thuê")
            return
        if Ten =='':
            QMessageBox.critical(self, "Lỗi", "Bạn chưa nhập tên khách")
            return
        if SDT =='':
            QMessageBox.critical(self, "Lỗi", "Bạn chưa nhập số điện thoại")
            return
        if DiaChi =='':
            QMessageBox.critical(self, "Lỗi", "Bạn chưa nhập địa chỉ")
            return
        
        db = create_connection()
        if db is None:
            return
        
        query = db.cursor()
        try:
                        # Chèn vào bảng tt_nguoithue
            sql_insert_01 = "INSERT INTO tt_nguoithue (MaKhachHang, TenKH, SDT, DiaChi) VALUES (%s, %s, %s, %s)"
            query.execute(sql_insert_01, (MaThue, Ten, SDT, DiaChi))
            db.commit()
            QMessageBox.information(self, "Thêm Thông Tin", "Thông tin mới đã được thêm thành công")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()

    def ThemTV_Form(self):
        MaThue = self.MaThue_text.text()
        SoLuong = self.SoLuong_text.text()
        NgayThue = self.NgayThue_date.date().toString("yyyy-MM-dd")
        MaSP = self.MaSP_cbx.currentText()  # Lấy mã sản phẩm đã chọn từ combobox

        db = create_connection()
        if db is None:
            return

        query = db.cursor()
        try:
            # Chèn vào bảng thuevay
            sql_insert_02 = "INSERT INTO thuevay (MaKhachHang, MaSanPham, NgayThue, SoLuong) VALUES (%s, %s, %s, %s)"
            query.execute(sql_insert_02, (MaThue, MaSP, NgayThue, SoLuong))

            # Update số lượng hàng
            sql_insert_03 = "UPDATE mathang SET SoLuong = SoLuong - %s  WHERE MaSanPham = %s "
            query.execute(sql_insert_03, (SoLuong,MaSP))

            # Update TrangThai
            sql_insert_04 = "UPDATE thuevay SET TrangThai ='Đang Thuê' WHERE MaKhachHang = %s "
            query.execute(sql_insert_04, (MaThue,))


            db.commit()
            QMessageBox.information(self, "Thêm Thông Tin", "Thông tin mới đã được thêm thành công")
            self.load_data(MaThue)  # Tải lại bảng sau khi chèn dữ liệu
            self.clear_inputs()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi cơ sở dữ liệu", f"Lỗi: {err}")
        finally:
            query.close()
            db.close()
            
    def clear_inputs(self):
        self.SoLuong_text.clear()
        self.MaSP_cbx.setCurrentIndex(0)
        self.DonGia_text.clear()
        self.TenSP_text.clear()
        self.selected_user = None
    
    def Clear_Data_From(self):
        self.Ten_text.clear()
        self.SDT_text.clear()
        self.DiaChi_text.clear()
        self.SoLuong_text.clear()
        self.MaSP_cbx.setCurrentIndex(0)
        self.DonGia_text.clear()
        self.TenSP_text.clear()
        self.selected_user = None
        self.load_data()