import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QLabel, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from prediction import predict_result


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.Browse.clicked.connect(self.open_image)
        self.Test.clicked.connect(self.result)
        self.Quit.clicked.connect(self.close_main_window)

    def open_image(self):
        # display original image
        self.fname = QFileDialog.getOpenFileName(
            self, "Open file", "D:/Desktop/Major_Project_Enhanced/assets/'", ("*.png, *.xmp *.jpg")
        )
        self.filename.setText(self.fname[0])
        pixmap = QPixmap(self.fname[0])
        self.ORIGINAL_IMAGE.setPixmap(pixmap)
        self.ORIGINAL_IMAGE.setPixmap(
            pixmap.scaled(self.ORIGINAL_IMAGE.size(), Qt.IgnoreAspectRatio)
        )
        self.ORIGINAL_IMAGE.show()

    def result(self):
        (prediction, confidence) = predict_result((self.fname))
        self.Result.setText(f"Prediction: {prediction}\nConfidence: {confidence} %")
        
        # display highlighted image
        if prediction == "Authentic" :
            pixmap1 = QPixmap("results/resaved_image.jpg")
            self.PROCESSED_IMAGE.setPixmap(pixmap1)
            self.PROCESSED_IMAGE.setPixmap(
                pixmap1.scaled(self.PROCESSED_IMAGE.size(), Qt.IgnoreAspectRatio)
            )
            self.PROCESSED_IMAGE.show()
        else :
            pixmap1 = QPixmap("results/processed_image.png")
            self.PROCESSED_IMAGE.setPixmap(pixmap1)
            self.PROCESSED_IMAGE.setPixmap(
                pixmap1.scaled(self.PROCESSED_IMAGE.size(), Qt.IgnoreAspectRatio)
            )
            self.PROCESSED_IMAGE.show()

    def close_main_window(self):
        # quit window
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Cancel | QMessageBox.Close,
        )
        if reply == QMessageBox.Close:
            sys.exit()


def main():
    app = QApplication(sys.argv)
    Result = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(Result)
    widget.setFixedWidth(620)
    widget.setFixedHeight(560)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
