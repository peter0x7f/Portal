import DatabaseInteraction
import sqlite3

url = "google.com"


def main():
  connection = sqlite3.connect("PortalDB.db")
  cursor = connection.cursor()
  
  forumList = ReadInDB(cursor):
  AddForum(cursor, url, forumList)
  UpdateSecurity(cursor, url, "Hello", "World", forumList)
  BreakConnection(cursor, connection)
  print(forumList[0])
