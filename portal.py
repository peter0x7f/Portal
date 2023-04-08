
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout,QHBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
import sys
from PyQt5.QtCore import pyqtSlot
import requests
# from geticon import download_favicon
from PyQt5.QtGui import *

#set arrays global to be accessed from other classes without making removeItem child 
global tab_name 
global tab_link
tab_name = []
tab_link = []



class removeItem(QMainWindow):
    def __init__(self):
        super(removeItem, self).__init__()
 
        # setting title
        self.setWindowTitle("Manage")
        self.con = 0
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
        # calling method
        self.UiComponents()
 
    # method for widgets
    def UiComponents(self):
        # creating a combo box widget
        self.combo_box = QComboBox(self)
 
        # setting geometry of combo box
        self.combo_box.setGeometry(200, 150, 120, 30)
 
        # adding list of items to combo box
        # creating push button
        self.submit = QPushButton("submit", self)
 
        print(self.combo_box.count())
 
        # adding action to button
        self.submit.clicked.connect(self.pressed)
        # setting geometry of the button
        self.submit.setGeometry(200, 200, 200, 30)
        print(self.con)
    def pressed(self):
        if self.con == 0:
            self.main = Window()
            self.con =+ 1
        self.content = self.combo_box.currentText()
        self.main.removewidget(self.content)
        self.combo_box.clear()
        self.hide()
        
class forumlist(QWidget):
    def __init__(self):
        super(forumlist, self).__init__()
 
        # setting title
        self.setWindowTitle("Forum List")
        self.con = 0
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
        # calling method
        self.UiComponents()
 
    # method for widgets
    def UiComponents(self):
        # creating a combo box widget
        self.combo_box = QComboBox(self)
 
        # setting geometry of combo box
        self.combo_box.setGeometry(200, 150, 120, 30)
 
        # adding list of items to combo box
        self.forum_list = ["https://www.reddit.com/","https://forums.craigslist.org/","https://www.quora.com/","http://stackoverflow.com/","https://gamefaqs.gamespot.com/","http://tianya.cn/","http://ign.com/boards","http://4chan.org/","https://www.ultimate-guitar.com/","https://www.xda-developers.com/","https://hackforums.net/","https://darkode.market/","http://slickdeals.net/","http://www.kaskus.co.id/","http://arstechnica.com/","https://bodybuilding.com","http://macrumors.com/","https://moneySavingExpert.com","http://www.teamliquid.net/","http://neogaf.com/","http://2ch.net/","https://ubuntuforums.org/","http://www.thestudentroom.co.uk/","http://sherdog.com/","https://LinuxQuestions.org","http://www.healthboards.com/","http://airliners.net/","http://www.pokecommunity.com/","http://www.pprune.org/","https://bitcointalk.org","https://www.blackhatworld.com/","https://www.phpbb.com/","https://disqus.com/"]
        self.combo_box.addItems(self.forum_list)
        # creating push button
        self.submit = QPushButton("add", self)
        self.combo_box.adjustSize()
        print(self.combo_box.count())
 
        # adding action to button
        self.submit.clicked.connect(self.pressed)
        # setting geometry of the button
        self.submit.setGeometry(200, 200, 200, 30)
        print(self.con)
    def pressed(self):
        if self.con == 0:
            self.main = Window()
            self.con =+ 1
        self.content = self.combo_box.currentText()
        self.forum_list.remove(self.content)
        self.main.pass_args(self.content)
        self.hide()      

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.con = 0
        self.con1 = 0
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #525252;")
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
        self.add_forum.clicked.connect(self.popup)
        self.search_forum = QPushButton('search', self)
        self.search_forum.clicked.connect(self.forums)
        self.rem_forum = QPushButton('-', self)
        self.rem_forum.clicked.connect(self.delet)
        self.rem_forum.clicked.connect(self.ui1)

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.add_forum)
        self.left_layout.addWidget(self.rem_forum)
        self.left_layout.addWidget(self.search_forum)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)

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
        #if tab_link empty:
        #populate tab_link and tab_name with db values
        #   for x in range(len(tab_name)):
        #     create_button(dbs entries)

    def ui1(self):
        self.mainurl.setUrl(QtCore.QUrl(f'https://reddit.com/login'))
        return self.mainurl
    
    def popup(self):
        urldialog, ok = self.geturl.getText(self, "Add Forum","Enter Url:")
        if ok:
            self.seturl.setText(urldialog)
            self.url_parse(self.seturl.text())

    def delet(self):
        print(tab_name)
        if len(tab_name) >= 1:
            if self.con == 0:
                self.thewindow=removeItem()
                self.con=+1
            self.thewindow.combo_box.addItems(tab_name)
            self.thewindow.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle(":/")
            msg.setText("You have nothing to manage yet")
            x = msg.exec_()

    def forums(self):
        if self.con1 == 0:
            self.thewind=forumlist()
            self.con1=+1
        self.thewind.show()

    def pass_args(self, content):
        self.url_parse(content)


    def removewidget(self, name):
        ind = tab_name.index(name)
        tab_name.pop(ind)
        tab_link.pop(ind)
        name = globals()[f'{name}']
        name.deleteLater()
        

    def create_button(self, name, url):
        try:
            download_favicon(url, name)
        except:
            print("..")
        tab_name.append(name)
        tab_link.append(url)
        print(tab_name)
        globals()[f'{name}'] = QPushButton(name, self)
        self.left_layout.addWidget(globals()[f'{name}'])
        globals()[f'{name}'].clicked.connect(lambda: self.mainurl.setUrl(QtCore.QUrl(f'{url}')))
        print(globals()[f'{name}'])
                
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
            print(response.status_code)
            if response.status_code == 200 or response.status_code == 403:
                #parses input for name
                name = name.split('.')
                if "https://www" in name[0]:
                    name = name[1]
                else:
                    name = name[0].split('://')
                    name = name[1][:]
                #call create button class
            response.close()
            if url not in tab_link:
                self.create_button(name, url)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Invalid input")
                msg.setText("You have already entered this URL")
                x = msg.exec_()
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
