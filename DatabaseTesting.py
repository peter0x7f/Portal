import DatabaseInteraction
import sqlite3

def test():
    url = "reddit.com"
    print("testing")
    connection = sqlite3.connect("PortalDB.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Forums (ForumURL) VALUES (?)", (url, ))
    cursor.execute("SELECT * FROM Forums")
    res = cursor.fetchall()

    for x in res:
        print(x)

    forumList = DatabaseInteraction.ReadInDB(cursor)
    AddForum(cursor, url, forumList, connection)
    UpdateSecurity(cursor, url, "Hello", "World", forumList, connection)
    BreakConnection(cursor, connection)
    print("tested")
    print(forumList[4].URL)
