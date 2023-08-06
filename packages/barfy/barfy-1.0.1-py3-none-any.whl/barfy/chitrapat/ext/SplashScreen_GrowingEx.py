import sys
import time
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from barfy.chitrapat.SplashScreen_Growing import SplashScreen_Growing
from barfy.chitrapat.TextBarfy import TextBarfy


class SplashScreen_GrowingEx(SplashScreen_Growing):

    def __init__(self,app=None,timeoutSeconds:int=4,

                appIconPath = r"path/to/app/icon.png",

                appTitle:str="App Title",
                appTitleFontSize:int=58,
                appTitleFontWeight=600,
                appTitleFontColor = "#2914c6",
                appTitleFontFamily="MS Shell Dlg 2",

                appTagLine = "App Tag Line",
                appTagLineFontSize:int = 16,
                appTagLineFontWeight: int = 200,
                appTagLineFontColor = "#2111ff",
                appTagLineFontFamily="MS Shell Dlg 2",
                initialWidth = 10,
                initialHeight = 10,
                finalWidth = 240
                ):
        super(SplashScreen_GrowingEx, self).__init__()

        appTitleFontSize=str(appTitleFontSize)
        appTitleFontWeight=str(appTitleFontWeight)

        appTagLineFontSize=str(appTagLineFontSize)
        appTagLineFontWeight=str(appTagLineFontWeight)


        self._labelAppIcon = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._labelAppIcon.sizePolicy().hasHeightForWidth())
        self._labelAppIcon.setSizePolicy(sizePolicy)
        self._labelAppIcon.setMinimumSize(QtCore.QSize(initialWidth, initialHeight))
        self._labelAppIcon.setAutoFillBackground(False)
        self._labelAppIcon.setText("")
        self._labelAppIcon.setScaledContents(True)
        self._labelAppIcon.setAlignment(QtCore.Qt.AlignCenter)
        self._labelAppIcon.setObjectName("_labelAppIcon")


        textBarfyTitle=TextBarfy(title=appTitle,fontSize=appTitleFontSize,fontColor=appTitleFontColor,fontWeight=appTitleFontWeight,fontFamily=appTitleFontFamily)
        textBarfyTagLine = TextBarfy(title=appTagLine, fontSize=appTagLineFontSize, fontColor=appTagLineFontColor,fontWeight=appTagLineFontWeight, fontFamily=appTagLineFontFamily)

        self._labelAppName.setText(textBarfyTitle.getHtmlStyleFormat())
        self._labelTagLine.setText(textBarfyTagLine.getHtmlStyleFormat())

        finalHeight=int(finalWidth/int((initialWidth/initialHeight)))
        initialPositionX=int((self.geometry().width()/2)-(initialWidth/2))
        initialPositionY=int((self.geometry().height()/2)-(initialHeight/2))-60
        diffWidth=(finalWidth-initialWidth)/2
        diffHeight = (finalHeight - initialHeight) / 2

        # self.setStyleSheet("""background-color: transparent;""")
        # self.setStyleSheet("background-image: url('{appBackgroundPath}');".format(appBackgroundPath=appBackgroundPath))
        # self.label_2.setStyleSheet("background-image: url('{appBackgroundPath}');".format(appBackgroundPath=appBackgroundPath))
        # self.label_2.setStyleSheet("background-color: rgba(255, 255, 255);")
        # self.setStyleSheet("background-color: rgb(54, 43, 46);")

        self.label_2.setAttribute(Qt.WA_TranslucentBackground)
        self._labelAppIcon.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._labelTagLine.setAttribute(Qt.WA_TranslucentBackground)

        self._app=app
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self._labelAppIcon.setMinimumSize(initialWidth,initialHeight)
        self._labelAppIcon.setPixmap(QtGui.QPixmap(appIconPath))
        self._labelAppIcon.setScaledContents(True)

        # self._labelAppIcon.setText("Yes")
        # self._labelAppIcon.setStyleSheet("background: red;")
        # geo=self._labelAppIcon.geometry()
        # print(geo)

        self.anim = QPropertyAnimation(self._labelAppIcon, b"geometry")
        # print(timeoutSeconds)
        animDuration=1000*timeoutSeconds
        # print(animDuration)
        self.anim.setDuration(animDuration)
        self.anim.setStartValue(QRect(initialPositionX,initialPositionY, initialWidth, initialHeight))
        self.anim.setEndValue(QRect(int(initialPositionX-diffWidth), int(initialPositionY-diffHeight), finalWidth, finalHeight))
        self.anim.start()

        qr=self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        timeToWait=time.time()+timeoutSeconds
        # print(time.time(),timeToWait,timeoutSeconds)
        self.show()

        while timeToWait >=time.time():
            # print("Waiting")
            if self._app is not None:
                self._app.processEvents()
        # print(timeToWait,time.time())
        # for i in range(1, 11):
        #     self.progressBar.setValue(i)
        #     t = time.time()
        #     while time.time() < t + 0.1:
        #         if self._app is not None:
        #             self._app.processEvents()

        # Simulate something that takes time
        # print(time.time_ns())
        # time.sleep(1)
        # print(time.time_ns())

    def finish(self,mainWindow):
        super(SplashScreen_GrowingEx, self).finish(mainWindow)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    dlg=SplashScreen_GrowingEx(app,2)
    dlg.show()
    app.exec()

# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QSplashScreen
# class SplashScreen_Growing(QSplashScreen):
#     def __init__(self):
#         super(SplashScreen_Growing, self).__init__()
#         self.setupUi()
#
#     def setupUi(self):
#         Dialog = self
