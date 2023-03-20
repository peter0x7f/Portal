class forum:
    def __init__ (self, URL, Icon, Password, Username):
        self.URL = URL
        self.icon = Icon
        self.Username = Username
        self.Password = Password
        
    def setSecurity(self, Username, Password):
        self.Username = Username
        self.Password = Password


def ReadInDB():
    forumList = []
    for row in cursor.execute("SELECT * FROM Forums"):
        forumList.append(forum(row[0], row[1], row[2], row[3]))
    return forumList


def AddForum(URL, iconFile, list):
    iconBin = convertImg(iconFile)
    cursor.execute("INSERT INTO Forums (ForumURL, Icon) VALUES (?, ?)", (URL, iconBin))
    connection.commit()
    list.append(forum(URL, iconBin))
    return list


def UpdateSecurity(URL, Username, Password, list):
    cursor.execute("UPDATE Forums SET Username = ?, Password = ? WHERE ForumURL = ?", (URL, Username, Password))
    connection.commit()
    for x in list:
        if x.URL == URL:
            setSecurity(Username, Password)
            break
    return list


def RemoveForum(URL, list):
    cursor.execute("DELETE FROM Forums WHERE ForumURL = ?", URL)
    connection.commit()
    for i in range(len(list)):
        if list[i].URL == URL:
            list.remove(i)
            break
    return list


def BreakConnection():
    for item in imageFiles:
        os.remove(item)
    if connection:
        cursor.close()
        del cursor


def ConvertToBin(filename):
    with open(filename, "rb") as file:
        img = file.read()
    return img


def ConvertToImg(Bin, filename): # we may need to include the filepath in filename
    with open(filename, 'wb') as file:
        file.write(Bin)
