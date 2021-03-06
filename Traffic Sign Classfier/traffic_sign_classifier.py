# -*- coding: utf-8 -*-
"""Traffic Sign Classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vVvv5sKDTj_sJgbUm80U_ydkjbhsGmCK
"""

!git clone https://bitbucket.org/jadslim/german-traffic-signs

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential

from keras.layers import Dense,Dropout,Flatten

from keras.optimizers import Adam

from keras.utils.np_utils import to_categorical

from keras.layers.convolutional import Conv2D,MaxPooling2D

np.random.seed(0)

!ls german-traffic-signs

import pandas as pd

import random

dataset = pd.read_csv('german-traffic-signs/signnames.csv')

dataset.head()

import pickle as pkl
with open('german-traffic-signs/train.p','rb') as f:
  train_data=pkl.load(f)
with open('german-traffic-signs/test.p','rb') as f:
  test_data=pkl.load(f)
with open('german-traffic-signs/valid.p','rb') as f:
  val_data=pkl.load(f)

X_train,y_train = train_data['features'],train_data['labels']

X_test,y_test = test_data['features'],test_data['labels']

X_val,y_val = val_data['features'],val_data['labels']

import matplotlib.pyplot as plt
# %matplotlib inline

num_of_sample=[]

cols=5
num_classes=43
fig,axs=plt.subplots(nrows=num_classes,ncols=cols,figsize=(15,50))
fig.tight_layout()

for i in range(cols):
  for j,raw in dataset.iterrows():
    x_selected=X_train[y_train==j]
    axs[j][i].imshow(x_selected[random.randint(0,len(x_selected)-1),:,:],cmap=plt.get_cmap('gray'))
    axs[j][i].axis("off")
    
    if i==2:
      axs[j][i].set_title(str(j)+'-'+raw['SignName'])
      num_of_sample.append(len(x_selected))

import cv2

def grayScale(img):
  return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def equalize(img):
  return cv2.equalizeHist(img)

def preprocess(img):
  img = grayScale(img)
  img = equalize(img)
  return img/255

plt.imshow(preprocess(X_train[1]))
plt.title("Image At 1 From X_train Data")

X_train=np.array(list(map(preprocess,X_train)))
X_test=np.array(list(map(preprocess,X_test)))
X_val=np.array(list(map(preprocess,X_val)))

X_train[1]

y_train=to_categorical(y_train,43)
y_test=to_categorical(y_test,43)
y_val=to_categorical(y_val,43)

X_train=X_train.reshape(34799,32,32,1)
X_test=X_test.reshape(12630,32,32,1)
X_val=X_val.reshape(4410,32,32,1)

def lenet():
  model = Sequential()
  model.add(Conv2D(30,(5,5),input_shape=(32,32,1),activation="relu"))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Conv2D(15,(3,3),activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Flatten())
  model.add(Dense(500,activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dropout(0.2))
  model.add(Dense(43,activation='softmax'))
  model.compile(Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
  return model

model = lenet()

model.summary()

history=model.fit(X_train,y_train,epochs=10,batch_size=400,verbose=1,shuffle=1,validation_data=(x_val,y_val))

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['loss','val_loss'])
plt.title('Loss')
plt.xlabel('epoch')

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.legend(['acc','val_acc'])
plt.title('accuracy')
plt.xlabel('epoch')

import requests
from PIL import Image

url="https://i.ebayimg.com/images/g/8u4AAMXQlgtS9Ko7/s-l300.jpg"
response=requests.get(url,stream=True)
img=Image.open(response.raw)

import cv2
img_array=np.asarray(img)
res=cv2.resize(img_array,(32,32))
gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
image=cv2.bitwise_not(gray)
plt.imshow(image,cmap=plt.get_cmap('gray'))

image=image.reshape(1,32,32,1)
str(model.predict_classes(image))



,