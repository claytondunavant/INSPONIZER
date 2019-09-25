from PyQt5.QtWidgets import QWidget
from xmp_api import check_inspo_xmp, inspo_xmp_to_dict

'''class INSPONIZER(QWidget):

    def __init__(self):
        super().__init__()'''

file = "tests/test3.jpg"

if check_inspo_xmp(file):
    print(inspo_xmp_to_dict(file))
