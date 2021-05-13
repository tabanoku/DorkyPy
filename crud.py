import os, glob, json

class Collections:

    def __init__(self, pathfolder):
        self.files = []
        os.chdir(pathfolder)
        for file in glob.glob('*.json'):
            self.files.append(str(file))
        self.files.append("")
    

class Collection:
    
    def __init__(self, collectionname):
        self.collectionname = collectionname

    def newJson(self):
        f = open(self.collectionname, 'x')
        f = open(self.collectionname, 'w')
        f.write('[]')
        f.close()

        

        

class Document:
                    
    def __init__(self, topic, site, ext, dorks, result, collectionname):
        self.document = {
            "topic":topic,
            "site":site,
            "fileext":ext,
            "dorks":dorks,
            "url":result
        }

class Results:
    pass