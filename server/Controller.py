import cv2
import glob
import shutil,os
import numpy as np
import ctypes as ct
import substring
from spellchecker import SpellChecker
from keras import backend as K
from Loader import Loader

class CImage(ct.Structure):
    _fields_ = [
        ('rows',ct.c_int),
        ('cols',ct.c_int),
        ('name',ct.c_char_p),
        ('pixels',ct.POINTER(ct.c_int)),
    ]

class Package(ct.Structure):
    _fields_ =[
        ('count',ct.c_int),
        ('letters',CImage * 0),
    ]

class Controller:

    loader = None
    model = None
    image = None

    images = []
    codes = []
    names = []

    def __init__(self,req):
        
        self.images.clear()
        self.codes .clear()
        self.names.clear()

        K.clear_session()
        self.loader = Loader()
        self.model = self.loader.loadModel()

        self.image = self.buildInitialImage(req['data'],req['height'],req['width'])

        try:
            dll = ct.cdll.LoadLibrary("./imageProcessingd.dll")

            main = dll.main

            main.argtypes = [
                np.ctypeslib.ndpointer(dtype=np.int, ndim=2, flags='C_CONTIGUOUS'),
                ct.c_int,
                ct.c_int
            ]

            main.restype = ct.POINTER(Package)

            package = main(self.imageToArray(self.image), req['height'], req['width'])

            package = package.contents
            
            cImages = ct.cast(ct.byref(package.letters),ct.POINTER(CImage * package.count)).contents
  
            for cImage in cImages:
                image = np.ctypeslib.as_array(cImage.pixels,shape=(cImage.rows,cImage.cols))
              
                width = 2
                top, bottom, left, right = [width]*4
                image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
                image = cv2.resize(np.uint8(image),(32,32))
                self.images.append(image)

                code = cImage.name.decode("utf-8")
                self.names.append(code)
                array = code.split('.')
                dictionary = {
                    "row" : int(array[0]),
                    "word" : int(array[1]),
                    "letter" : int(array[2])
                }
                self.codes.append(dictionary)

            dll.myFree.argtypes = ct.POINTER(Package),
            dll.myFree.restype = None
            dll.myFree(package)

            self.saveLetters()

        except Exception as e:
            print(str(e))
      


    def buildInitialImage(self,array,height,width):
        image = np.zeros((height,width))
        row=0
        col=-1
        for i in range(0,height*width*4,4):
            col+=1
            if(col%width==0 and col!=0):
                row +=1
                col=0
            blue = array[i+2]
            green = array[i+1]
            red = array[i]
            image[row][col] = 0.3*red + 0.59*green + 0.11 * blue
        return image

    def imageToArray(self,image):
        return np.asanyarray(image,dtype=np.int)

    def saveLetters(self):
        for i in range(len(self.images)):
            cv2.imwrite("./images/" + self.names[i] + ".png",self.images[i])

    def recognize(self):
        
        _images = np.asarray(self.images)
        _images = _images.reshape(len(_images), 32, 32,1)

        predictions = self.model.predict_classes(_images)
        text = self.buildText(predictions)

        return text

    def buildText(self,predictions):
        text = ""
        previousRow = 0
        previousWord = 0

        for i in range(len(predictions)):
            letter = self.dictionary[predictions[i]]
            
            if self.codes[i]['row'] != previousRow:
                text = text + "\n"
                previousRow = self.codes[i]['row']
                previousWord =0
            if self.codes[i]['word'] != previousWord:
                text = text + " "
                previousWord = self.codes[i]['word']  
            text = text + letter
        
        text = self.check(text)

        return text

    def check(self,text):
        array = text.split(" ")
        for i in range(len(array)):
            if array[i][0].islower():
                array[i] = array[i].lower()
        spell = SpellChecker(distance=1)
        output = ""
        for i in range(len(array)):
            output = output + spell.correction(array[i]) + " "
        return output

    dictionary = {
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'A',
            11: 'B',
            12: 'C',
            13: 'D',
            14: 'E',
            15: 'F',
            16: 'G',
            17: 'H',
            18: 'I',
            19: 'J',
            20: 'K',
            21: 'L',
            22: 'M',
            23: 'N',
            24: 'O',
            25: 'P',
            26: 'Q',
            27: 'R',
            28: 'S',
            29: 'T',
            30: 'U',
            31: 'V',
            32: 'W',
            33: 'X',
            34: 'Y',
            35: 'Z',
            36: 'a',
            37: 'b',
            38: 'c',
            39: 'd',
            40: 'e',
            41: 'f',
            42: 'g',
            43: 'h',
            44: 'i',
            45: 'j',
            46: 'k',
            47: 'l',
            48: 'm',
            49: 'n',
            50: 'o',
            51: 'p',
            52: 'q',
            53: 'r',
            54: 's',
            55: 't',
            56: 'u',
            57: 'v',
            58: 'w',
            59: 'x',
            60: 'y',
            61: 'z',
        }
