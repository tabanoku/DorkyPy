#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import core
import crud
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QApplication

class DorkyPy(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.searchGoogle.clicked.connect(self.fn_searchGoogle)
        self.searchApp.clicked.connect(self.fn_searchApp)
        self.google.toggled.connect(self.fn_radiobuttons)

    # activate or deactivate search on google if database is checked
    def fn_radiobuttons(self):
        if(self.google.isChecked()):
            self.searchGoogle.setEnabled(True)
        else:
            self.searchGoogle.setEnabled(False)
            
    # Function on search on App clicked
    def fn_searchApp(self):
        query = core.Query(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text())
        if(self.google.isChecked()):
            query.searchAppQuery()
            query.searchGoogleQuery()
            self.resultsShow.setAcceptRichText(True)
            self.resultsShow.setOpenExternalLinks(True)
            self.resultsShow.clear()
            if (len(query.searchedAppQuery) > 0):
                for result in query.searchedAppQuery:
                    self.resultsShow.append("<a href=\"" + result +"\">"+result[:40]+"...</a>")
            else:
                self.resultsShow.append("<a>No results found!!!</a>")
        else:
            print("google = " + str(self.google.isChecked()))
            print("DDBB = " + str(self.database.isChecked()))

    # Function on search on google clicked
    def fn_searchGoogle(self):
        gQuery = core.Query(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text())
        gQuery.searchGoogleQuery()
        QDesktopServices.openUrl(QUrl(gQuery.searchedGoogleQuery))

if __name__ == '__main__':
    app = QApplication([])
    GUI = DorkyPy()
    GUI.show()
    sys.exit(app.exec_())