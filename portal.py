# import necessary pyqt5 libraries
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# import other required libraries
import sys
import os
import sqlite3
import requests
import atexit

# import files
import DatabaseInteraction
import GetIcon
import ForumClass

# TG start
# connect to the database check for connection and create a cursor
connection = sqlite3.connect("PortalDB.db")
if connection:
    cursor = connection.cursor()
else:
    msg = QMessageBox()
    msg.setWindowTitle("Database Error")
    msg.setText("Unable to connect with the database.")
    x = msg.exec_()
    if returnValue == QMessageBox.Ok:
        sys.exit()

# TG end

# MM start

# set arrays global to be accessed from other classes without making removeItem child
global tab_name
global tab_link
global tab_icon
tab_name = []
tab_link = []
tab_icon = []


# class to allow the popup windows without it being a child class.
# required to be in one class to avoid segfault
class RemoveNSearch(QWidget):

    # instantiates the window
    def __init__(self):
        super(RemoveNSearch, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(100, 100, 600, 400)
        self.added = 0
        self.con = 0
        self.submit = QPushButton("submit", self)
        self.submit.hide()
        self.add = QPushButton("Add", self)
        self.add.hide()
        self.combo_box = QComboBox(self)
        # removes the red 'x' button on window to avoid deleting the QWidget
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint
                            | Qt.WindowMinMaxButtonsHint)

        self.forum_list = [
            "https://www.reddit.com/", "https://forums.craigslist.org/",
            "https://www.quora.com/", "https://stackoverflow.com/",
            "https://gamefaqs.gamespot.com/", "https://ign.com/boards",
            "https://4chan.org/", "https://www.ultimate-guitar.com/",
            "https://www.xda-developers.com/", "https://hackforums.net/",
            "https://slickdeals.net/", "https://arstechnica.com/",
            "https://macrumors.com/", "https://www.teamliquid.net/",
            "https://neogaf.com/", "https://ubuntuforums.org/",
            "https://www.thestudentroom.co.uk/", "https://sherdog.com/",
            "https://www.healthboards.com/", "https://airliners.net/",
            "https://www.pokecommunity.com/", "https://www.pprune.org/",
            "https://bitcointalk.org", "https://www.blackhatworld.com/",
            "https://www.phpbb.com/", "https://disqus.com/"
        ]

        # for regularity the search function is loaded.
        self.setToolTip("Use the dropdown menu to search a list of forums.")
        # setting title
        self.setWindowTitle("Forum List")
        self.con = 0
        # calling method
        self.UiSearch()
        self.cancel = QPushButton("cancel", self)
        self.cancel.clicked.connect(self.CancelAction)
        # setting geometry of the button
        self.cancel.setGeometry(150, 200, 100, 30)

    # creates window contents for remove feature
    def UiRemove(self):
        #self.combo_box = QComboBox(self)

        # setting geometry of combo box
        self.combo_box.show()
        self.combo_box.setGeometry(200, 150, 120, 30)
        # adding list of items to combo box
        # creating push button
        #self.submit = QPushButton("submit", self)
        self.submit.show()
        self.submit.setText("submit")
        # adding action to button

        self.submit.clicked.connect(self.PressRemove)
        # setting geometry of the button
        #self.submit.setGeometry(300, 200, 100, 30)

    # creates window contents for search feature
    def UiSearch(self):
        # creating a combo box widget
        #self.combo_box = QComboBox(self)

        # setting geometry of combo box
        self.combo_box.show()
        self.combo_box.setGeometry(200, 150, 120, 30)

        # adding list of items to combo box
        """# remove forums from forum_list which are already found.
        for item in tab_link:
            if item in self.forum_list:
                self.forum_list.remove(item)
            elif (item + '/') in self.forum_list:
                self.forum_list.remove(item + "/")
        """
        self.combo_box.addItems(self.forum_list)
        # creating push button
        self.add.show()
        self.combo_box.adjustSize()

        # adding action to button
        self.add.clicked.connect(self.PressSearch)
        # setting geometry of the button
        #self.add.setGeometry(400, 200, 100, 30)

    def CancelAction(self):
        self.hide()

    # function to add functionality to the remove button.
    def PressRemove(self):
        if self.con == 0:
            self.main = Window()
            self.main.setAttribute(Qt.WA_AlwaysShowToolTips)
            self.main.setAttribute(Qt.WA_QuitOnClose, False)
            self.con = +1
        self.content = self.combo_box.currentText()
        #if self.content in tab_name:
        #    self.forum_list.append(tab_link[tab_name.index(self.content)])
        self.main.removewidget(self.content)
        self.combo_box.clear()
        self.hide()

    # function to add functionality to search button.
    def PressSearch(self):
        if self.con == 0:
            self.main = Window()
            self.main.setAttribute(Qt.WA_AlwaysShowToolTips)
            self.main.setAttribute(Qt.WA_QuitOnClose, False)
            self.con = +1
        if self.added != len(self.forum_list):
            self.content = self.combo_box.currentText()
            self.added += 1
            #self.forum_list.remove(self.content)
            ex.url_parse(self.content)
            self.add.hide()
            self.combo_box.clear()
            self.hide()
        else:
            msg = QMessageBox()
            msg.setWindowTitle(":/")
            msg.setText("No Forum Selected")
            x = msg.exec_()

    # TG start
    # function to change window contents
    def ChangeType(self, type):
        # clears reused variables
        self.combo_box.clear()
        if type == 0:
            self.add.setGeometry(900, 900, 100, 30)
            self.submit.setGeometry(400, 200, 100, 30)
            # changes the contents to remove functionality
            self.setWindowTitle("Manage")
            self.setToolTip("Use the dropdown menu to remove a saved forum.")
            self.UiRemove()
        else:
            self.add.setGeometry(400, 200, 100, 30)
            self.submit.setGeometry(900, 900, 100, 30)
            # changes the contents to the search functionality
            self.setToolTip(
                "Use the dropdown menu to search a list of forums.")
            # setting title
            self.setWindowTitle("Forum List")
            self.con = 0
            # calling method
            self.UiSearch()

    # TG end


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.con = 0
        self.con1 = 0
        self.initUI()

    # sets up ui.
    def initUI(self):
        self.setStyleSheet("background-color: #423F3E;")  # 525252;")
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

        self.left_widget = QScrollArea()
        self.left_widget.setWidgetResizable(True)

        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)
        self.left_layout.setSpacing(30)
        # MM end
        # TG start

        self.uiBox = QHBoxLayout()

        # add forum button
        self.addButton = QPushButton("", self)
        self.addButton.setIcon(QIcon("UI_Icons/AddButton.png"))
        self.addButton.setIconSize(QSize(30, 30))
        self.addButton.setStyleSheet(
            "border-radius : 15; border : 0px solid black")
        self.addButton.clicked.connect(self.popup)

        # remove forum button
        self.minusButton = QPushButton("", self)
        self.minusButton.setIcon(QIcon("UI_Icons/MinusButton.png"))
        self.minusButton.setIconSize(QSize(35, 35))
        self.minusButton.setStyleSheet(
            "border-radius : 15; border : 0px solid black")
        self.minusButton.clicked.connect(self.delet)
        self.minusButton.clicked.connect(self.ui1)

        # search for forums button
        self.searchButton = QPushButton("", self)
        self.searchButton.setIcon(QIcon("UI_Icons/SearchButton.png"))
        self.searchButton.setIconSize(QSize(30, 30))
        self.searchButton.setStyleSheet(
            "border-radius : 15; border : 0px solid black")
        self.searchButton.clicked.connect(self.forums)

        # add buttons to the horizontal box widget
        self.uiBox.addWidget(self.addButton)
        self.uiBox.addWidget(self.minusButton)
        self.uiBox.addWidget(self.searchButton)

        # make left_layout scrollable and add the uiBox to it.
        self.left_layout.addLayout(self.uiBox)
        self.inner = QFrame(self.left_widget)
        self.inner.setLayout(self.left_layout)
        self.left_widget.setWidget(self.inner)
        # TG end

        # MM start
        self.tab1 = self.ui1()
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        # add tab to right widget
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
        # MM end

        # TG start

        # creates the popup window
        self.PopupWindow = RemoveNSearch()
        self.PopupWindow.hide()

        # read in the database if the lists are empty
        if len(tab_link) == 0 and len(tab_name) == 0:
            forumList = DatabaseInteraction.ReadInDB(cursor)
            for item in forumList:
                self.create_button(item.name, item.URL, 1)
        # TG end

    # MM start
    # set initial view to Home.html
    def ui1(self):
        self.mainurl.load(QtCore.QUrl.fromLocalFile(os.getcwd() +
                                                    '/Home.html'))
        return self.mainurl

    # opens popup window to input the url
    def popup(self):
        urldialog, ok = self.geturl.getText(self, "Add Forum", "Enter Url:")
        if ok:
            self.seturl.setText(urldialog)
            self.url_parse(self.seturl.text())

    # helper function to remove items from the buttons, list
    def delet(self):
        try:
            self.PopupWindow
        except:
            self.PopupWindow = RemoveNSearch()
        if len(tab_name) >= 1:
            if self.con == 0:

                self.PopupWindow.ChangeType(0)
                self.closeEvent
                self.con = +1
            self.PopupWindow.combo_box.addItems(tab_name)
            self.PopupWindow.combo_box.adjustSize()
            self.PopupWindow.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle(":/")
            msg.setText("You have nothing to manage yet")
            x = msg.exec_()

    # MM end

    # TG start
    def closeEvent(self, event):
        try:
            if ex.PopupWindow.main.isWindow():
                ex.PopupWindow.destroy(True, True)
            ex.PopupWindow.close()
        except:
            print("PopupWindow")
        app.quit()

    # TG end

    # MM start
    def forums(self):
        if self.con1 == 0:
            self.PopupWindow.ChangeType(1)

            self.con1 = +1
        self.PopupWindow.combo_box.addItems(self.PopupWindow.forum_list)
        self.PopupWindow.show()

    # removes the button, removes from list, and deletes from database
    def removewidget(self, name):
        ind = tab_name.index(name)

        # removes from database
        DatabaseInteraction.RemoveForum(cursor, tab_link[ind], connection)

        # deletes from list
        tab_name.pop(ind)
        tab_link.pop(ind)
        tab_icon.pop(ind)

        # deletes button.
        name = globals()[f'{name}']
        name.deleteLater()

    def create_button(self, name, url, action):
        path = GetIcon.download_favicon(url, name)
        if action == 0:
            DatabaseInteraction.AddForum(cursor, url, path, name, connection)
        tab_name.append(name.lower())
        tab_link.append(url)
        tab_icon.append(path)
        self.temp = len(tab_name)
        try:
            globals()[f'{name}'] = QPushButton(name, self)
            globals()[f'{name}'].setStyleSheet(
                "border-radius : 25; border : 0px solid black")
            globals()[f'{name}'].setIcon(QIcon(path))
            globals()[f'{name}'].setIconSize(QSize(50, 50))
            self.left_layout.addWidget(globals()[f'{name}'])

            globals()[f'{name}'].clicked.connect(
                lambda: self.mainurl.setUrl(QtCore.QUrl(f'{url}')))
        except:
            print("button err")
            #pass

    @pyqtSlot()
    def url_parse(self, urlval):

        name = urlval
        url = urlval

        #checks if http to convert to https
        if "http://" in url:
            url = url.replace("http://", "https://")
            name = url

        #checks if user entered https instead and if not adds it to their url
        elif "https://" not in url:
            url = "https://" + url
            name = url

        #includes relavant headers
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        #check if url is valid
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200 or response.status_code == 403:
                #parses input for name
                name = name.split('.')
                if "https://www" in name[0]:
                    name = name[1]
                else:
                    name = name[0].split('://')
                    name = name[1][:]
            response.close()
            if url not in tab_link:
                #call create button class
                self.create_button(name, url, 0)
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
        # MM end


# MM started but TG debugged and added to the function
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Window()
    atexit.register(DatabaseInteraction.BreakConnection, cursor, connection)
    atexit.register(ex.deleteLater)
    atexit.register(app.deleteLater)

    ex.show()
    sys.exit(app.exec_())
