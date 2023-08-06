
class TextBarfy:

    def __init__(self,
                 title:str="Label Barfy",
                 fontSize:int=20,
                 fontWeight:int=300,
                 fontFamily:str="MS Shell Dlg 2",
                 fontColor:str="black"
                 ):
        self._title =title
        self._fontSize=fontSize
        self._fontFamily=fontFamily
        self._fontColor=fontColor
        self._fontWeight=fontWeight

    def getFontWeight(self)->int:
        fontWeight=self._fontWeight
        return fontWeight

    def setFontWeight(self,fontWeight:int):
        self._fontWeight=fontWeight
        return self

    def getFontColor(self)->str:
        fontColor=self._fontColor
        return fontColor

    def setFontColor(self,fontColor:str):
        self._fontColor=fontColor
        return self

    def getFontFamily(self)->str:
        fontFamily=self._fontFamily
        return fontFamily


    def setFontFamily(self,fontFamily:str):
        self._fontFamily=fontFamily
        return self

    def setFontSize(self,fontSize:int):
        self._fontSize=fontSize
        return self

    def getFontSize(self)->str:
        fontSize=self._fontSize
        return fontSize

    def getTitle(self)->str:
        return self._title

    def setTitle(self, title:str):
        self._title=title
        return self

    def getHtmlStyleFormat(self)->str:
        fontSize=str(self.getFontSize())
        fontWeight=str(self.getFontWeight())
        fontColor=str(self.getFontColor())
        fontFamily=self.getFontFamily()
        title=self.getTitle()
        htmlFormat="""
            <html>
                <head/>
                <body>
                    <p>
                    <span style="
                        font-size:{fontSize}pt; 
                        font-weight:{fontWeight}; 
                        color:{fontColor};
                        font-family:{fontFamily};
                        ">
                        {title}
                    </span>
                    </p>
                </body>
            </html>""".format(fontSize=fontSize,fontWeight=fontWeight,fontColor=fontColor,title=title,fontFamily=fontFamily)

        return htmlFormat

if __name__ == '__main__':
    l=LabelBarfy()
    l.getTitle="Yes"
    print(l.getTitle)






