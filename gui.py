from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class Reddit_to_INSPO(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # set up
        grid = QGridLayout()  # init grid layout object
        grid.setSpacing(10)  # make 10px spacing in grid

        # read only text box
        text_edit = QPlainTextEdit()  # add text editor
        text_edit.setReadOnly(True)  # make it read-only
        text_edit.setPlainText("ava is really hecking cute")  # set text

        # corrdinates are (y, x)
        grid.addWidget(text_edit, 0, 1)

        # picture
        label = QLabel()  # set up label
        pixmap = QPixmap('examples/first_fit.jpg')  # set up pixmap
        label.setPixmap(pixmap)  # set pixmap on label

        grid.addWidget(label, 0, 2)

        #final steps
        self.setLayout(grid) #set up layout
        self.show() #show window

if __name__ == "__main__":
    # every application must have a QApplication to build on
    app = QApplication([])  # brackets are commandline arguements to bring along
    app.setStyleSheet("QPushButton { margin: 10ex; }")  # can add css-like style sheets to program
    ex = Reddit_to_INSPO()
    sys.exit(app.exec_())


