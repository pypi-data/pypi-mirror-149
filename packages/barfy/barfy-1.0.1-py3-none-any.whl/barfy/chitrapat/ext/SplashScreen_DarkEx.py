import sys
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from barfy.chitrapat.SplashScreen_Dark import SplashScreen_Dark
from barfy.chitrapat.TextBarfy import TextBarfy


class SplashScreen_DarkEx(SplashScreen_Dark):
    
    def __init__(self,app=None,timeoutSeconds:int=10,

                 appIconPath:str="path/to/the/app/icon.png",
                 appIconSize:tuple=(180,70),

                 appTitle: str = "App Title",
                 appTitleFontWeight=600,
                 appTitleFontSize: int = 36,
                 appTitleFontColor="#ffffff",
                 appTitleFontFamily="MS Shell Dlg 2",

                 appTagLine="App Tag Line",
                 appTagLineFontSize: int = 18,
                 appTagLineFontWeight: int = 200,
                 appTagLineFontColor="#bfbfbf",
                 appTagLineFontFamily="MS Shell Dlg 2",

                 progressBarColor="rgb(1,136,166)",
                 appBackgroundColor="rgb(54, 43, 46)"
                 ):
        super(SplashScreen_DarkEx, self).__init__()

        # if splashConfig is None:
        #     splashConfig=SplashConfig()
        #     splashConfig.setAppTitle("App Title").setAppTagLine("Application Tag Line").setCompanyName("Company Name")

        appIconPath=appIconPath
        appTitleFontSize=str(appTitleFontSize)
        appTitleFontWeight = str(appTitleFontWeight)

        appTagLineFontSize=str(appTagLineFontSize)
        appTagLineFontWeight=str(appTagLineFontWeight)

        textBarfyTitle = TextBarfy(title=appTitle, fontSize=appTitleFontSize, fontColor=appTitleFontColor,fontWeight=appTitleFontWeight, fontFamily=appTitleFontFamily)
        textBarfyTagLine = TextBarfy(title=appTagLine, fontSize=appTagLineFontSize, fontColor=appTagLineFontColor,fontWeight=appTagLineFontWeight, fontFamily=appTagLineFontFamily)

        self.label_2.setText(textBarfyTitle.getHtmlStyleFormat())
        self.label_3.setText(textBarfyTagLine.getHtmlStyleFormat())

        appIconPixMap=QtGui.QPixmap(appIconPath)
        self.label.setPixmap(appIconPixMap)
        self.label.setMinimumSize(QtCore.QSize(appIconSize[0], appIconSize[1]))
        self.label.setMaximumSize(QtCore.QSize(appIconSize[0], appIconSize[1]))
        self.setStyleSheet("background-color: {appBackgroundColor};".format(appBackgroundColor=appBackgroundColor))
        self._app=app
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        s="""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
            }
            
            QProgressBar::chunk {
                background-color: """+progressBarColor+""";
                width: 20px;
            }
        """
        self.progressBar.setStyleSheet(s)
        self.progressBar.setMaximum(10)
        qr=self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()

        # self.showMessage("<h1><font color='green'>Welcome BeeMan!</font></h1>", Qt.AlignTop | Qt.AlignCenter,
        #                  Qt.black)
        for i in range(1, 11):
            self.progressBar.setValue(i)
            t = time.time()
            while time.time() < t + 0.1:
                if self._app is not None:
                    self._app.processEvents()

        # Simulate something that takes time
        time.sleep(timeoutSeconds)

    def finish(self,mainWindow):
        super(SplashScreen_DarkEx, self).finish(mainWindow)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    dlg=SplashScreen_DarkEx(app,5)
    dlg.show()
    app.exec()

# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QSplashScreen
# from src.styles import appResources
#
# class SplashScreen_Dark(QSplashScreen):
#
#     def __init__(self):
#         super(SplashScreen_Dark, self).__init__()
#         self.setupUi()
#
#     def setupUi(self):
#         Dialog = self
