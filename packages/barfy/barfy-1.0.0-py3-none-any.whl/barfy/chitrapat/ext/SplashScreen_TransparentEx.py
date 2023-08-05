import sys
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from barfy.chitrapat.SplashConfig import SplashConfig
from barfy.chitrapat.SplashScreen_Transparent import SplashScreen_Transparent


class SplashScreen_TransparentEx(SplashScreen_Transparent):

    def __init__(self,app=None,timeoutSeconds:int=10,splashConfig:SplashConfig=None):
        super(SplashScreen_TransparentEx, self).__init__()
        if splashConfig is None:
            splashConfig=SplashConfig()
            splashConfig.setAppTitle("App Title").setAppTagLine("Application Tag Line").setCompanyName("Company Name")

        title=splashConfig.getAppTitle()
        titleDesc=splashConfig.getAppTagLine()
        appIconPath=splashConfig.getAppIcon()

        appIconSize=(150,150) if splashConfig.getAppIconSize() is None else splashConfig.getAppIconSize()
        appTitleFontSize=str(36) if splashConfig.getAppTitleFontSize() is None else str(splashConfig.getAppTitleFontSize())
        appTitleFontColor="#03468b" if splashConfig.getAppTitleFontColor() is None else splashConfig.getAppTitleFontColor()
        appTagLineFontSize=str(18) if splashConfig.getAppTagLineFontSize() is None else str(splashConfig.getAppTagLineFontSize())
        appTagLineFontColor="#0570da" if splashConfig.getAppTagLineFontColor() is None else splashConfig.getAppTagLineFontColor()
        progressBarColor="rgb(1,136,166)" if splashConfig.getProgressBarColor() is None else splashConfig.getProgressBarColor()


        self.label_2.setText("""<html><head/><body><p align="center"><span style=" font-size:{appTitleFontSize}pt; font-weight:600; color:{appTitleFontColor};">{title}</span></p></body></html>""".format(title=title,appTitleFontSize=appTitleFontSize,appTitleFontColor=appTitleFontColor))
        self.label_2.setStyleSheet("background-color: transparent;")
        self.label_3.setText("""<html><head/><body><p align="center"><span style=" font-size:{appTagLineFontSize}pt; text-decoration: underline; color:{appTagLineFontColor};">{titleDesc}</span></p></body></html>""".format(titleDesc=titleDesc,appTagLineFontSize=appTagLineFontSize,appTagLineFontColor=appTagLineFontColor))
        self.label_3.setStyleSheet("background-color: transparent;")

        self.label.setPixmap(QtGui.QPixmap(appIconPath))
        self.label.setScaledContents(True)
        self.label.setStyleSheet("background-color: transparent;")
        self.label.setMinimumSize(QtCore.QSize(appIconSize[0], appIconSize[1]))
        self.label.setMaximumSize(QtCore.QSize(appIconSize[0], appIconSize[1]))

        self._app=app
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        s = """
            QProgressBar {
                background-color: transparent;
                border-radius: 15px;
            }

            QProgressBar::chunk {
                background-color: """+progressBarColor+ """ ;                
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


        for i in range(1, 11):
            self.progressBar.setValue(i)
            t = time.time()
            while time.time() < t + 0.1:
                if self._app is not None:
                    self._app.processEvents()

        # Simulate something that takes time
        time.sleep(timeoutSeconds)

    def finish(self,mainWindow):
        super(SplashScreen_TransparentEx, self).finish(mainWindow)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    dlg=SplashScreen_TransparentEx(app,1)
    dlg.show()
    app.exec()



# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QSplashScreen
#
#
# class SplashScreen_Transparent(QSplashScreen):
#
#     def __init__(self):
#         super(SplashScreen_Transparent, self).__init__()
#         self.setupUi()
#
#     def setupUi(self):
#         Dialog = self