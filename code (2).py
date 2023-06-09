# -*- coding: utf-8 -*-
"""ERGASIA_15_11_2020.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1isF2om_P-XYulXUwP8qFOBm6fn-mKYPJ
"""

import numpy as np
from keras.utils.np_utils import to_categorical
from matplotlib import pyplot
from keras.datasets import cifar10
from sklearn.metrics import classification_report 
from sklearn.neighbors import NearestCentroid 
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
from pandas import pandas

#I load the dataset
(trainX, trainy), (testX, testy) = cifar10.load_data()

#I look at my data
print('Train: X=%s, y=%s' % (trainX.shape, trainy.shape))
print('Test: X=%s, y=%s' % (testX.shape, testy.shape))

#My dataset has 50000 32x32pixels training images, 10000 testing images with depth 3

# i look at my first 9 images to have a better idea about my data
for i in range(9):
	pyplot.subplot(330 + 1 + i)
	pyplot.imshow(trainX[i])
pyplot.show()

#I load the data again and now make the testY, trainY categorical so I can work with them
# The dataset has 10 classes so we are going to use one hot encoding for each class element
(trainX, trainY), (testX, testY) = cifar10.load_data()
trainY = to_categorical(trainY)
testY = to_categorical(testY)

#How do the images appear as an array?
index = 0
trainX[index]
#I look at the first one

#We need to normalise the pixel to values between 0 and 1
#from integer to float
def prep_pixels(train, test):
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	return train_norm, test_norm

#Create the image class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse','ship', 'truck']

#We are going to create nearest centroid classifier and see how good is the accuracy

#Get the shape of the arrays

print('trainX shape:',trainX.shape)
print('trainY shape:',trainY.shape)

#I am going to need to reshape the images so model_nc.fit can work
#I am going to use the trainy and not the trainY because it is a (50000,1) and not categorical
trainX_2d = trainX.reshape(50000,32*32*3)
testX_2d = testX.reshape(10000,32*32*3)
model_nc = NearestCentroid()

# Fit the data to the model_nc (training)
model_nc.fit(trainX_2d, trainy.ravel())

print(f"Training Set Score : {model_nc.score(trainX_2d, trainy) * 100} %") 

accuracy_model_nc = model_nc.score(testX_2d, testy) * 100
print(f"Test Set Score : {accuracy_model_nc} %") 


print(f"Nearest Centroid Model Classification Report : \n{classification_report(testy, model_nc.predict(testX_2d))}")

#We are going to create two knn model 
#The first one is a 1 nearest neighbor classifier

model_1nn = KNeighborsClassifier(n_neighbors=1)

# Fit the data to the model_1nn (training)
model_1nn.fit(trainX_2d, trainY)

print(f"Training Set Score : {model_1nn.score(trainX_2d, trainY) * 100} %") 

accuracy_model_1nn = model_1nn.score(testX_2d, testY) * 100
print(f"Test Set Score : {accuracy_model_1nn} %") 

print(f"Nearest Centroid Model Classification Report : \n{classification_report(testY, model_1nn.predict(testX_2d))}")

#The second one is a 3 nearest neighbor classifier

model_3nn = KNeighborsClassifier(n_neighbors=3)

# Fit the data to the model_nc (training)
model_3nn.fit(trainX_2d, trainY)

print(f"Training Set Score : {model_3nn.score(trainX_2d, trainY) * 100} %")

accuracy_model_3nn = model_3nn.score(testX_2d, testY) * 100
print(f"Test Set Score : {accuracy_model_3nn} %") 

print(f"Nearest Centroid Model Classification Report : \n{classification_report(testY, model_3nn.predict(testX_2d))}")

#I create a variable "compare" that compares the accuracies of the models and stores the highest one 
if accuracy_model_nc >= accuracy_model_1nn:
   if accuracy_model_nc >= accuracy_model_3nn:
        compare = accuracy_model_nc
   else: 
        compare = accuracy_model_3nn
else:
    if accuracy_model_1nn >= accuracy_model_3nn:
        compare = accuracy_model_1nn
    else:
      compare = accuracy_model_3nn

#I create a variable "best" if that stores name of the model with the highest accuracy 
if compare == accuracy_model_nc:
  best = "Nearest Centroid Classifier"
elif compare == accuracy_model_1nn:
  best = "(KNN) k-nearest neighbor, k=1 "
else:
  best = "(KNN) k-nearest neighbor, k=3 "

#I print the model with the best accuracy and the accuracy of it.
print(f"The model that has the highest accuracy is the {best} model, with an accuracy of {compare} %.")