from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class TrangChu_w(QMainWindow):
    def __init__(self, widget):
        super(TrangChu_w, self).__init__()
        self.widget = widget
        self.load_ui()
        self.QLTK.clicked.connect(self.QLTK_Form)
        self.MatHang.clicked.connect(self.MatHang_form)
        self.NhapHang.clicked.connect(self.NhapHang_form)
        self.ThueVay.clicked.connect(self.ThueVay_form)
        self.TraVay.clicked.connect(self.TraVay_form)
        self.ThongKe.clicked.connect(self.ThongKe_form)
        self.TTKH.clicked.connect(self.TTKH_form)
        self.DX_btn.clicked.connect(self.login_form)


    def load_ui(self):
        uic.loadUi('TrangChu.ui', self)
    def login_form(self):
        self.widget.setCurrentIndex(0)

    def QLTK_Form(self):
        self.widget.setCurrentIndex(2)  # Chuyển đến QLTK
    def MatHang_form(self):
        self.widget.setCurrentIndex(3)  # Chuyển đến MatHang
    def NhapHang_form(self):
        self.widget.setCurrentIndex(4)  # Chuyển đến 
    def ThueVay_form(self):
        self.widget.setCurrentIndex(5)  # Chuyển đến
    def TraVay_form(self):
        self.widget.setCurrentIndex(6)  # Chuyển đến
    def ThongKe_form(self):
        self.widget.setCurrentIndex(7)  # Chuyển đến
    def TTKH_form(self):
        self.widget.setCurrentIndex(8)  # Chuyển đến