from PyQt6.QtWidgets import QMessageBox

class Notification:
    @staticmethod
    def show_alert(title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
