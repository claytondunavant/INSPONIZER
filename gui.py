from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
import sys
import xmp_api
from requests import get
from ast import literal_eval
from os import remove, rename

class Reddit_to_INSPO(QWidget):

    def __init__(self):
        super().__init__()

        #widgets
        self.text_edit = QPlainTextEdit()
        self.photo_container = QLabel()

        #variables
        self.current_file_path = ''
        self.current_photo_path = ''
        self.current_photo_name = ''
        self.articles_and_names = {}

        #functions
        self.initUI()

    def initUI(self):
        ARTICLES = xmp_api.get_ARTICLES() #get all possible articles
        max_rows = (len(ARTICLES) * 2) + 1 #get the max number of rows

        # set up
        grid = QGridLayout()  # init grid layout object
        grid.setSpacing(10)  # make 10px spacing in grid

        #INSPO COMMENT
        self.text_edit.setReadOnly(True)  # make it read-only
        self.text_edit.setPlainText("")  # set text
        grid.addWidget(self.text_edit, 0, 1, max_rows, 1)

        #INSPO PICTURE
        grid.addWidget(self.photo_container, 0, 2, max_rows, 1)


        # FILL IN INSPO INFO
        class inspo_article_form: #create a new class for each article fill in the blank section
            def __init__(self, name):
                self.label = QLabel() #init the label
                self.line_edit = QLineEdit() #init the form
                self.name = name #save the articles name
                self.label.setText(self.name) #set the label as the articles name

                self.line_edit.textChanged.connect(lambda text: ex.inspo_data_to_dict(text, self.name)) #whenever edited send the new text and name of article

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

        #temp open button
        open_button = QPushButton()
        open_button.setText("Open file")
        open_button.clicked.connect(lambda: self.open_file("reddit_parsing/cg6h3j"))
        grid.addWidget(open_button, row + 1, 3)

        #final steps
        self.setLayout(grid) #set up layout
        self.show() #show window

    @pyqtSlot()
    def write_inspo(self):
        xmp_api.dictonary_write(self.current_photo_path, self.articles_and_names)
        rename(self.current_photo_path, "examples/" + self.current_photo_name)

        remove(self.current_file_path)
        self.current_file_path = ''
        self.current_photo_path = ''
        self.current_photo_name = ''
        self.articles_and_names = {}


    def inspo_data_to_dict(self, text, article):
        if text == "":
            self.articles_and_names.pop(article, None)
        else:
            self.articles_and_names[article] = text

    def open_file(self, file):
        self.current_file_path = file

        # get info dict from file
        info_dict = {}
        with open(file, "r") as f:
            info_dict = literal_eval(f.readline())

        #get comments from file
        comments = ""
        with open(file, 'r') as f:
            f.readline() #skip first line
            comments = f.read() #read the rest

        #place comments in their box
        self.text_edit.setPlainText(comments)

        #download a photo into .temp
        photo_url = info_dict["photoURL"]

        #find the file extension
        extension = ''
        for i in range(len(photo_url) - 1, -1,  -1): #loop backwards
            extension = extension + photo_url[i]
            if photo_url[i] == '.':
                extension = extension[::-1] #make it backwards
                break

        #download photo
        r = get(photo_url)
        self.current_photo_name = info_dict["id"] + extension
        self.current_photo_path = '.temp/' + info_dict["id"] + extension
        open(self.current_photo_path, 'wb').write(r.content)


        self.photo_container.setPixmap(QPixmap(self.current_photo_path).scaled(self.width() / 2, self.height() / 2, Qt.KeepAspectRatio, Qt.FastTransformation))


if __name__ == "__main__":
    # every application must have a QApplication to build on
    app = QApplication([])  # brackets are commandline arguements to bring along
    app.setStyleSheet("QPushButton { margin: 10ex; }")  # can add css-like style sheets to program
    ex = Reddit_to_INSPO()
    sys.exit(app.exec_())


