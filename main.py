#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from os import environ
import sys
import core
import crud
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QMessageBox

class DorkyPy(QMainWindow):
    """
    class that contains the full App
    """
    pathfolder = os.path.abspath(os.getcwd()) + "/"
    
    def __init__(self):
        """
        Initialize the main application
        """
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.searchGoogle.clicked.connect(self.fn_searchGoogle)
        self.searchApp.clicked.connect(self.fn_searchApp)
        self.folder_button.clicked.connect(self.fn_folder_select)
        self.google.toggled.connect(self.fn_radiobuttons)
        self.selectbutton.clicked.connect(self.checkifjson)
        self.jsonRefreash()

    def checkifjson(self):
        """
        function to check if json is selected
        """
        if (self.google.isChecked()):
            self.searchApp.setEnabled(True)
            self.searchGoogle.setEnabled(True)
        else:     
            if ('.json' not in str(self.files_combobox.currentText())):
                self.searchApp.setEnabled(False)
            else:
                self.searchApp.setEnabled(True)

    def jsonRefreash(self):
        """
        function to refreash de combo box of .json
        """
        files = crud.Collections(self.pathfolder)
        self.files_combobox.clear()
        for file in files.files:
            self.files_combobox.addItem(file)     

    def fn_folder_select(self):
        """
        function on folder selected, detect .json and add them to combobox
        """
        dialog = QFileDialog()
        self.pathfolder = dialog.getExistingDirectory(None, 'Select folder') + "/"
        files = crud.Collections(self.pathfolder)
        self.files_combobox.clear()
        for file in files.files:
            self.files_combobox.addItem(file)
        self.checkifjson()

    def fn_radiobuttons(self):
        """
        activate or deactivate buttons in each case
        """
        if(self.google.isChecked()):
            self.searchGoogle.setEnabled(True)
            self.searchApp.setEnabled(True)
        else:
            self.searchGoogle.setEnabled(False)
            self.checkifjson()

    def fn_writeResultDDBB(self, query):
        """
        function to write the results on .json
        """
        if(self.files_combobox.currentText() != ""):
            self.collection = crud.Collection(self.pathfolder, self.files_combobox.currentText())
            self.documents = []
            for result in query.searchedAppQuery:
                if (not result.startswith("http")):
                    self.resultTitle = result
                else:
                    self.documents.append(crud.Document(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text(), self.resultTitle, result))
            for document in self.documents:
                self.collection.addDocument(document.document)
        else:
            self.colName = 'collection.json'
            self.collection = crud.Collection(self.pathfolder, self.colName)
            self.collection.newJson()
            self.documents = []
            for result in query.searchedAppQuery:
                if (not result.startswith("http")):
                    self.resultTitle = result
                else:
                    self.documents.append(crud.Document(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text(), self.resultTitle, result))
            for document in self.documents:
                self.collection.addDocument(document.document)

    def fn_searchApp(self):
        """
        Function on search on App clicked, generate query, show results and save the results on .json
        """
        query = core.Query(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text())
        if(self.google.isChecked()):
            query.searchAppQuery()
            self.resultsShow.setAcceptRichText(True)
            self.resultsShow.setOpenExternalLinks(True)
            self.resultsShow.clear()

            if (len(query.searchedAppQuery) > 0):
                for result in query.searchedAppQuery: 
                    if (not result.startswith("http")):
                        self.resultTitle = result
                    else:
                        self.resultsShow.append("<a href=\"" + result + "\">" + self.resultTitle[:47] + "</a>")
                self.fn_writeResultDDBB(query)
                self.jsonRefreash()
            else:
                self.resultsShow.append("<a>No results found!!!</a>")
        else:
            self.collection = crud.Collection(self.pathfolder, self.files_combobox.currentText())
            self.collection.generateResults(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text())
            self.resultsShow.setAcceptRichText(True)
            self.resultsShow.setOpenExternalLinks(True)
            self.resultsShow.clear()
            if (len(self.collection.results) > 0):
                for result in self.collection.results:
                    if (not result.startswith("http")):
                        self.resultTitle = result
                    else:
                        self.resultsShow.append("<a href=\"" + result + "\">" + self.resultTitle[:47] + "</a>")            
            else:
                self.resultsShow.append("<a>No results found!!!</a>")
                
    def fn_searchGoogle(self):
        """
        Function on search on google clicked, open default browser with google url including dorks
        """
        gQuery = core.Query(self.topicSearch.text(), self.site.text(), self.fileExt.currentText(), self.customDorks.text())
        gQuery.searchGoogleQuery()
        QDesktopServices.openUrl(QUrl(gQuery.searchedGoogleQuery))

def suppress_qt_warnings():
    """
    Prevent warnings
    """
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication([])
    GUI = DorkyPy()
    GUI.show()
    sys.exit(app.exec_())