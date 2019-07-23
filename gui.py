from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
import sys
import xmp_api

class Reddit_to_INSPO(QWidget):

    def __init__(self):
        super().__init__()
        self.articles_and_names = {}
        self.initUI()

    def initUI(self):
        ARTICLES = xmp_api.get_ARTICLES() #get all possible articles
        max_rows = (len(ARTICLES) * 2) + 1 #get the max number of rows

        # set up
        grid = QGridLayout()  # init grid layout object
        grid.setSpacing(10)  # make 10px spacing in grid

        #INSPO COMMENT
        text_edit = QPlainTextEdit()  # add text editor
        text_edit.setReadOnly(True)  # make it read-only
        text_edit.setPlainText("ava is really hecking cute")  # set text

        # corrdinates are (y, x)
        grid.addWidget(text_edit, 0, 1, max_rows, 1)

        #INSPO PICTURE
        label = QLabel()  # set up label
        pixmap = QPixmap('examples/dope.png')  # set up pixmap
        label.setPixmap(pixmap)  # set pixmap on label

        grid.addWidget(label, 0, 2, max_rows, 1)


        # FILL IN INSPO INFO
        class inspo_article_form: #create a new class for each article fill in the blank section
            def __init__(self, name):
                self.label = QLabel() #init the label
                self.line_edit = QLineEdit() #init the form
                self.name = name #save the articles name
                self.label.setText(self.name) #set the label as the articles name

                self.line_edit.textChanged.connect(lambda text: ex.print_inspo_data(text, self.name)) #whenever edited send the new text and name of article

        row = 0
        inspo_article_forms = []

        for article in ARTICLES: #for each article set a label and fill in the box
            form = inspo_article_form(article) #make new inspo article form

            #add article form
            grid.addWidget(form.label, row, 3)
            row = row + 1

            grid.addWidget(form.line_edit, row, 3)
            row = row + 1

            inspo_article_forms.append(form) #add inspo_article_form to list

        #write button
        write_button = QPushButton()
        write_button.setText("Write INSPO Data")

        write_button.clicked.connect(self.write_inspo)

        grid.addWidget(write_button, row, 3)

        #final steps
        self.setLayout(grid) #set up layout
        self.show() #show window

    @pyqtSlot()
    def write_inspo(self):
        xmp_api.dictonary_write('examples/dope.png', self.articles_and_names)

    def print_inspo_data(self, text, article):
        if text == "":
            self.articles_and_names.pop(article, None)
        else:
            self.articles_and_names[article] = text

        print(self.articles_and_names)


if __name__ == "__main__":
    # every application must have a QApplication to build on
    app = QApplication([])  # brackets are commandline arguements to bring along
    app.setStyleSheet("QPushButton { margin: 10ex; }")  # can add css-like style sheets to program
    ex = Reddit_to_INSPO()
    sys.exit(app.exec_())


