import os, glob, json
from datetime import datetime

class Collections:

    def __init__(self, pathfolder):
        self.files = []
        os.chdir(pathfolder)
        for file in glob.glob('*.json'):
            self.files.append(str(file))
        self.files.append("")

class Collection:
    
    def __init__(self, path, collectionname):
        self.path = path
        self.collectionname = collectionname
        self.fullpath = self.path + self.collectionname

    def newJson(self):
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
        with open(self.path+self.collectionname) as reader:
            data = json.load(reader)
            data.append(document)
        with open(self.path+self.collectionname, 'w') as writer:
            json.dump(data, writer, indent=4)

    def generateResults(self, topic, site, ext, dorks):
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
                    
    def __init__(self, topic, site, ext, dorks, result, fullpath):
        self.document = {
            "topic":topic,
            "site":site,
            "fileext":ext,
            "dorks":dorks,
            "url":result
        }