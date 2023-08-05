import sys
from PyQt5.QtWidgets import QApplication
from barfy.chitrapat.SplashConfig import SplashConfig
from barfy.chitrapat.ext.SplashScreen_DarkEx import SplashScreen_DarkEx
from barfy.chitrapat.ext.SplashScreen_TransparentEx import SplashScreen_TransparentEx

def splashScreenDarkDemoEx():
    app = QApplication(sys.argv)
    splashConfig=SplashConfig().setAppTitle("TechNicalSaaNd").setAppTagLine("Building Skills").setIcon(r"C:\Users\DELL\Downloads\flutter_projects\PDFSecure\pdf_secure\assets\images\_AboutAppImage.png")\
        .setProgressBarColor("yellow")\
        .setAppTitleFontColor("yellow")\
        .setAppTagLineFontColor("lime")\
        .setAppIconSize(300,100)\
        .setAppBackgroundColor("brown")
    dlg = SplashScreen_DarkEx(app,splashConfig=splashConfig)
    dlg.show()
    app.exec()

def splashScreenTransparentEx():
    app = QApplication(sys.argv)
    splashConfig = SplashConfig().setAppTitle("TechNicalSaaNd")\
        .setAppTagLine("Building Skills")\
        .setIcon(r"C:\Users\DELL\Downloads\flutter_projects\PDFSecure\pdf_secure\assets\images\_AboutAppImage.png")\
        .setProgressBarColor("brown")\
        .setAppTitleFontColor("brown")\
        .setAppTagLineFontColor("brown")\
        .setAppIconSize(400,200)
    dlg = SplashScreen_TransparentEx(app,splashConfig=splashConfig)
    dlg.show()
    app.exec()

# def splashScreenTransparent():
#     app = QApplication(sys.argv)
#     dlg = SplashScreen_Transparent()
#     dlg.show()
#     app.exec()

# def splashScreenDarkDemo():
#     app = QApplication(sys.argv)
#     dlg = SplashScreen_Dark()
#     dlg.show()
#     app.exec()


if __name__ == '__main__':
    splashScreenDarkDemoEx()
    # splashScreenTransparentEx()
