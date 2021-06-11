from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

from vault import vault
from pwm import pwm


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # set widow titles
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('./images/lock_title.png'))

        # resize window
        self.resize(600, 500)

        # set the logo
        logo_file = QPixmap('./images/vault_title.png')
        logo_file = logo_file.scaled(400, 125)
        self.logo = QLabel(self)
        self.logo.setPixmap(logo_file)
        self.logo.move(145, 15)

        # white line across screen
        sep = QPixmap('./images/line.png')
        sep = sep.scaled(600, 1)
        self.top_line = QLabel(self)
        self.top_line.setPixmap(sep)
        self.top_line.move(-10, 130)
        self.mid_line = QLabel(self)
        self.mid_line.setPixmap(sep)
        self.mid_line.move(-10, 250)
        sep = sep.scaled(1, 400)  # rotate vertically
        self.vert_line = QLabel(self)
        self.vert_line.setPixmap(sep)
        self.vert_line.move(300, 250)

        # select file label
        self.select_file_lbl = QLabel(self)
        self.select_file_lbl.move(10, 153)
        self.select_file_lbl.setText('Select File:')

        # input for folder path
        self.file_path = QLineEdit(self)
        self.file_path.move(70, 150)
        self.file_path.resize(435, 20)

        # private key label
        self.key_lbl = QLabel(self)
        self.key_lbl.move(10, 183)
        self.key_lbl.setText('Key:')

        # input for private key
        self.key_path = QLineEdit(self)
        self.key_path.move(70, 180)
        self.key_path.resize(435, 20)

        # button for file picker
        self.get_file = QPushButton('Choose...', self)
        self.get_file.move(510, 150)
        self.get_file.clicked.connect(self.pick_file)

        # button for file picker
        self.get_key = QPushButton('Choose...', self)
        self.get_key.move(510, 180)
        self.get_key.clicked.connect(self.pick_key)

        # button to encrypt file
        self.encrypt_btn = QPushButton('Encrpyt', self)
        self.encrypt_btn.move(210, 210)
        self.encrypt_btn.clicked.connect(self.encrypt_file)

        # button to decrypt file
        self.decrypt_btn = QPushButton('Decrpyt', self)
        self.decrypt_btn.move(310, 210)
        self.decrypt_btn.clicked.connect(self.decrypt_file)

        # button to delete the file
        self.delete_file_lbl = QLabel(self)
        self.delete_file_lbl.move(10, 210)
        self.delete_file_lbl.setText('Delete File:')
        self.delete_file = QCheckBox(self)
        self.delete_file.move(70, 210)

        # drop down for websites to choose
        self.site_lbl = QLabel(self)
        self.site_lbl.setText('Select Site:')
        self.site_lbl.move(50, 275)
        self.sites_cmb = QComboBox(self)
        self.sites_cmb.move(110, 272)
        self.sites_cmb.resize(150, 20)
        self.sites_cmb.setEditable(True)
        self.populate_sites()
        self.sites_cmb.activated.connect(self.get_cred)

        # label for username
        self.user_lbl = QLabel(self)
        self.user_lbl.setText('Username:')
        self.user_lbl.move(50, 300)
        self.user_val = QLabel(self)
        self.user_val.setText('')
        self.user_val.move(110, 300)

        # label for password
        self.pass_lbl = QLabel(self)
        self.pass_lbl.setText('Password:')
        self.pass_lbl.move(50, 325)
        self.pass_stored_val = QLabel(self)
        self.pass_stored_val.setText('')
        self.pass_stored_val.move(110, 325)

        # button to show password
        self.show_pass_btn = QPushButton('🔦', self)
        self.show_pass_btn.setGeometry(35, 323, 10, 17)
        self.show_pass_btn.setStyleSheet('QPushButton {border:  none}')
        self.show_pass_btn.clicked.connect(self.reveal_stored_pass)

        # label for notes
        self.notes_lbl = QLabel(self)
        self.notes_lbl.setText('Notes:')
        self.notes_lbl.move(50, 350)
        self.notes_val = QLabel(self)
        self.notes_val.setText('')
        self.notes_val.move(110, 350)

        # input for site
        self.site_in_lbl = QLabel(self)
        self.site_in_lbl.move(345, 275)
        self.site_in_lbl.setText('Site:')
        self.site_in = QLineEdit(self)
        self.site_in.move(400, 272)
        self.site_in.resize(150, 20)

        # input for username
        self.user_in_lbl = QLabel(self)
        self.user_in_lbl.move(345, 300)
        self.user_in_lbl.setText('Username:')
        self.user_in = QLineEdit(self)
        self.user_in.move(400, 297)
        self.user_in.resize(150, 20)

        # label for password
        self.new_pass_lbl = QLabel(self)
        self.new_pass_lbl.move(345, 325)
        self.new_pass_lbl.setText('Password:')
        self.new_pass = QLineEdit(self)
        self.new_pass.move(400, 325)
        self.new_pass.resize(150, 20)

        # button to create password
        self.create_pass_btn = QPushButton('🔑', self)
        self.create_pass_btn.setGeometry(330, 323, 12, 17)
        self.create_pass_btn.setStyleSheet('QPushButton {border:  none}')
        self.create_pass_btn.clicked.connect(self.generate_password)

        # label for notes
        self.note_in_lbl = QLabel(self)
        self.note_in_lbl.move(345, 350)
        self.note_in_lbl.setText('Notes:')
        self.note_in = QPlainTextEdit(self)
        self.note_in.move(400, 350)
        self.note_in.resize(150, 50)

        # button to remove from the database
        self.save_pass_btn = QPushButton('Remove', self)
        self.save_pass_btn.setGeometry(70, 410, 85, 20)
        self.save_pass_btn.clicked.connect(self.remove_credentials)

        # button to modify in the database
        self.save_pass_btn = QPushButton('Update', self)
        self.save_pass_btn.setGeometry(160, 410, 85, 20)
        self.save_pass_btn.clicked.connect(self.modify_credentials)

        # button to insert into the database
        self.save_pass_btn = QPushButton('Store', self)
        self.save_pass_btn.setGeometry(425, 410, 85, 20)
        self.save_pass_btn.clicked.connect(self.store_credentials)

    def dark_mode(self):
        # https://gist.github.com/mstuttgart/37c0e6d8f67a0611674e08294f3daef7
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        return dark_palette

    # show the file picker to select file to encrypt
    def pick_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Select File', '', 'All Files (*)')
        if file_name:
            self.file_path.setText(file_name)

    # show the file picker to encrypt key file

    def pick_key(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Select Private Key', '', 'Text File (*.txt)')
        if file_name:
            self.key_path.setText(file_name)

    # run encryption
    def encrypt_file(self):
        if self.file_path.text() != '' and os.path.exists(self.file_path.text()):
            vault('e', self.file_path.text(), self.key_path.text())
        else:
            return
        if 'pwm.db' in self.file_path.text():
            os.remove('pwm.db')
        elif self.delete_file.isChecked():
            os.remove(self.file_path.text())

    # run dectryption
    def decrypt_file(self):
        if self.key_path.text() != '' and self.file_path.text() != '' and self.file_path.text()[-4:] == '.vsa' and os.path.exists(self.file_path.text()):
            vault('d', self.file_path.text(), self.key_path.text())
        else:
            return
        if 'pwm.db.vsa' in self.file_path.text():
            self.populate_sites()
        if self.delete_file.isChecked():
            os.remove(self.file_path.text())

    # get a list of available sites
    def get_sites(self):
        return pwm('l', '', '', '', '')

    # get the users credentials for a selected site
    def get_cred(self):
        if self.sites_cmb.currentText() == '':
            self.clear_stored_fields()
            return
        self.user_val.setText(
            pwm('r', self.sites_cmb.currentText(), '', '', '')[0][1])
        self.pass_stored_val.setText('*****')
        self.notes_val.setText('*****')
        self.user_val.adjustSize()
        self.pass_stored_val.adjustSize()
        self.notes_val.adjustSize()

    # clear the fields showing passwords
    def clear_stored_fields(self):
        self.user_val.setText('')
        self.pass_stored_val.setText('')
        self.notes_val.setText('')

    # toggle between the user's password and the asterisks
    def reveal_stored_pass(self):
        if self.sites_cmb.currentText() == '':
            return
        if self.pass_stored_val.text() == '*****':
            self.pass_stored_val.setText(
                pwm('r', self.sites_cmb.currentText(), '', '', '')[0][2])
            self.notes_val.setText(
                pwm('r', self.sites_cmb.currentText(), '', '', '')[0][3])
        else:
            self.pass_stored_val.setText('*****')
            self.notes_val.setText('*****')
        self.pass_stored_val.adjustSize()
        self.notes_val.adjustSize()

    # create a new randomly generated passsword
    def generate_password(self):
        self.new_pass.setText(vault('p', '', ''))

    # save the credentials into the database
    def store_credentials(self):
        pwm('i', self.site_in.text(), self.user_in.text(),
            self.new_pass.text(), self.note_in.toPlainText())
        temp_val = self.sites_cmb.currentText()
        self.populate_sites()
        self.sites_cmb.setCurrentText(temp_val)
        self.clear_new_fields()

    # modify the credentials in the database
    def modify_credentials(self):
        self.site_in.setText(self.sites_cmb.currentText())
        self.user_in.setText(self.user_val.text())
        self.new_pass.setText(pwm('r', self.site_in.text(), '', '', '')[0][2])
        self.note_in.insertPlainText(
            pwm('r', self.site_in.text(), '', '', '')[0][3])
        self.clear_stored_fields()

    # clear the fields showing passwords
    def clear_new_fields(self):
        self.site_in.setText('')
        self.user_in.setText('')
        self.new_pass.setText('')
        self.note_in.clear()

    # remove the credentials from the database for the selected site
    def remove_credentials(self):
        pwm('d', self.sites_cmb.currentText(), '', '', '')
        self.populate_sites()
        self.pass_stored_val.setText('')
        self.user_val.setText('')
        self.notes_val.clear()

    # provide the sites that are stored in the database
    def populate_sites(self):
        self.sites_cmb.clear()
        self.sites_cmb.addItem('')
        try:
            self.sites_cmb.addItems([site[0] for site in self.get_sites()])
        except TypeError:
            pass


if __name__ == '__main__':
    # instantiate application and create a window
    app = QApplication([])
    app.setStyle('Fusion')
    window = Window()
    app.setPalette(window.dark_mode())  # turn on dark mode
    window.show()
    app.exec()
