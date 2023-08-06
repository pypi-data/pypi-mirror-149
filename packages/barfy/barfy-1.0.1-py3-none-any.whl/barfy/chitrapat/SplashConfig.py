
class SplashConfig:

    def __init__(self):
        self._appTitle=""
        self._appIcon=""
        self._appTagLine=""
        self._companyName=""
        self._companyIcon=""

        self._appIconSize=None
        self._appTitleFontSize=None
        self._appTitleFontColor=None
        self._appTagLineFontSize=None
        self._appTagLineFontColor=None
        self._progressBarColor=None
        self._appBackgroundColor=None

    def getAppBackgroundColor(self)->str:
        color=self._appBackgroundColor
        return color

    def setAppBackgroundColor(self, color:str):
        self._appBackgroundColor=color
        return self

    def getProgressBarColor(self)->str:
        color= self._progressBarColor
        return color

    def setProgressBarColor(self,progressBarColor:str):
        self._progressBarColor=progressBarColor
        return self

    def getAppTagLineFontColor(self):
        color=self._appTagLineFontColor
        return color

    def setAppTagLineFontColor(self,fontColor:str):
        self._appTagLineFontColor=fontColor
        return self

    def getAppTagLineFontSize(self)->int:
        fontSize=self._appTagLineFontSize
        return fontSize

    def setAppTagLineFontSize(self,fontSize:int):
        self._appTagLineFontSize=fontSize
        return self

    def getAppTitleFontColor(self)->str:
        color=self._appTitleFontColor
        return color

    def setAppTitleFontColor(self,fontColor:str):
        self._appTitleFontColor=fontColor
        return self

    def getAppTitleFontSize(self)->int:
        size=self._appTitleFontSize
        return size

    def setAppTitleFontSize(self,fontSize:int):
        self._appTitleFontSize=fontSize
        return self

    def setAppIconSize(self,width:int,height:int):
        self._appIconSize=(width,height)
        return self

    def getAppIconSize(self)->tuple:
        iconSize=self._appIconSize
        return iconSize


    def setAppTitle(self,appTitle:str="App Title"):
        self._appTitle=appTitle
        return self

    def setIcon(self,iconPath):
        self._appIcon=iconPath
        return self

    def setAppTagLine(self,tagLine):
        self._appTagLine=tagLine
        return self

    def setCompanyName(self,companyName:str="Company Name"):
        self._companyName=companyName
        return self

    def setCompanyIcon(self,companyIcon:str):
        self._companyIcon=companyIcon
        return self

    def getAppTitle(self)->str:
        appTitle=self._appTitle
        return appTitle

    def getAppTagLine(self)->str:
        tagLine=self._appTagLine
        return tagLine

    def getAppIcon(self)->str:
        iconPath=self._appIcon
        return iconPath

    def getCompanyName(self)->str:
        name=self._companyName
        return name

    def getCompanyIcon(self)->str:
        iconPath=self._companyIcon
        return iconPath