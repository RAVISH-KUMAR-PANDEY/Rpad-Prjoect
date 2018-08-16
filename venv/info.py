import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import sys


class Ab_class(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(250, 150)
        self.center()
        self.setWindowIcon(QtGui.QIcon('morr.jpg'))
        self.setWindowTitle('About')

        self.l1 = QtWidgets.QLabel("""It's an Simple Editor.\n
    Made for Personal Use.\n
        Made By :~ Ravish Kumar Pandey """,self)
        self.setCentralWidget(self.l1)
        self.l1.setAlignment(QtCore.Qt.AlignCenter)
        self.l1.setStyleSheet("QLabel {background-color: #2B2B2B; color : #F8F8F2}")
        self.statusBar().showMessage("All @Rights@ Reserved.")
        #self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app1 = QtWidgets.QApplication(sys.argv)
    abt = Ab_class()
    sys.exit(app1.exec_())
#################################################
"""
from PyQt4 import QtGui, QtCore
import sys


class Second(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)


class First(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.pushButton = QtGui.QPushButton("click me")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dialog = Second(self)

    def on_pushButton_clicked(self):
        self.dialog.show()


def main():
    app = QtGui.QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())
"""