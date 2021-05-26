try:
    from googlesearch import search
except ImportError: 
    print('No module named \'googlesearch\' found')

INTITLEDORK = "intitle:"
SITEDORK = " site:"
FILEEXTDORK = " filetype:"

BASEBW = "https://www.google.com/search?q="
BWINTITLE = "intitle%3A"
BWSITE = "site%3A"
BWEXT = "ext%3A"
BWSPACE = "+"

class Query:
    """
    Generates Query object with parameters   
    """
    def __init__(self, intitle = "", site = "", fileExt = "", dorks = ""):
        self.intitle = ""
        self.site = ""
        self.fileExt = ""
        self.dorks = ""

        if (intitle != ""):
            self.intitle = "\"" + intitle + "\""
        if (site != ""):
            self.site = site
        if (fileExt != ""):
            self.fileExt = fileExt
        if (dorks != ""):
            self.dorks = dorks
    
    def searchGoogleQuery(self):
        """
        Generates a valid query to Google
        """
        self.searchedGoogleQuery = BASEBW
        if (self.intitle != ""):
            self.searchedGoogleQuery += BWINTITLE + self.intitle
        if (self.site != ""):
            self.searchedGoogleQuery += BWSPACE + BWSITE + self.site
        if (self.fileExt != ""):
            self.searchedGoogleQuery += BWSPACE + BWEXT + self.fileExt
        if (self.dorks != ""):
            bwdorkstemp = self.dorks.split(' ')
            bwdorks = ""
            for dork in bwdorkstemp:
                bwdorks += dork + BWSPACE
            bwdorks = bwdorks[:-1]
            self.searchedGoogleQuery += BWSPACE + bwdorks

    def searchAppQuery(self):
        """
        Generates a valid query to GoogleSearch library
        """
        self.searchedQuery = ""
        if(self.intitle != ""):
            self.searchedQuery += INTITLEDORK + self.intitle + " "
        if(self.site != ""):
            self.searchedQuery += SITEDORK + self.site + " "
        if(self.fileExt != ""):
            self.searchedQuery += FILEEXTDORK + self.fileExt + " "
        if(self.dorks != ""):
            self.searchedQuery += self.dorks
        self.searchedAppQuery = search(self.searchedQuery, num_results=24, lang="es")

        # googlesearch randomly gets search url as a result, this code fix that
        
        if (len(self.searchedAppQuery) > 0):
            if (self.searchedAppQuery[len(self.searchedAppQuery)-1].startswith("/search")):
                self.searchedAppQuery.pop(len(self.searchedAppQuery)-1)