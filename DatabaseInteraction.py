import sqlite3
import os
import geticon

#                       Database Structure                             #
#                             Forums                                   #
# ForumURL - Text Not Null                                   Holds URL #
# Username - Text                                       Holds Username #
# Password - Text                                       Holds password #
# Icon - Text                             Holds file/filepath for file #
# Name - Text                              Holds the name of the forum #

#                            AllForums                                 #
# URL - Text Not Null                                        Holds URL #


class forum:

    def noPass(self, URL, Icon, Name):
        self.URL = URL
        self.icon = Icon
        self.name = Name

    def withPass(self, URL, Icon, Password, Username):
        self.URL = URL
        self.icon = Icon
        self.Username = Username
        self.Password = Password
        self.name = Name

    def setSecurity(self, Username, Password):
        self.Username = Username
        self.Password = Password

    def __init__(self, URL, Icon, Password, Username, Name):
        self.URL = URL
        self.icon = Icon
        self.Username = Username
        self.Password = Password
        self.name = Name
        #if (Password == ""):
        #    noPass(self, URL, Icon)
        #else:
        #    withPass(self, URL, Icon, Password, Username)

def ReadInDB(cursor):
    forumList = []

    cursor.execute("SELECT * FROM Forums")
    inList = cursor.fetchall()
    for row in inList:
        forumList.append(forum(row[0], row[1], row[2], row[3], row[4]))
    return forumList


def AddForum(cursor, URL, path, name, ls, connection):
    cursor.execute(
        "INSERT INTO Forums (ForumURL, Icon, Name) VALUES (?, ?, ?)",
        (URL, path, name))
    connection.commit()

    ls.append(forum(URL, path, "", "", name))
    return ls


def UpdateSecurity(cursor, URL, Username, Password, ls, connection):
    cursor.execute(
        "UPDATE Forums SET Username = ?, Password = ? WHERE ForumURL = ?",
        (URL, Username, Password))
    connection.commit()
    for x in ls:
        if x.URL == URL:
            x.setSecurity(Username, Password)
            break
    return ls


def RemoveForum(cursor, URL, ls, connection):
    cursor.execute("SELECT 'Icon' FROM 'Forums' WHERE 'ForumsURL' = (?)",
                   (URL, ))
    file = cursor.fetchall()
    if len(file) > 0:
        if file != "UNSET":
            os.remove(file[0])
    cursor.execute("DELETE FROM 'Forums' WHERE ForumURL = ?", (URL, ))
    connection.commit()
    if URL in ls:
        ls.remove(URL)
    return ls


def BreakConnection(cursor, connection):
    if connection:
        cursor.close()
        del cursor
