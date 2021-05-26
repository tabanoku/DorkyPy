import os, glob, json
from datetime import datetime


class Collections:
    """
    class to detect all .json files inside the selected folder
    """
    def __init__(self, pathfolder):
        self.files = []
        os.chdir(pathfolder)
        for file in glob.glob('*.json'):
            self.files.append(str(file))
        self.files.append("")

class Collection:
    """
    class to generate and preform actions on selected .json file
    """
    def __init__(self, path, collectionname):
        self.path = path
        self.collectionname = collectionname
        self.fullpath = self.path + self.collectionname

    def newJson(self):
        """
        when no json selected, creates a new one
        """
        self.fullpath = self.path+self.collectionname
        
        try:
            open(self.fullpath, 'x')
            f = open(self.fullpath, 'w')
            f.write('[]')
            f.close()

        except:
            actualDate = datetime.now()
            actualDate = actualDate.strftime("%d_%m_%Y_%H_%M_%S")
            fullnewpath = self.path + actualDate + self.collectionname
            open(fullnewpath, 'x')
            f = open(fullnewpath, 'w')
            f.write('[]')
            f.close()

    def addDocument(self, document):
        """
        add the document to .json file
        """
        with open(self.path+self.collectionname) as reader:
            data = json.load(reader)
            data.append(document)
        with open(self.path+self.collectionname, 'w') as writer:
            json.dump(data, writer, indent=4)

    def generateResults(self, topic, site, ext, dorks):
        """
        preform a search on .json selected file
        """
        self.results = []
        with open(self.fullpath) as reader:
            data = json.load(reader)   
            for d in data:
                flag = True
                if(topic != ""):
                    if(topic != d['topic']):
                        flag = False
                if(site != ""):
                    if(site != d['site']):
                        flag = False
                if(ext != ""):
                    if(ext != d['fileext']):
                        flag = False
                if(dorks != ""):
                    if(dorks != d['dorks']):
                        flag = False
                if (flag):
                    self.results.append(d['url'])

class Document:
    """
    a class to create the json document (type dict in Python3)
    """
    def __init__(self, topic, site, ext, dorks, result):
        self.document = {
            "topic":topic,
            "site":site,
            "fileext":ext,
            "dorks":dorks,
            "url":result
        }