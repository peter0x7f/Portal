# TG start


#class to hold forums including name, icon filepath, and url
class forum:

    def __init__(self, URL, Icon, Name):
        self.URL = URL
        self.icon = Icon
        self.name = Name

    def SetUrl(url):
        self.URL = url

    def GetUrl():
        return self.URL

    def SetIcon(icon):
        self.icon = icon

    def GetIcon():
        return self.icon

    def SetName(name):
        self.name = name

    def GetName():
        return self.name


# TG end