try:
    from requests import get
    from bs4 import BeautifulSoup
except ImportError: 
    print('Try installing requests and bs4 libraries')

INTITLEDORK = "intitle:"
SITEDORK = " site:"
FILEEXTDORK = " filetype:"

BASEBW = "https://www.google.com/search?q="
BWINTITLE = "intitle%3A"
BWSITE = "site%3A"
BWEXT = "ext%3A"
BWSPACE = "+"

class Query:
    '''
    Generates Query object with parameters   
    '''

    def __init__(self, intitle = "", site = "", fileExt = "", dorks = ""):
        '''
        Initialize Query object

        :param str intitle: Topic searched
        :param str site: Site or domain searched
        :param str fileExt: File extension searched
        :param str dorks: Other dorks added to search
        '''


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
    
    def __scrapper(self, term, num_results = 24, lang='es'):

        usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

        def fetch_results(search_term, number_results, language_code):
            escaped_search_term = search_term.replace(' ', '+')

            google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results+1,
                                                                                language_code)
            response = get(google_url, headers=usr_agent)
            response.raise_for_status()

            return response.text

        def parse_results(raw_html):
            soup = BeautifulSoup(raw_html, 'html.parser')
            result_block = soup.find_all('div', attrs={'class': 'g'})

            for result in result_block:
                link = result.find('a', href=True)
                title = result.find('h3')
                if link and title:
                    yield link['href']
                    yield title.string

        html = fetch_results(term, num_results, lang)

        return list(parse_results(html))
    
    def searchGoogleQuery(self):
        """
        Generates a valid query to use on default browser
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
        Generates a valid query to use GoogleSearch library
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
        self.searchedAppQuery = self.__scrapper(self.searchedQuery, num_results=24, lang="es")

        # googlesearch randomly gets search url as a result, this code fix that
        
        if (len(self.searchedAppQuery) > 0):
            if (self.searchedAppQuery[len(self.searchedAppQuery)-2].startswith("/search")):
                self.searchedAppQuery.pop(len(self.searchedAppQuery)-1)
                self.searchedAppQuery.pop(len(self.searchedAppQuery)-1)


