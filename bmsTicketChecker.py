
import urllib
import re
import json
import notify2
import time
import string
from datetime import datetime, timedelta


# ----------------------------------------------------------------------------------------------- #
# Class for storing backend Data and running Queries to get content from BMS WebSite
class BMSTicketsData() :
      
      # JS Queries for BMS WebSite
      def InitializeBMSQueries(self) :
            self.BMS_GETREGIONS_QUERY = "http://in.bookmyshow.com/getJSData/?cmd=GETREGIONS"
            self.BMS_GETVENUES_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetVenues_MT_CITY.js&cmd=GETVENUESWEB&et=MT&rc=CITY"
            self.BMS_GETMOVIES_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetEvents_MT.js&cmd=GETEVENTSWEB&et=MT&rc=CITY"
            self.BMS_GETSHOWTIMESDATA_QUERY = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetShowTimesByEvent_CITY_MOVIECODE_DATE.js&cmd=GETSHOWTIMESBYEVENTWEB&ec=MOVIECODE&dc=DATE&rc=CITY"


      # Json variables which will store data as parsed from JS Queries run on WebSite
      def InitializeJsonData(self) :
            self.regionJsonData = None
            self.theatersJsonData = None
            self.moviesJsonData = None
            self.movieShowtimeJsonData = None
            self.movieAvailabilityJsonData = None


      def InitializeMovieVariables(self) :
            self.stateName = None
            self.cityName = None
            self.cityCode = None
            self.theaterName = None
            self.theaterCode = None
            self.movieName = None
            self.movieCode = None
            self.movieDate = None


      # Constructor
      def __init__(self, *args, **kw) :
            # Initialize Class Data
            self.InitializeBMSQueries()
            self.InitializeJsonData()
            self.InitializeMovieVariables()


      def InitRegionData(self) :
            try :
                  pageContent = urllib.urlopen(self.BMS_GETREGIONS_QUERY).read()
                  # Clean the read content from unWanted Data
                  pageContent = re.sub('var.+?=|;var.+', '', pageContent)
                  self.regionJsonData = json.loads(pageContent)
            except :
                  self.regionJsonData = None
                  return False

            return True


      def GetStatesList(self) :
            if self.regionJsonData is None :
                  return None

            stateList = list()
            for stateName in self.regionJsonData.keys() : 
                  stateList.append(str(stateName))

            return stateList


      def SetStateName(self, stateName) : 
            self.stateName = stateName


      def GetStateName(self) :
            return self.stateName


      def GetCitiesList(self) :
            if self.stateName is None or self.regionJsonData is None:
                  return None

            cityList = list()
            for cityData in self.regionJsonData[self.stateName] :
                  cityList.append(str(cityData["name"]))

            return cityList


      def SetCityData(self, cityName) :
            for cityData in self.regionJsonData[self.stateName] :
                  if cityData["name"] == cityName :
                        self.cityName = cityName
                        self.cityCode = cityData["code"]
                        break


      def GetCityData(self) :
            return self.cityName


      def InitTheaterData(self) :
            if self.cityCode is None :
                  self.theatersJsonData = None
                  return False

            try : 
                  pageContent = urllib.urlopen(self.BMS_GETVENUES_QUERY.replace("CITY", self.cityCode)).read()
                  # Clean the read content from unWanted Data
                  pageContent = re.sub('aiVN=|;$', '', pageContent)
                  self.theatersJsonData = json.loads(pageContent)
            except : 
                  self.theatersJsonData = None
                  return False

            return True


      def GetTheaterList(self) :
            if self.theatersJsonData is None :
                  return None

            theaterList = list()
            for theaterData in self.theatersJsonData : 
                  theaterList.append(str(theaterData[2]))

            return theaterList


      def SetTheaterData(self, theaterName) :
            for theaterData in self.theatersJsonData : 
                  if theaterData[2] == theaterName :
                        self.theaterName = theaterName
                        self.theaterCode = theaterData[0]
                        break


      def GetTheaterData(self) :
            return self.theaterName


      def InitMoviesData(self) :
            if self.cityCode is None :
                  self.moviesJsonData = None
                  return False

            try : 
                  pageContent = urllib.urlopen(self.BMS_GETMOVIES_QUERY.replace("CITY", self.cityCode)).read()
                  # Clean the read content from unWanted Data
                  pageContent = re.sub('aiLN=.+?;|aiEV=|;aiSRE=.*', '', pageContent)
                  self.moviesJsonData = json.loads(pageContent)
            except : 
                  self.moviesJsonData = None
                  return False

            return True


      def GetMoviesList(self) :
            if self.moviesJsonData is None :
                  return None

            moviesList = list()
            for moviesData in self.moviesJsonData : 
                  moviesList.append(str(moviesData[4]))

            return moviesList


      def SetMoviesData(self, movieName) :
            for moviesData in self.moviesJsonData : 
                  if moviesData[4] == movieName :
                        self.movieName = movieName
                        self.movieCode = moviesData[1]
                        break


      def GetMoviesData(self) :
            return self.movieName


      def SetMovieDate(self, movieDate) :
            try :
                  self.movieDate = movieDate.strftime("%Y%m%d")
            except :
                  self.movieDate = None
                  return False

            return True


      def GetMovieDate(self) :
            # TODO: return DateTime oject
            return self.movieDate


      def InitMoviesShowtimesData(self) :
            if self.cityCode is None or self.movieCode is None or self.movieDate is None:
                  self.movieShowtimeJsonData = None
                  self.movieAvailabilityJsonData = None
                  return False

            try : 
                  self.BMS_GETSHOWTIMESDATA_QUERY = self.BMS_GETSHOWTIMESDATA_QUERY.replace("CITY", self.cityCode)
                  self.BMS_GETSHOWTIMESDATA_QUERY = self.BMS_GETSHOWTIMESDATA_QUERY.replace("MOVIECODE", self.movieCode)
                  self.BMS_GETSHOWTIMESDATA_QUERY = self.BMS_GETSHOWTIMESDATA_QUERY.replace("DATE", self.movieDate)
                  pageContent = urllib.urlopen(self.BMS_GETSHOWTIMESDATA_QUERY).read()                  
                  # Clean the read content from unWanted Data
                  pageContent_ShowtimesData = re.sub('aEV=.+?;|aVN=.+aST=|;aAV=.+;$', '', pageContent)
                  pageContent_AvailabilityData = re.sub('aEV=.+?;|aVN=.+aAV=|;$', '', pageContent)
                  self.movieShowtimeJsonData = json.loads(pageContent_ShowtimesData)
                  self.movieAvailabilityJsonData = json.loads(pageContent_AvailabilityData)
            except : 
                  self.movieShowtimeJsonData = None
                  self.movieAvailabilityJsonData = None
                  return False

            return True


      def GetShowtimes(self) : 
            if self.movieAvailabilityJsonData is None or self.movieShowtimeJsonData is None :
                  if self.GetMoviesShowtimesData() is False : 
                        return None

            showTimes = list()
            for showTimeAvailInfo in self.movieAvailabilityJsonData :
                  if showTimeAvailInfo[0] == self.theaterCode :
                        showTimes.append([showTimeAvailInfo[1], showTimeAvailInfo[0], showTimeAvailInfo[3], showTimeAvailInfo[4], showTimeAvailInfo[5], showTimeAvailInfo[6]])

            for movieTimeInfo in self.movieShowtimeJsonData :
                  for showTimesInfo in showTimes :
                        if movieTimeInfo[0] == self.theaterCode and showTimesInfo[0] == movieTimeInfo[2] :
                              showTimesInfo.append(movieTimeInfo[3])                 

            # Setting the Data to None to avoid using stale Values
            self.movieAvailabilityJsonData = None
            self.movieShowtimeJsonData = None
            return showTimes

# End of Class BMSTicketsData
# ----------------------------------------------------------------------------------------------- #


def main() :     
      bms = BMSTicketsData()
      if bms.GetRegionData() is True :
            print "Got Region Data"
            # time.sleep(2)
            # print bms.GetStatesList()
            bms.SetStateName("Telangana")
            # time.sleep(2)
            # print bms.GetCitiesList()
            bms.SetCityData("Hyderabad")
            if bms.GetMoviesData() is True :
                  print "Got Movies Data"
                  # time.sleep(2)
                  # print bms.GetMoviesList()
                  bms.SetMoviesData("NH10 (A)")
                  bms.GetTheaterData()
                  # print bms.GetTheaterList()
                  bms.SetTheaterData("PVR: Cyberabad, Inorbit Mall")
                  bms.SetMovieDate(datetime.today().date())
                  if bms.GetMoviesShowtimesData() is True :
                        print "Got Movies Showtimes Data"
                        time.sleep(2)
                        print bms.GetShowtimes()
                  
# ----------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()   