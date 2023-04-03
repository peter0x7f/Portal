from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
import sys
import os
import sqlite3
import DatabaseInteraction
import geticon
from PyQt5.QtCore import pyqtSlot
import requests

connection = sqlite3.connect("PortalDB.db")
if connection:
    cursor = connection.cursor()
else:
    msg = QMessageBox()
    msg.setWindowTitle("Database Error")
    msg.setText("Unable to connect with the database.")
    x = msg.exec_()

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()
    def initUI(self):
        self.tab_name = []
        self.tab_link = []
        self.theapp = QApplication(['', '--no-sandbox'])
        self.mainurl = QWebEngineView()
        # set the title of main window
        self.setWindowTitle('Portal')

        # set the size of window
        self.seturl = QLineEdit()
        self.geturl = QInputDialog()
        self.Width = 1600
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)


        self.add_forum = QPushButton('+', self)
        self.add_forum.move(0, int(0.618 * self.Width))
        self.add_forum.clicked.connect(self.popup)
        
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.add_forum)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)
  
        # for x in range(len(self.tab_)):
        #     self.right_widget.addTab(QWidget(), self.tab_index[x][0])

        self.tab1 = self.ui1()
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')
        #fix layout feature
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def ui1(self):
        self.mainurl.setUrl(QtCore.QUrl(f'https://reddit.com'))
        return self.mainurl

    def ui2(self, url):
        self.mainurl.setUrl(QtCore.QUrl(f'{url}'))
        return self.mainurl
    
    def popup(self):
        urldialog, ok = self.geturl.getText(self, "Add Forum","Enter Url:")
        if ok:
            self.seturl.setText(urldialog)
            self.url_parse(self.seturl.text())
            
    #dynamically sets button name and sets to params defined in ui2
    def create_button(self, name, url):
                path = GetIcon.download_favicon(url, name)
                DatabaseInteraction.AddForum(cursor, url, path, name, ls, connection)
                self.tab_name.append(name)
                self.tab_link.append(url)
                self.temp = len(self.tab_name)
                globals()[f'{name}'] = QPushButton(name, self)
                globals()[f'{name}'].setStyleSheet("border-radius : 25; border : 0px solid black")
                globals()[f'{name}'].setIcon(QIcon(path))
                globals()[f'{name}'].setIconSize(QSize(50, 50))
                self.left_layout.addWidget(globals()[f'{name}'])
                globals()[f'{name}'].clicked.connect(lambda: self.ui2(url))
                
    @pyqtSlot()
    def url_parse(self, urlval):

        name = urlval
        url = urlval 

        #checks if http to convert to https
        if "http://" in url:
            url = url.replace("http://","https://")
            name = url

        #checks if user entered https instead and if not adds it to their url
        elif "https://" not in url:
            url = "https://"+url
            name = url

        #includes relavant headers 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        #check if url is valid
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                #parses input for name
                name = name.split('.')
                if "https://www" in name[0]:
                    name = name[1]
                else:
                    name = name[0].split('://')
                    name = name[1][:]
                self.create_button(name, url)
            response.close()
        except:
            #alert user they entered invalid input
            msg = QMessageBox()
            msg.setWindowTitle("Invalid input")
            msg.setText("The URL you entered is invalid, please try again.")
            x = msg.exec_()

 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
    
