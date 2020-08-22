from tensorflow import keras
import numpy as np
import cv2

model = keras.models.load_model('./model/my_model.h5')    
classDict = {
    0: 'cardboard',
    1: 'glass',
    2: 'metal',
    3: 'paper',
    4: 'plastic',
    5: 'trash'
  }

def predictImage(image):
  image = cv2.resize(image, (100,100), interpolation = cv2.INTER_AREA)
  image = np.reshape(image, [1, 100, 100, 3])
  prob = model.predict(image)
  predict = np.argmax(prob)
  label = classDict[predict]
  confident = prob[0][predict]

  return label, confident