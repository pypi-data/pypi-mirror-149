import sys
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from barfy.chitrapat.SplashConfig import SplashConfig
from barfy.chitrapat.SplashScreen_Dark import SplashScreen_Dark

class SplashScreen_DarkEx(SplashScreen_Dark):
    
    def __init__(self,app=None,timeoutSeconds:int=10,splashConfig:SplashConfig=None):
        super(SplashScreen_DarkEx, self).__init__()

        if splashConfig is None:
            splashConfig=SplashConfig()
            splashConfig.setAppTitle("App Title").setAppTagLine("Application Tag Line").setCompanyName("Company Name")

        title=splashConfig.getAppTitle()
        titleDesc=splashConfig.getAppTagLine()
        appIconPath=splashConfig.getAppIcon()

        appIconSize=(180,70) if splashConfig.getAppIconSize() is None else splashConfig.getAppIconSize()
        appTitleFontSize=str(36) if splashConfig.getAppTitleFontSize() is None else str(splashConfig.getAppTitleFontSize())
        appTitleFontColor="#ffffff" if splashConfig.getAppTitleFontColor() is None else splashConfig.getAppTitleFontColor()
        appTagLineFontSize=str(18) if splashConfig.getAppTagLineFontSize() is None else str(splashConfig.getAppTagLineFontSize())
        appTagLineFontColor="#bfbfbf" if splashConfig.getAppTagLineFontColor() is None else splashConfig.getAppTagLineFontColor()
        progressBarColor = "rgb(1,136,166)" if splashConfig.getProgressBarColor() is None else splashConfig.getProgressBarColor()
        appBackgroundColor="rgb(54, 43, 46)" if splashConfig.getAppBackgroundColor() is None else splashConfig.getAppBackgroundColor()

        self.label_2.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:{appTitleFontSize}pt; font-weight:600; color:{appTitleFontColor};\">{appName}</span></p></body></html>".format(appName=title,appTitleFontSize=appTitleFontSize,appTitleFontColor=appTitleFontColor))
        self.label_3.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:{appTagLineFontSize}pt; text-decoration: underline; color:{appTagLineFontColor};\">{appTagLine}</span></p></body></html>".format(appTagLine=titleDesc,appTagLineFontSize=appTagLineFontSize,appTagLineFontColor=appTagLineFontColor))
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
