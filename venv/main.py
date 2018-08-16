import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QAction,QMessageBox,QTextEdit,QFileDialog
from PyQt5.QtGui import QIcon
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import functools
import datetime
from info import *
file_path = None

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.title = 'Made By - Ravish'
        self.left = 400
        self.top = 150
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        #self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage("Made by Python")
        self.setWindowIcon(QIcon("morr.jpg"))
        self.textEdit = QtWidgets.QPlainTextEdit()
        self.setCentralWidget(self.textEdit)
        self.insert = True
        self.fname = 'Untitled.txt'
        self.file_path = ['/', '']
        self.file_type = self.fname.split('.')[-1]
        self.dialog = Ab_class()
        #Menus..................................

        self.menu_bar = self.menuBar()
        self.file_menu()
        self.edit_menu()
        self.format_menu()
        self.about_menu()

        self.default_visual()

        self.Rpad_ui()
        self.show()
    def Rpad_ui(self):
        self.update_cursor()
        self.update_statusbar()
        self.need_saving(False)
        self.setWindowTitle('{} - Rpad'.format(self.fname))
        self.textEdit.textChanged.connect(functools.partial(self.need_saving, True))
        self.textEdit.textChanged.connect(self.update_statusbar)
        self.textEdit.cursorPositionChanged.connect(self.update_statusbar)

    def new_file(self):

        if self.has_changed:
            has_saved = self.save_box(new=True)
        else:
            has_saved = True
        if has_saved:
            self.textEdit.clear()
            self.file_path = './'
            self.fname = 'Untitled'
            self.setWindowTitle("{} - Rpad".format(self.fname))
            self.need_saving(False)

    def closeEvent(self, event):
        if self.has_changed:
            save_ = QMessageBox()
            save_.setIcon(QMessageBox.Question)
            save_.setWindowTitle('Save and Exit')
            save_.setText('The document has been modified.')
            save_.setInformativeText('Do you want to save your changes?')
            save_.setStandardButtons(QMessageBox.Save | QMessageBox.Discard |QMessageBox.Cancel)
            save_.setDefaultButton(QMessageBox.Save)
            save_.setEscapeButton(QMessageBox.Cancel)
            reply = save_.exec_()

            if reply == 2048:
                self.save_file()
                event.accept()
            elif reply == 8388608:
                event.accept()
                # Cancel
            else:
                event.ignore()
        else:
                event.accept()

    def default_visual(self):
        default_palette = self.textEdit.palette()

        default_background_color = QtGui.QColor()
        default_background_color.setNamedColor('#2B2B2B')
        default_palette.setColor(QtGui.QPalette.Base, default_background_color)

        default_font_color = QtGui.QColor()
        default_font_color.setNamedColor('#F8F8F2')
        default_palette.setColor(QtGui.QPalette.Text, default_font_color)

        default_font = QtGui.QFont('Consolas', 13)
        self.textEdit.setFont(default_font)

        self.textEdit.setPalette(default_palette)

    def get_cursor_position(self):
        self.update_cursor()
        cursor_row = self.text_cursor.blockNumber() + 1
        cursor_column = self.text_cursor.columnNumber()
        return cursor_row, cursor_column

    def update_cursor(self):
        self.text_cursor = self.textEdit.textCursor()
        self.textEdit.setTextCursor(self.text_cursor)

    def update_statusbar(self):
        cursor_row, cursor_column = self.get_cursor_position()
        newline_count = self.textEdit.blockCount()
        char_count = self.char_count()
        lines_str = 'lines: ' + str(newline_count)
        chars_str = '  |  chars: ' + str(char_count)
        column_str = '  |  Col: ' + str(cursor_column)
        row_str = '  |  Row: ' + str(cursor_row)

        status_string = lines_str + chars_str + column_str + row_str
        status_lbl = QtWidgets.QLabel(status_string)
        status_lbl.setAlignment(QtCore.Qt.AlignLeft)

        filepath_lbl = QtWidgets.QLabel(str(self.file_path[0]))
        filepath_lbl.setToolTip(str(self.file_path[0]))
        filepath_lbl.setAlignment(QtCore.Qt.AlignLeft)

        custom_status = QtWidgets.QStatusBar()
        custom_status.addWidget(filepath_lbl, stretch=2)
        custom_status.addWidget(status_lbl, stretch=1)
        custom_status.adjustSize()

        self.setStatusBar(custom_status)


    def char_count(self):

        content = self.textEdit.toPlainText()
        content_chars = list(content)
        char_count = len(content_chars)
        return char_count

    def file_menu(self):
        file_menu = self.menu_bar.addMenu('&File')

        new_action = QAction(QtGui.QIcon('new.png'), '&New', self)
        new_action.setStatusTip('Create a new file')
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)

        open_action = QAction(QtGui.QIcon('open.png'), '&Open...', self)
        open_action.setStatusTip('Open File')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_dialog)

        save_action = QAction(QtGui.QIcon('save.png'), '&Save', self)
        save_action.setStatusTip('Save a file')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction(QtGui.QIcon('save_as.png'), 'Save &As', self)
        save_as_action.setStatusTip('Save as.. a file')
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_dialog)

        exit_action = QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setStatusTip('Exit')
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(QtWidgets.qApp.quit)


        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def edit_menu(self):
        edit_menu = self.menu_bar.addMenu('&Edit')

        undo_action = QAction(QtGui.QIcon('undo.png'), '&Undo Typing', self)
        undo_action.setStatusTip('Undo last action')
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo_action)

        cut_action = QAction(QtGui.QIcon('cut.png'), 'Cu&t', self)
        cut_action.setStatusTip('Cut the selection to clipboard')
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.cut_action)

        copy_action = QAction(QtGui.QIcon('copy.png'), '&Copy', self)
        copy_action.setStatusTip('Copy selection to clipboard')
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_action)

        paste_action = QAction(QtGui.QIcon('paste.png'), '&Paste', self)
        paste_action.setStatusTip('Paste from clipboard')
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste_action)

        del_action = QAction(QtGui.QIcon('del.png'), '&Delete', self)
        del_action.setStatusTip('Delete selection')
        del_action.setShortcut('Del')
        del_action.triggered.connect(self.del_action)


        select_all_action = QAction(QtGui.QIcon('select_all.png'), '&Select All', self)
        select_all_action.setStatusTip('Select all lines')
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.select_all_action)

        edit_menu.addAction(undo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(del_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)

    def format_menu(self):
        font_action = QAction(QtGui.QIcon('font.png'), '&Font', self)
        font_action.setStatusTip('Change the document font')
        font_action.triggered.connect(self.font_dialog)

        date_action = QAction(QtGui.QIcon('assets/icons/date.png'), '&Append Date', self)
        date_action.setStatusTip('Insert date and time at cursor location')
        date_action.setShortcut('F5')
        date_action.triggered.connect(self.insert_date)

        format_menu = self.menu_bar.addMenu('&Format')
        format_menu.addAction(font_action)
        format_menu.addAction(date_action)

    def about_menu(self):
        about_action = QAction(QtGui.QIcon('about.png'),'&About',self)
        about_action.setStatusTip('About the Developer.')
        about_action.triggered.connect(self.about_action)

        about_menu = self.menu_bar.addMenu('&About')
        about_menu.addAction(about_action)


    def index_count(self, count):
        return count + 1

    def undo_action(self):
        self.textEdit.undo()

    def cut_action(self):
        self.textEdit.cut()

    def copy_action(self):
        self.textEdit.copy()

    def paste_action(self):
        self.textEdit.paste()

    def del_action(self):
        self.update_cursor()
        self.text_cursor.deleteChar()

    def select_all_action(self):

        self.textEdit.selectAll()

    def insert_date(self):

        today = self.get_datetime()
        self.textEdit.insertPlainText(today)

    def about_action(self):
        self.dialog.show()

    @staticmethod
    def get_datetime():
        date = datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S')
        return date

    def font_dialog(self):
        font, ok = QtWidgets.QFontDialog.getFont(self)
        if ok:
            self.textEdit.setFont(font)

    def need_saving(self, check_):
        self.has_changed = check_
        if self.has_changed:
            self.setWindowTitle('{}* - Rpad'.format(self.fname))
        else:
            self.setWindowTitle('{} - Rpad'.format(self.fname))

    def open_dialog(self):
        if self.has_changed:
            self.save_box(open=True)

        try:
            self.file_path = QFileDialog.getOpenFileName(self, 'Open File', './',
                                                                   filter="All Files(*.*);;Text Files(*.txt)")
            if self.file_path[0]:
                self.fname = (self.file_path[0].split('/'))[-1]

                self.setWindowTitle("{} - Rpad".format(self.fname))

                file_open = open(self.file_path[0], 'r+')
                self.statusBar().showMessage('Open... {}'.format(self.file_path[0]))

                with file_open:
                    data = file_open.read()
                    self.textEdit.setPlainText(data)
                    self.need_saving(False)

        except UnicodeDecodeError as why:
            self.error_box(why)
            pass

    def save_box(self, new=False, open=False):

        reply = QMessageBox().question(self, 'Notepad', "Do you want to save {}".format(self.fname),
                                                 QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.No |
                                                 QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Save)
        if reply == QtWidgets.QMessageBox.Save:
            self.save_file()
            if new:
                return True

        elif reply == QtWidgets.QMessageBox.No:
            if new:
                return True

        elif reply == QtWidgets.QMessageBox.Cancel:
            if new:
                return False
            elif open:
                pass

    def save_dialog(self):
        global file_path
        try:
            save_dialog = QFileDialog()
            save_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_path = save_dialog.getSaveFileName(self, 'Save as... File', './',
                                                    filter='All Files(*.*);; Text Files(*.txt)')
            if file_path[0]:
                self.file_path = file_path
                file_open = open(self.file_path[0], 'w')
                self.fname = (self.file_path[0].split('/'))[-1]
                self.statusBar().showMessage('Saved at: {}'.format(self.file_path[0]))
                self.setWindowTitle("{} - Rpad".format(self.fname))
                with file_open:
                    file_open.write(self.textEdit.toPlainText())
                    self.need_saving(False)

        except FileNotFoundError as why:
            self.error_box(why)
            pass

    def save_file(self):
        global file_path
        try:
            if file_path:
                if (self.file_path[0].split('/')[-1].lower()== self.fname.lower()):

                    file_open = open(self.file_path[0], 'w')
                    self.fname = (self.file_path[0].split('/'))[-1]
                    self.setStatusTip('Saved at: {}'.format(self.file_path[0]))
                    self.setWindowTitle("{} - Rpad".format(self.fname))
                    with file_open:
                        file_open.write(self.textEdit.toPlainText())
                        self.need_saving(False)
                    return

            else:
                self.save_dialog()
        except FileNotFoundError as why:
            self.error_box(why)


    @staticmethod
    def error_box(why):
        errorMessage = QMessageBox()
        errorMessage.setWindowTitle("Error !!")
        errorMessage.setWindowIcon(QMessageBox.Critical)
        errorMessage.setText('An error was found ')
        errorMessage.setInformativeText('%s'%why)
        errorMessage.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())