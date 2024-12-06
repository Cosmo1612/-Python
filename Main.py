from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys

from Login import Login_w
from TrangChu import TrangChu_w
from  QLTK import QLTK_w
from MatHang import MatHang_w
from NhapHang import NhapHang_w
from ThueVay import ThueVay_w
from TraVay import TraVay_w
from ThongKe import ThongKe_w
from TTKH import TTKH_w

def main():
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    Login_f = Login_w(widget)
    TrangChu_f = TrangChu_w(widget)
    QLTK_f = QLTK_w(widget)
    MatHang_f = MatHang_w(widget)
    NhapHang_f = NhapHang_w(widget)
    ThueVay_f = ThueVay_w(widget)
    TraVay_f = TraVay_w(widget)
    ThongKe_f = ThongKe_w(widget)
    TTKH_f = TTKH_w(widget)

    widget.addWidget(Login_f)       # Index 0
    widget.addWidget(TrangChu_f)    # Index 1
    widget.addWidget(QLTK_f)        # Index 2
    widget.addWidget(MatHang_f)     # Index 3
    widget.addWidget(NhapHang_f)    # Index 4
    widget.addWidget(ThueVay_f)     # Index 5
    widget.addWidget(TraVay_f)      # Index 6
    widget.addWidget(ThongKe_f)     # Index 7
    widget.addWidget(TTKH_f)        # Index 8
    widget.setCurrentIndex(0)
    widget.setFixedHeight(700)
    widget.setFixedWidth(900)
    widget.show()

    sys.exit(app.exec_())  # Note: exec_() is used in PyQt5

if __name__ == '__main__':
    main()