# -----------------------------------------------------------------------------------------------------------------------
#      Author: Ankit Goyal
#      Email : ankitgoyal.bpl@gmail.com
#------------------------------------------------------------------------------------------------------------------------

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from collections import defaultdict

# Global Constants
ERROR_MSG = "Some Error while contacting WebSite. Please Try again later"
BMS_WEBSITE_ADDRESS = "http://in.bookmyshow.com"
BMS_CITY_NAME = "hyderabad"
BMS_MOVIES_WEBPAGE = "movies"

# Function to get list of movies in a City
# both Now Showing and Next Change
def GetMoviesList() :
      try :
            pageContent = urllib.urlopen('/'.join([BMS_WEBSITE_ADDRESS, BMS_CITY_NAME, BMS_MOVIES_WEBPAGE])).read()
            onlyMovieTags = SoupStrainer("a", "mvCnt")
            movieSoup = BeautifulSoup(pageContent, parseOnlyThese=onlyMovieTags)
      except : 
            print ERROR_MSG
            exit()

      if len(movieSoup) < 1 :
            return None

      movieDict = defaultdict(list)
      for movieData in movieSoup :
            movieDict[movieData["data"]].append(movieData["href"])
            movieDict[movieData["data"]].append(movieData["title"])

      return movieDict


movieDict = GetMoviesList()
print len(movieDict)
