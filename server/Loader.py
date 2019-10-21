# import cv2
import keras
from keras.models import model_from_json
# from sklearn.utils import shuffle
import numpy as np


class Loader:
    
    def loadModel(self):
        jsonFile = open('./model.json','r')
        jsonModel = jsonFile.read()
        jsonFile.close()

        model = model_from_json(jsonModel)
        model.load_weights('./weights.h5')
        return model