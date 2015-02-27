# -----------------------------------------------------------------------------------------------------------------------
#      Author: Ankit Goyal
#      Email : ankitgoyal.bpl@gmail.com
#------------------------------------------------------------------------------------------------------------------------

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from collections import defaultdict

# Global Constants
WEBSITE_ERROR_MSG = "Some Error while contacting WebSite. Please Try again later"
INPUT_ERROR_MSG = "Wrong Input entered. Exiting"
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

      # TODO: Make sure that we need a dictionary over here and not list. If not convert this to a list of tuples
      movieDict = defaultdict(list)
      for movieData in movieSoup :
            movieDict[movieData["data"]].append(movieData["href"])
            movieDict[movieData["data"]].append(movieData["title"])

      return movieDict

# Function to ask for User Input to select a movie out of list
# of movies in his/her city
def SelectMovie(movieDict) :      
      movieCouner = 1
      for movieItem in movieDict.values() :
            print movieCouner, movieItem[1]
            movieCouner = movieCouner + 1

      inputIndex = raw_input("Please Enter your Movie Choice: ")
      try :
            choosenIndex = int(inputIndex) - 1
      except : 
            print INPUT_ERROR_MSG

      return movieDict.values()[choosenIndex]


movieDict = GetMoviesList()
(movieLink, movieTitle) = SelectMovie(movieDict)

print "Choosen Movie", movieLink, movieTitle