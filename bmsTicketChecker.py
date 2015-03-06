# -----------------------------------------------------------------------------------------------------------------------
#      Author: Ankit Goyal
#      Email : ankitgoyal.bpl@gmail.com
#------------------------------------------------------------------------------------------------------------------------

import urllib
import re
import json
import notify2
import time
import string
import smtplib
from datetime import datetime, timedelta
from collections import defaultdict

# Global Constants
WEBSITE_ERROR_MSG = "Some Error while contacting WebSite. Please Try again later"
INPUT_ERROR_MSG = "Wrong Input entered. Exiting"
SLEEP_TIME = int(300)                     # 5 Minutes

BMS_GETCITIES_QUERY = "http://in.bookmyshow.com/getJSData/?cmd=GETREGIONS"
BMS_GETTHEATERS_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetVenues_MT_CITY.js&cmd=GETVENUESWEB&et=MT&rc=CITY"
BMS_GETMOVIES_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetEvents_MT.js&cmd=GETEVENTSWEB&et=MT&rc=CITY"
BMS_GETSHOWTIMESINFO_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetShowTimesByEvent_CITY_MOVIECODE_DATE.js&cmd=GETSHOWTIMESBYEVENTWEB&ec=MOVIECODE&dc=DATE&rc=CITY"

srcEmailID = "ankitgoyal.bpl@gmail.com"

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
            exit()

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
            exit()

      return movieData[choosenIndex]


# This function is used to get the Date of the Movie from the user
# Currently this has been set to make sure that the date is exactly 
# within 2 days from today 
def GetDateOfMovie() :
      global INPUT_ERROR_MSG

      todaysDate = datetime.now()
      counter = 0
      while True :
            print (counter + 1), (todaysDate + timedelta(days = counter)).date().strftime("%A - %d %B, %Y")
            counter = counter + 1
            if counter > 4 : 
                  break
      inputIndex = raw_input("Please Enter your Date (Index): ")
      try :
            choosenIndex = int(inputIndex) - 1
            if choosenIndex < 0 or choosenIndex > 4 : 
                  raise Exception()
      except : 
            print INPUT_ERROR_MSG
            exit()

      return (todaysDate + timedelta(days = choosenIndex)).date()


# This function gets the list of ShowTimes for the given city, Movie and Theater selected
# It also gets the number of available seats for each showtime
def GetShowTimes(cityCode, date, movieCode, theaterCode) : 
      global WEBSITE_ERROR_MSG, INPUT_ERROR_MSG, BMS_GETSHOWTIMESINFO_QUERY

      showTimes = list()
      # Read the Movie List from BMS Website
      try : 
            BMS_GETSHOWTIMESINFO_QUERY = BMS_GETSHOWTIMESINFO_QUERY.replace("CITY", cityCode)
            BMS_GETSHOWTIMESINFO_QUERY = BMS_GETSHOWTIMESINFO_QUERY.replace("MOVIECODE", movieCode)
            BMS_GETSHOWTIMESINFO_QUERY = BMS_GETSHOWTIMESINFO_QUERY.replace("DATE", date)
            pageContent = urllib.urlopen(BMS_GETSHOWTIMESINFO_QUERY).read()

            # Clean the read content from unWanted Data
            availPageContent = re.sub('aEV=.+?;|aVN=.+aAV=|;$', '', pageContent)
            timePageContent = re.sub('aEV=.+?;|aVN=.+aST=|;aAV=.+;$', '', pageContent)
            availabilityData = json.loads(availPageContent)
            movieTimeData = json.loads(timePageContent) 
      except : 
            print WEBSITE_ERROR_MSG
            exit()

      for showTimeAvailInfo in availabilityData : 
            if showTimeAvailInfo[0] == theaterCode :
                  showTimes.append([showTimeAvailInfo[1], showTimeAvailInfo[0], showTimeAvailInfo[3], showTimeAvailInfo[4], showTimeAvailInfo[5], showTimeAvailInfo[6]])

      for movieTimeInfo in movieTimeData :
            for showTimesInfo in showTimes :
                  if movieTimeInfo[0] == theaterCode and showTimesInfo[0] == movieTimeInfo[2] :
                        showTimesInfo.append(movieTimeInfo[3])                  

      return showTimes


# Main Code
destEmailId = raw_input("Enter your Email Id: ")
city = SelectCity()
theaterData = SelectTheater(city["code"])
movieData = SelectMovie(city["code"])
movieDate = GetDateOfMovie()
counter = 1
while True:
      showTimes = GetShowTimes(city["code"], movieDate.strftime("%Y%m%d"), movieData[5], theaterData[0])
      notify2.init("BookMyShow Checker")

      # Found Match. Showing Results for each match
      if len(showTimes) > 0 :
            for showTimesInfo in showTimes : 
                  bookingSummary = "Bookings Open...!!!"
                  bookingMessage = "Movie: %s \nDate: %s \nTheater: %s \nShowTime: %s \nClass: %s \nAvailable-Seats: %s/%s" %(movieData[4], movieDate.strftime("%A - %d %B, %Y"), theaterData[2], showTimesInfo[6], showTimesInfo[2].capitalize(), showTimesInfo[4], showTimesInfo[5])
                  notify2.Notification(bookingSummary, bookingMessage, "notification-message-IM").show()
            break
      
      # More than 5 hours elapsed. Program will Quit
      elif counter == 60 :
            bookingSummary = "Tired...!!! Exiting..."
            bookingMessage = "Movie: %s \nDate: %s \nTheater: %s \nCan't find the Movie for selected details. Exiting...!!!" %(movieData[4], movieDate.strftime("%A - %d %B, %Y"), theaterData[2])
            notify2.Notification(bookingSummary, bookingMessage, "notification-message-IM").show()
            break

      # Search still in Progress
      elif counter % 5 == 0 :
            bookingSummary = "Still Searching...!!!"
            bookingMessage = "Movie: %s \nDate: %s \nTheater: %s \nCity: %s" %(movieData[4], movieDate.strftime("%A - %d %B, %Y"), theaterData[2], city["name"])
            notify2.Notification(bookingSummary, bookingMessage, "notification-message-IM").show()

      counter = counter + 1
      time.sleep(SLEEP_TIME)
 