import sqlite3
import os

#                       Database Structure                             #
# ForumURL - Text Not Null                                   Holds URL #
# Username - Text                                       Holds Username #
# Password - Text                                       Holds password #
# Icon - Text                             Holds file/filepath for file #


class forum:

    def __init__(self, URL, Icon, Password, Username):
        self.URL = URL
        self.icon = Icon
        self.Username = Username
        self.Password = Password

    def setSecurity(self, Username, Password):
        self.Username = Username
        self.Password = Password


def ReadInDB(cursor):
    forumList = []
    print("reading")

    cursor.execute("SELECT * FROM Forums")
    #for row in cursor.execute("SELECT * FROM Forums"):
    #    forumList.append(forum(row[0], row[1], row[2], row[3]))
    inList = cursor.fetchall()
    for row in inList:
        #print("hello ", row)
        forumList.append(forum(row[0], row[1], row[2], row[3]))
    return forumList


def AddForum(cursor, URL, list, connection):
    #iconBin = convertImg(iconFile)
    print("adding")
    cursor.execute("INSERT INTO Forums (ForumURL) VALUES (?)", (URL, ))
    connection.commit()
    list.append(forum(URL, "", "", ""))
    return list


def UpdateSecurity(cursor, URL, Username, Password, list, connection):
    print("updating")
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
    cursor.execute("DELETE FROM Forums WHERE ForumURL = ?", URL)
    connection.commit()
    for i in range(len(list)):
        if list[i].URL == URL:
            list.remove(i)
            break
    return list


def BreakConnection(cursor, connection):
    for item in imageFiles:
        os.remove(item)
    if connection:
        cursor.close()
        del cursor


def ConvertToBin(filename):
    with open(filename, "rb") as file:
        img = file.read()
    return img


def ConvertToImg(Bin, filename):
    with open(filename, 'wb') as file:
        file.write(Bin)

