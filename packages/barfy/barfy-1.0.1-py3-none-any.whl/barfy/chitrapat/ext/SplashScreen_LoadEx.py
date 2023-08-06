import sys
import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLabel
from barfy.chitrapat.SplashScreen_Load import SplashScreen_Load
from barfy.chitrapat.TextBarfy import TextBarfy


class SplashScreen_LoadEx(SplashScreen_Load):

    def __init__(self,app=None,timeoutSeconds:int=10,

                 appIconPath:str=r"path/to/application/icon.png",
                 appIconSize:tuple=(120,120),

                 appTitle: str = "App Title",
                 appTitleFontWeight=600,
                 appTitleFontSize: int = 36,
                 appTitleFontColor="#00007f",
                 appTitleFontFamily="MS Shell Dlg 2",

                 appTagLine="App Tag Line",
                 appTagLineFontSize: int = 18,
                 appTagLineFontWeight:int=200,
                 appTagLineFontColor="#00007f",
                 appTagLineFontFamily="MS Shell Dlg 2",

                 companyIconPath:str=r"path/to/company/icon.png",
                 companyIconSize:tuple=(40,40),

                 companyName:str="Company Name",
                 companyNameFontSize:int=18,
                 companyNameFontColor:str="black",
                 companyNameFontFamily:str="MS Shell Dlg 2",
                 companyNameFontWeight:int=600,

                 companyIntro:str="Powered By:",
                 companyIntroFontSize:int=12,
                 companyIntroFontColor: str = "#000000",
                 companyIntroFontFamily: str = "MS Shell Dlg 2",
                 companyIntroFontWeight: int = 100,

                 copyrightLine:str="Copyright © 2001-2022, Company name pvt ltd., all rights reserved",
                 copyrightFontSize:int=8,
                 copyrightFontColor: str = "#000000",
                 copyrightFontFamily: str = "MS Shell Dlg 2",
                 copyrightFontWeight: int = 0,

                 loaderGifPath:str=r"path/to/loader/transparentloader.gif",
                 loaderGifSize:tuple=(100,100)

                 # progressBarColor="rgb(1,136,166)",
                 ):
        super(SplashScreen_LoadEx, self).__init__()

        textBarfyTitle=TextBarfy(title=appTitle,fontSize=appTitleFontSize,fontColor=appTitleFontColor,fontWeight=appTitleFontWeight,fontFamily=appTitleFontFamily)
        textBarfyTagLine = TextBarfy(title=appTagLine, fontSize=appTagLineFontSize, fontColor=appTagLineFontColor,fontWeight=appTagLineFontWeight, fontFamily=appTagLineFontFamily)
        textBarfyCompanyName=TextBarfy(title=companyName,fontSize=companyNameFontSize,fontWeight=companyNameFontWeight,fontColor=companyNameFontColor,fontFamily=companyNameFontFamily)
        textBarfyCompanyIntro=TextBarfy(title=companyIntro,fontSize=companyIntroFontSize,fontColor=companyIntroFontColor,fontWeight=companyIntroFontWeight,fontFamily=companyIntroFontFamily)
        textBarfyCopyRight=TextBarfy(title=copyrightLine,fontSize=copyrightFontSize,fontColor=copyrightFontColor,fontFamily=copyrightFontFamily,fontWeight=copyrightFontWeight)

        self._labelAppTitle.setText(textBarfyTitle.getHtmlStyleFormat())
        self._labelAppTagLine.setText(textBarfyTagLine.getHtmlStyleFormat())
        self._labelCompanyName.setText(textBarfyCompanyName.getHtmlStyleFormat())
        self._labelCompanyIntroHeading.setText(textBarfyCompanyIntro.getHtmlStyleFormat())
        self._labelCopyRight.setText(textBarfyCopyRight.getHtmlStyleFormat())

        self._labelAppIconPath.setPixmap(QtGui.QPixmap(appIconPath))
        self._labelAppIconPath.setMinimumSize(appIconSize[0],appIconSize[1])
        self._labelAppIconPath.setMaximumSize(appIconSize[0],appIconSize[1])
        self._labelAppIconPath.setScaledContents(True)

        self._labelCompanyIcon.setPixmap(QtGui.QPixmap(companyIconPath))
        self._labelCompanyIcon.setMinimumSize(companyIconSize[0],companyIconSize[1])
        self._labelCompanyIcon.setMaximumSize(companyIconSize[0],companyIconSize[1])
        self._labelCompanyIcon.setScaledContents(True)

        self._labelLoader.setMinimumSize(loaderGifSize[0],loaderGifSize[1])
        self._labelLoader.setMaximumSize(loaderGifSize[0], loaderGifSize[1])

        self._labelLoader.setScaledContents(True)
        self.movie = QMovie(loaderGifPath)
        self._labelLoader.setMovie(self.movie)
        self.movie.start()

        self._app=app
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        qr=self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        timeToWait=time.time()+timeoutSeconds
        self.show()
        while timeToWait >=time.time():
            # print("Waiting")
            if self._app is not None:
                self._app.processEvents()

        # Simulate something that takes time
        # time.sleep(1)

    def finish(self,mainWindow):
        super(SplashScreen_LoadEx, self).finish(mainWindow)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    splash=SplashScreen_LoadEx(app,1)
    splash.show()
    app.exec()




# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QSplashScreen
#
# class SplashScreen_Load(QSplashScreen):
#     def __init__(self):
#         super(SplashScreen_Load, self).__init__()
#         self.setupUi()
#
#     def setupUi(self):
#         Dialog=self