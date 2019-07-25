from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLabel, QGridLayout, QGroupBox, QVBoxLayout, QScrollArea, QLineEdit, QPushButton, QMessageBox, QFileDialog, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from requests import get
from ast import literal_eval
from os import remove, rename, listdir
import sys
import xmp_api


class RedditINSPOParser(QWidget):
    '''displays the comments and photos scrapped from reddit by reddit_bot and allows for the manual embedding of INSPO data
    into said photos'''

    '''
     ___ _   _ ___ _____ 
    |_ _| \ | |_ _|_   _|
     | ||  \| || |  | |  
     | || |\  || |  | |  
    |___|_| \_|___| |_|  

    '''

    #initialization function: runs everytime the class is called
    def __init__(self):
        super().__init__()

        #widgets
        self.text_edit = QPlainTextEdit()
        self.photo_container = QLabel()

        #design variables
        self.title = "Reddit INSPO Parser"

        #fuction variables
        self.output_folder = "inspos/reddit/"
        self.current_file_path = ''
        self.current_photo_path = ''
        self.current_photo_name = ''
        self.articles_and_names = {}

        #get list of files to parse
        self.files_to_parse = listdir("reddit_parsing")
        self.files_to_parse.remove("_scrapped_posts")

        #functions
        self.initUI() #initilialize user interface
        self.automode() #automatically check to see if there are new scrapped reddit posts to parse


    '''
      ____ ____      _    ____  _   _ ___ ____ ____  
     / ___|  _ \    / \  |  _ \| | | |_ _/ ___/ ___| 
    | |  _| |_) |  / _ \ | |_) | |_| || | |   \___ \ 
    | |_| |  _ <  / ___ \|  __/|  _  || | |___ ___) |
     \____|_| \_\/_/   \_\_|   |_| |_|___\____|____/ '''

    def initUI(self):
        #set up grid
        self.ui_window()

        # set up window
        self.setWindowTitle(self.title)

        #final steps
        self.setLayout(self.grid)
        self.show() #show window


    def ui_window(self):
        #variables
        self.ARTICLES = xmp_api.get_ARTICLES()  # get all possible articles
        self.inspo_rows = (len(self.ARTICLES) * 2) + 1  #rows taken up by inspo forms

        #make grid that organizes the widgets
        self.grid = QGridLayout()
        self.grid.setSpacing(10) #make 10px spacing in grid

        #make the text box to hold the comment information
        self.ui_comment_textbox()

        #make the area to hold the photo from the reddit post
        self.ui_fit_photo()

        #make the forms to place INSPO information from comments into
        self.ui_inspo_info_forms()

        #make the bottom buttons to write, open, and delete saved reddit posts
        self.ui_bottom_buttons()

    def ui_comment_textbox(self):
        #make the text box to hold the comment information
        self.text_edit.setReadOnly(True)  # make it read-only
        self.text_edit.setPlainText("")  # set text
        self.grid.addWidget(self.text_edit, 0, 0, self.inspo_rows, 3)

    def ui_fit_photo(self):
        #make the area to hold the photo from the reddit post
        self.grid.addWidget(self.photo_container, 0, 3, self.inspo_rows, 4)

    def ui_inspo_info_forms(self):
        #make the forms to place INSPO information from comments into
        inspo_form_box = QGroupBox()  # make group box for inspo forms
        form_layout = QVBoxLayout()
        inspo_form_box.setLayout(form_layout)  # make the group box have a vertical layout

        form_scroll = QScrollArea()  # create scroll area
        form_layout.addWidget(form_scroll)  # add scroll area to box
        form_scroll.setWidgetResizable(True)
        form_scroll_content = QWidget(form_scroll)  # make a widget to hold the scroll area content

        form_scroll_layout = QVBoxLayout(form_scroll_content)
        form_scroll_content.setLayout(form_scroll_layout) #give a layout to the content

        '''class for each possible article of clothing
        This is done so there is a stored article name with each unique text box'''
        class inspo_article_form:
            def __init__(self, name):
                self.label = QLabel()  # init the label
                self.line_edit = QLineEdit()  # init the form
                self.name = name  # save the articles name
                self.label.setText(self.name)  # set the label as the articles name

                self.line_edit.textChanged.connect(lambda text: ex.inspo_data_to_dict(text,
                                                                                      self.name))  # whenever edited send the new text and name of article

        row = 0 #current row
        self.inspo_article_forms = [] #store all the inspo_article_form objects in a list

        for article in self.ARTICLES:  # for each article set a label and fill in the box
            if article != "author" and article != "id" and article != "url": #if it is not a default article
                form = inspo_article_form(article)  # make new inspo article form

                # add article form
                form_scroll_layout.addWidget(form.label) #title
                row = row + 1 #go down a row

                form_scroll_layout.addWidget(form.line_edit) #text box
                row = row + 1 #go down a row

                self.inspo_article_forms.append(form) # add inspo_article_form to list'

        form_scroll.setWidget(form_scroll_content) #add the content to the scroll area

        self.grid.addWidget(inspo_form_box, 0, 7, self.inspo_rows, 3)

    def ui_bottom_buttons(self):
        # write button
        write_button = QPushButton()
        write_button.setText("Write INSPO Data")
        write_button.clicked.connect(self.write_inspo) #when clicked write the inspo data and save the image
        self.grid.addWidget(write_button, self.inspo_rows + 1, 2, 1, 2)

        # temp open button
        open_button = QPushButton()
        open_button.setText("Open file")
        open_button.clicked.connect(lambda: self.open_file("")) #when clicked open the browser
        self.grid.addWidget(open_button, self.inspo_rows + 1, 4, 1, 2)

        # delete button
        delete_button = QPushButton()
        delete_button.setText("Delete File")
        delete_button.clicked.connect(lambda: self.reset(delete=True)) #when clicked reset the program and delete the current photo and file
        self.grid.addWidget(delete_button, self.inspo_rows + 1, 6, 1, 2)




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


            self.photo_container.setPixmap(QPixmap(self.current_photo_path).scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation))

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
        if len(self.files_to_parse) > 0: #if there are files to parse
            file = self.files_to_parse[0]
            self.open_file('reddit_parsing/' + file, auto=True) #open file in auto mode
            self.files_to_parse.remove(file) #remove file form files to parse


if __name__ == "__main__":
    # every application must have a QApplication to build on
    app = QApplication(sys.argv) #QApplication runs with system arguements
    app.setStyleSheet("QPushButton { margin: 10ex; }")  # can add css-like style sheets to program
    ex = RedditINSPOParser() #start Reddit INSPO Parser
    sys.exit(app.exec_())


