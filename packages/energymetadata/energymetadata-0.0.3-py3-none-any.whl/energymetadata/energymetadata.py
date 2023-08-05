class GetMetadata:
   locCount = 0
   def __init__(self, latitude, longitude):
      self.latitude = latitude
      self.longitude = longitude
      GetMetadata.locCount += 1
   def display_nb_locations(self):
      print("Total Locations %d" % GetMetadata.locCount)
   def display_location(self):
      print("Latitude : ", self.latitude, ", Longitude: ", self.longitude)