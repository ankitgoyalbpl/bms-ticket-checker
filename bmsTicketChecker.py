# -----------------------------------------------------------------------------------------------------------------------
#      Author: Ankit Goyal
#      Email : ankitgoyal.bpl@gmail.com
#------------------------------------------------------------------------------------------------------------------------

import urllib
import re
import json
from datetime import datetime

# Global Constants
WEBSITE_ERROR_MSG = "Some Error while contacting WebSite. Please Try again later"
INPUT_ERROR_MSG = "Wrong Input entered. Exiting"

BMS_GETCITIES_QUERY = "http://in.bookmyshow.com/getJSData/?cmd=GETREGIONS"
BMS_GETTHEATERS_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetVenues_MT_CITY.js&cmd=GETVENUESWEB&et=MT&rc=CITY"
BMS_GETMOVIES_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetEvents_MT.js&cmd=GETEVENTSWEB&et=MT&rc=CITY"

# This function uses a JQuery that the BMS site uses to select a City
# We read the results of that Query and ask user to select the City
# as per her preferences.
def SelectCity() :
      global WEBSITE_ERROR_MSG, INPUT_ERROR_MSG, BMS_GETCITIES_QUERY

      # Read the Geographic data from BMS Website
      try :
            pageContent = urllib.urlopen(BMS_GETCITIES_QUERY).read()
            
            # Clean the read content from unWanted Data
            pageContent = re.sub('var.+?=|;var.+', '', pageContent)
            regionData = json.loads(pageContent)
      except :
            print WEBSITE_ERROR_MSG
            exit()

      # Ask User to select the State
      counter = 1
      for stateName in regionData.keys() :
            print counter, stateName
            counter = counter + 1
      inputIndex = raw_input("Please Enter your State Name (Index): ")
      try :
            choosenIndex = int(inputIndex) - 1
            if choosenIndex < 0 or choosenIndex >= len(regionData.keys()) : 
                  raise Exception()
      except : 
            print INPUT_ERROR_MSG
            exit()

      # Ask User to choose a City from the selected State 
      cityList = regionData.values()[choosenIndex]
      counter = 1
      for cityName in cityList :
            print counter, cityName["name"]
            counter = counter + 1
      inputIndex = raw_input("Please Enter your City Name (Index): ")
      try :
            choosenIndex = int(inputIndex) - 1
            if choosenIndex < 0 or choosenIndex >= len(cityList) : 
                  raise Exception()
      except : 
            print INPUT_ERROR_MSG
            exit()

      return cityList[choosenIndex]

# This function uses a JQuery that the BMS site uses to select a Theater
# We read the results of that Query on the basis of City selected and 
# ask user to select the Theater as per her preferences.
def SelectTheater(cityCode) :
      global WEBSITE_ERROR_MSG, INPUT_ERROR_MSG, BMS_GETTHEATERS_QUERY

      # Read the Theater List from BMS Website
      try : 
            pageContent = urllib.urlopen(BMS_GETTHEATERS_QUERY.replace("CITY", cityCode)).read()

            # Clean the read content from unWanted Data
            pageContent = re.sub('aiVN=|;$', '', pageContent)
            theaterData = json.loads(pageContent)
      except : 
            print WEBSITE_ERROR_MSG
            exit()

      # Ask User to Select the Theater
      counter = 1
      for theaterName in theaterData :
            print counter, theaterName[2]
            counter = counter + 1
      inputIndex = raw_input("Please Enter your Theater Name (Index): ")
      try :
            choosenIndex = int(inputIndex) - 1
            if choosenIndex < 0 or choosenIndex >= len(theaterData) : 
                  raise Exception()
      except : 
            print INPUT_ERROR_MSG

      return theaterData[choosenIndex]

# This function uses a JQuery that the BMS site uses to select a Movie
# We read the results of that Query on the basis of City selected and 
# ask user to select the Movie as per her preferences.
def SelectMovie(cityCode) :      
      global WEBSITE_ERROR_MSG, INPUT_ERROR_MSG, BMS_GETMOVIES_QUERY

      # Read the Movie List from BMS Website
      try : 
            pageContent = urllib.urlopen(BMS_GETMOVIES_QUERY.replace("CITY", cityCode)).read()

            # Clean the read content from unWanted Data
            pageContent = re.sub('aiLN=.+?;|aiEV=|;aiSRE=.*', '', pageContent)
            movieData = json.loads(pageContent)
      except : 
            print WEBSITE_ERROR_MSG
            exit()

      # Ask User to Select the Movie
      counter = 1
      for movieInfo in movieData :
            print counter, movieInfo[4]
            counter = counter + 1
      inputIndex = raw_input("Please Enter your Movie Name (Index): ")
      try :
            choosenIndex = int(inputIndex) - 1
            if choosenIndex < 0 or choosenIndex >= len(movieData) : 
                  raise Exception()
      except : 
            print INPUT_ERROR_MSG

      return movieData[choosenIndex]

# This function is used to get the Date of the Movie from the user
# Currently this has been set to make sure that the date is exactly 
# within 2 days from today 
def GetDateOfMovie() :
      global INPUT_ERROR_MSG

      inputValue = raw_input("Please Enter the Date (within 2 days from now) in following format (YYYYMMDD) : ")
      try : 
            inputDate = datetime.strptime(inputValue, '%Y%m%d')
      except : 
            print INPUT_ERROR_MSG
            exit()

      todaysDate = datetime.now()
      if  (inputDate - todaysDate).days < 0 or (inputDate - todaysDate).days > 2: 
            print INPUT_ERROR_MSG
            exit()

      return inputValue


# Main Code
city = SelectCity()
print city["code"]
theaterData = SelectTheater(city["code"])
print theaterData
movieData = SelectMovie(city["code"])
print movieData
print GetDateOfMovie()