from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
import sys
import xmp_api
from requests import get
from ast import literal_eval
from os import remove, rename, listdir

class Reddit_to_INSPO(QWidget):

    '''
     __     ___    ____  ___    _    ____  _     _____ ____
     \ \   / / \  |  _ \|_ _|  / \  | __ )| |   | ____/ ___|
      \ \ / / _ \ | |_) || |  / _ \ |  _ \| |   |  _| \___ \
       \ V / ___ \|  _ < | | / ___ \| |_) | |___| |___ ___) |
        \_/_/   \_\_| \_\___/_/   \_\____/|_____|_____|____/
    '''

    def __init__(self):
        super().__init__()

        #widgets
        self.text_edit = QPlainTextEdit()
        self.photo_container = QLabel()

        #design variables
        self.title = "Reddit INSPONIZER Parser"
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600


        #fuction variables
        self.output_folder = "inspos/reddit/"
        self.current_file_path = ''
        self.current_photo_path = ''
        self.current_photo_name = ''
        self.articles_and_names = {}

        #get list of files to parse
        self.files_to_parse = listdir("reddit_parsing")
        self.files_to_parse.remove("_scrapped_posts")
        self.file_index = 0

        #functions
        self.initUI()

        self.automode()

    '''
      ____ ____      _    ____  _   _ ___ ____ ____  
     / ___|  _ \    / \  |  _ \| | | |_ _/ ___/ ___| 
    | |  _| |_) |  / _ \ | |_) | |_| || | |   \___ \ 
    | |_| |  _ <  / ___ \|  __/|  _  || | |___ ___) |
     \____|_| \_\/_/   \_\_|   |_| |_|___\____|____/ '''

    def initUI(self):
        #set up grid
        self.generate_grid()

        # set up window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #final steps
        self.setLayout(self.grid)
        self.show() #show window


    def generate_grid(self):
        ARTICLES = xmp_api.get_ARTICLES()  # get all possible articles
        inspo_rows = (len(ARTICLES) * 2) + 1  #rows taken up by inspo forms

        self.grid = QGridLayout()
        self.grid.setSpacing(10)  # make 10px spacing in grid

        # INSPO COMMENT
        self.text_edit.setReadOnly(True)  # make it read-only
        self.text_edit.setPlainText("")  # set text
        self.grid.addWidget(self.text_edit, 0, 0, inspo_rows, 3)

        # INSPO PICTURE
        self.grid.addWidget(self.photo_container, 0, 3, inspo_rows, 4)

        # FILL IN INSPO INFO
        class inspo_article_form:  # create a new class for each article fill in the blank section
            def __init__(self, name):
                self.label = QLabel()  # init the label
                self.line_edit = QLineEdit()  # init the form
                self.name = name  # save the articles name
                self.label.setText(self.name)  # set the label as the articles name

                self.line_edit.textChanged.connect(lambda text: ex.inspo_data_to_dict(text,self.name))  # whenever edited send the new text and name of article

        row = 0
        self.inspo_article_forms = []

        for article in ARTICLES:  # for each article set a label and fill in the box
            if article != "author" and article != "id" and article != "url":
                form = inspo_article_form(article)  # make new inspo article form

                # add article form
                self.grid.addWidget(form.label, row, 7, 1, 3)
                row = row + 1

                self.grid.addWidget(form.line_edit, row, 7, 1, 3)
                row = row + 1

                self.inspo_article_forms.append(form)  # add inspo_article_form to list

        # write button
        write_button = QPushButton()
        write_button.setText("Write INSPO Data")
        write_button.clicked.connect(self.write_inspo)
        self.grid.addWidget(write_button, inspo_rows + 1, 2, 1, 2)

        # temp open button
        open_button = QPushButton()
        open_button.setText("Open file")
        open_button.clicked.connect(lambda: self.open_file(""))
        self.grid.addWidget(open_button, inspo_rows + 1, 4, 1, 2)

        # delete button
        delete_button = QPushButton()
        delete_button.setText("Delete File")
        delete_button.clicked.connect(lambda: self.reset(delete=True))
        self.grid.addWidget(delete_button, inspo_rows + 1, 6, 1, 2)



    '''
     _____ _   _ _   _  ____ _____ ___ ___  _   _ ____  
    |  ___| | | | \ | |/ ___|_   _|_ _/ _ \| \ | / ___| 
    | |_  | | | |  \| | |     | |  | | | | |  \| \___ \ 
    |  _| | |_| | |\  | |___  | |  | | |_| | |\  |___) |
    |_|    \___/|_| \_|\____| |_| |___\___/|_| \_|____/ 

    '''

    @pyqtSlot()
    def write_inspo(self):
        #try:
        xmp_api.dictonary_write(self.current_photo_path, self.articles_and_names) #write info
        rename(self.current_photo_path, self.output_folder + self.current_photo_name) #change file location

        QMessageBox.about(self, "Write Complete", "Your INSPO info has been written to the image and saved") #notify user

        self.reset(delete=True) #reset

        '''except Exception as e:
            QMessageBox.about(self, "Error", "Your inspo info did not write: " + str(e))
            pass'''


    def inspo_data_to_dict(self, text, article): #constantly updates information placed into the form boxes
        if text == "":
            self.articles_and_names.pop(article, None)
        else:
            self.articles_and_names[article] = text



    def open_file(self, file, auto=False):

        try:
            if auto == False:
                self.reset()

            if file == "":
                file = QFileDialog.getOpenFileName(self, "Open File", 'reddit_parsing/')[0]

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

            #add info_dict to dict to write to photo
            self.articles_and_names['id'] = info_dict['id']
            self.articles_and_names['url'] = info_dict['url']
            self.articles_and_names['author'] = info_dict['author']


            self.photo_container.setPixmap(QPixmap(self.current_photo_path).scaled(700, 700, Qt.KeepAspectRatio, Qt.FastTransformation))

        except Exception as e:
            QMessageBox.about(self, "Error", "cannot open file: " + str(e))



    def reset(self, delete=False):

        if delete == True: #if files are to be deleted
            try:
                remove(self.current_file_path) #remove reddit file
                temp_files = listdir(".temp/")
                for file in temp_files:
                    remove('.temp/' + file)  # remove all temp files
            except:
                pass

        #reset variables
        self.current_file_path = ''
        self.current_photo_path = ''
        self.current_photo_name = ''
        self.articles_and_names = {}

        for form in self.inspo_article_forms:  # reset forms
            form.line_edit.setText("")

        self.text_edit.setPlainText("")
        #self.photo_container.setPixmap(QPixmap(self.current_photo_path).scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation))

        self.automode()

    def automode(self):
        if len(self.files_to_parse) > 0:
            file = self.files_to_parse[self.file_index]
            self.open_file('reddit_parsing/' + file, auto=True)
            self.file_index = self.file_index + 1


if __name__ == "__main__":
    # every application must have a QApplication to build on
    app = QApplication(sys.argv)  # brackets are commandline arguements to bring along
    app.setStyleSheet("QPushButton { margin: 10ex; }")  # can add css-like style sheets to program
    ex = Reddit_to_INSPO()
    sys.exit(app.exec_())


