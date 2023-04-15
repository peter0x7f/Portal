# TG start


#class to hold forums including name, icon filepath, and url
class forum:

    def __init__(self, URL, Icon, Name):
        self.SetUrl(URL)
        self.SetIcon(Icon)
        self.SetName(Name)

    def SetUrl(self, url):
        self.URL = url

    def GetUrl(self):
        return self.URL

    def SetIcon(self, icon):
        self.icon = icon

    def GetIcon(self):
        return self.icon

    def SetName(self, name):
        self.name = name

    def GetName(self):
        return self.name


# TG end
