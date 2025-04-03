import pandas as pd


class WeatherModel:
    
    precipitation_model = None

    def __init__(self):
        self.model = None #init the model with the trained one => load checkpoint
        #other stuff
    
    def get_accurate_predictions(self, api_data_raw):

        return 0 #return the list of precipitation

