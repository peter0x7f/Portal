import sqlite3
import os
import GetIcon
import ForumClass

#                       Database Structure                             #
#                             Forums                                   #
# ForumURL - Text Not Null                                   Holds URL #
# Icon - Text                             Holds file/filepath for file #
# Name - Text                              Holds the name of the forum #

#                            AllForums                                 #
# URL - Text Not Null                                        Holds URL #


# TG start


# returns a list of all forum objects containing all the forums in the database
def ReadInDB(cursor):
    forumList = []

    cursor.execute("SELECT * FROM Forums")
    inList = cursor.fetchall()
    for row in inList:
        forumList.append(ForumClass.forum(row[0], row[1], row[2]))
    return forumList


# adds a forum to the database after checking if it already exists
def AddForum(cursor, URL, path, name, connection):
    cursor.execute(
        "INSERT INTO Forums (ForumURL, Icon, Name) VALUES (?, ?, ?)",
        (URL, path, name))
    connection.commit()
    return 0


# removes a forum from the database and checks if an icon was downloaded. if so delete .ico file
def RemoveForum(cursor, URL, connection):
    cursor.execute("SELECT Icon FROM 'Forums' WHERE ForumURL = (?)", (URL, ))
    file = cursor.fetchall()
    if len(file) > 0:
        file = file[0]
        if file[0] != "Icons/Default.png":
            os.remove(file[0])
    cursor.execute("DELETE FROM 'Forums' WHERE ForumURL = ?", (URL, ))
    connection.commit()


# breaks the connection with the database
def BreakConnection(cursor, connection):
    if connection:
        cursor.close()
        del cursor


# TG end
