import os, glob, json
from datetime import datetime


class Collections:
    '''
    class to detect all .json files inside the selected folder
    '''

    def __init__(self, pathfolder):
        '''
        Initialize Colletions object

        :param str pathfolder: Absolute path selected to search, create new and store .json files
        '''

        self.files = []
        os.chdir(pathfolder)
        for file in glob.glob('*.json'):
            self.files.append(str(file))
        self.files.append("")

class Collection:
    '''
    class to generate and preform actions on selected .json file
    '''

    def __init__(self, path, collectionname):
        '''
        Initialize Collection object

        :param str path: Path of previous selected folder
        :param str collectionname: Name of .json file
        '''

        self.path = path
        self.collectionname = collectionname
        self.fullpath = self.path + self.collectionname

    def newJson(self):
        '''
        With fullpath try to create a new .json file, if it exists, creates a new one with day_month_year_hour_min_sec.json name
        '''

        self.fullpath = self.path+self.collectionname
        
        try:
            open(self.fullpath, 'x')
            f = open(self.fullpath, 'w')
            f.write('[]')
            f.close()

        except:
            actualDate = datetime.now()
            actualDate = actualDate.strftime("%d_%m_%Y_%H_%M_%S")
            self.fullpath = self.path + actualDate + self.collectionname
            open(self.fullpath, 'x')
            f = open(self.fullpath, 'w')
            f.write('[]')
            f.close()

    def addDocument(self, document):
        '''
        Open the .json file on path + collectionname and add the document

        :param dict document: dict generated from search parameters and result url
        '''

        with open(self.fullpath) as reader:
            data = json.load(reader)
            data.append(document)
        with open(self.fullpath, 'w') as writer:
            json.dump(data, writer, indent=4)

    def generateResults(self, topic, site, ext, dorks):
        '''
        preform a search on .json selected file

        :param str topic: Searched topic
        :param str site: Searched site or domain
        :param str ext: Searched file extension
        :param str dorks: Extra dorks used
        '''

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
                    self.results.append(d['title'])
                    self.results.append(d['url'])

class Document:
    '''
    a class to create the json document (type dict in Python3)
    '''

    def __init__(self, topic, site, ext, dorks, title, url):
        '''
        Initialize Document class to generate dict document variable with parameters and result URL

        :param str topic: Searched topic
        :param str site: Searched site or domain
        :param str ext: Searched file extension
        :param str dorks: Extra dorks used
        :param str title: Title of result
        :param str url: URL of result      
        '''

        self.document = {
            "topic":topic,
            "site":site,
            "fileext":ext,
            "dorks":dorks,
            "title":title,
            "url":url
        }