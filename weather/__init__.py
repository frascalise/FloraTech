from .AI import StartingTraining,Prediction
import os
stasi=False
if (not stasi):
    if os.path.exists("C:/Users/paolo/Desktop/università/IOT/consegna/model_parameters.pkl"):
        print("presente")
        Prediction()
    else:
        
        print("assente")
        StartingTraining()
    stasi=True