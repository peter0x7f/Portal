import sqlite3
import os
import geticon

#                       Database Structure                             #
#                             Forums                                   #
# ForumURL - Text Not Null                                   Holds URL #
# Username - Text                                       Holds Username #
# Password - Text                                       Holds password #
# Icon - Text                             Holds file/filepath for file #

#                            AllForums                                 #
# URL - Text Not Null                                        Holds URL #


class forum:

    def __init__(self, URL, Icon, Password, Username):
        if (Password == ""):
            noPass(self, URL, Icon)
        else:
            withPass(self, URL, Icon, Password, Username)
    
    def noPass(self, URL, Icon):
        self.URL = URL
        self.icon = Icon
        
    def withPass(self, URL, Icon, Password, Username):
        self.URL = URL
        self.icon = Icon
        self.Username = Username
        self.Password = Password
        
    def setSecurity(self, Username, Password):
        self.Username = Username
        self.Password = Password


def ReadInDB(cursor):
    forumList = []

    cursor.execute("SELECT * FROM Forums")
    inList = cursor.fetchall()
    for row in inList:
        forumList.append(forum(row[0], row[1], "", ""))#row[2], row[3]))
    return forumList


def AddForum(cursor, URL, list, connection):
    cursor.execute("SELECT * FROM 'Forums' WHERE 'ForumsURL' = ?", URL)
    if (cursor.fetchall().len() > 0):
        return(2)
    cursor.execute("INSERT INTO Forums (ForumURL) VALUES ?", URL)
    connection.commit()
    geticon.download_favicon(URL)
    list.append(forum(URL, os.path.basename(URL) + '.ico', "", ""))
    return list


def UpdateSecurity(cursor, URL, Username, Password, list, connection):
    cursor.execute(
        "UPDATE Forums SET Username = ?, Password = ? WHERE ForumURL = ?",
        (URL, Username, Password))
    connection.commit()
    for x in list:
        if x.URL == URL:
            x.setSecurity(Username, Password)
            break
    return list


def RemoveForum(cursor, URL, list, connection):
    cursor.execute("SELECT 'Icon' FROM 'Forums' WHERE 'ForumsURL' = ?", URL)
    file = cursor.fetchall()
    os.remove(file)
    cursor.execute("DELETE FROM 'Forums' WHERE 'ForumURL' = ?", URL)
    connection.commit()
    
    for i in range(len(list)):
        if list[i].URL == URL:
            list.remove(i)
            break
    return list


def BreakConnection(cursor, connection):
    if connection:
        cursor.close()
        del cursor
