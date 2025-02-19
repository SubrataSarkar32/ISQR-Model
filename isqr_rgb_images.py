# -*- coding: utf-8 -*-
"""ISQR_RGB_Images.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gDG1Ymec4CZMQ9pWw6put9Vk6c7-zMNy
"""

!pip install sewar

import sys
# set_printoptions(threshold=sys.maxsize)
from PIL import Image
import cv2
from google.colab.patches import cv2_imshow
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
from matplotlib import pyplot as plt
import os
import numpy as np
import random
import pandas as pd
from skimage import io

#!wget https://i.ibb.co/GxhRPnC/lake-512.jpg -O lake.jpg
#!wget https://i.ibb.co/D18bYP1/peppers-color.jpg -O peppers.jpg
#!wget https://i.ibb.co/2dckpJ9/mandril-color.jpg -O mandril.jpg
!wget https://i.ibb.co/QNsZ6z5/2015_00015.jpg -O 2015_00015.jpg
#!wget https://i.postimg.cc/0yLDZZkp/Dark-RGB-2.jpg
#!wget https://i.postimg.cc/nh1BfWmZ/Dark-RGB-1.png

files = [f for f in os.listdir(".") if os.path.isfile(f)]
print(files)

def convert (H,i_state):
    cov = np.dot(H,i_state)
    si = cov
    alpha=si[0][0]
    beta=si[1][0]
    return [alpha,beta]

def conv_img3_arcsin(img):
    small = cv2.resize(img,(256,256))
    converted = np.zeros((256,512))
    miny=np.amin(small)
    maxy=np.amax(small)
    #miny = 0
    #maxy = 255
    for i in range(0,len(small)):
        for j in range(0,len(small[0])):
            converted[i][j] = 2.0*np.arccos(np.sqrt((float(small[i][j])-float(miny))/(float(maxy)-float(miny)))) # ISQR Encoding
            H = np.array([[1,0],[0,1]])
            a1=np.cos(converted[i][j])
            a2=np.sin(converted[i][j])
            i_state= np.array([[a1],[a2]])
            c = convert(H,i_state)
            #list_st+=[c[0]**2 + c[1]**2]
            converted [i][2*j] = c[0]*255
            converted [i][2*j+1] = c[1]*255
            #converted[i][j]=small[i][j]
            #print(small[i][j])

    return converted


def conv_rgb3_arcsin(img):
    #img = cv2.imread(fname)
    #print(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    img = cv2.resize(img,(256,256))
    b, g, r    = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    b1, g1, r1 = conv_img3_arcsin(b), conv_img3_arcsin(g), conv_img3_arcsin(r)
    img = cv2.resize(img,(512,256))
    img[:,:,0], img[:,:,1], img[:,:,2] = b1, g1, r1
    #print(img)
    return img

df = pd.DataFrame()
for filey in files:
  img= cv2.imread(filey)
  print(filey)
  new1 = cv2.resize(img,(256,256))
  cv2_imshow(new1)
  conv2=conv_rgb3_arcsin(new1)
  cv2_imshow(conv2)
  cv2.imwrite("quantum_rgb.png",conv2)

def convert_a(H,i_state):
    cov = np.dot(H,i_state)
    si = cov
    alpha=si[0][0]
    beta=si[1][0]
    t=[alpha , beta]
    e=random.choices(t,weights=[alpha**2,beta**2],k=1)
    if e == alpha:
      c = 0*255
    else:
      c = 1*255
    return c

def conv_img1(img,size=256):
    small = cv2.resize(img,(size,size))
    H = np.array([[1,0],[0,1]])
    converted = np.zeros((size,size))
    img = small
    miny=np.amin(small)
    maxy=np.amax(small)
    for i in range(0,len(small)):
        for j in range(0,len(small)):
            converted[i][j] = 2.0*np.arccos(np.sqrt((float(small[i][j])-float(miny))/(float(maxy)-float(miny)))) # ISQR Encoding
            H = np.array([[1,0],[0,1]])
            a1=np.cos(converted[i][j])
            a2=np.sin(converted[i][j])
            i_state= np.array([[a1],[a2]])
            c = convert_a(H,i_state)
            #list_st+=[c[0]**2 + c[1]**2]
            #converted [i][2*j] = c[0]*255
            converted [i][j] = c
            #converted[i][j]=small[i][j]
            #converted[i][j] = (float(small[i][j])/255)* math.degrees(90) # FRQI Encoding
            #print(small[i][j])

    return converted

def conv1_rgb(img,size1=256):
    img = cv2.resize(img,(size1,size1))
    b, g, r    = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    b1, g1, r1 = conv_img1(b,size=size1), conv_img1(g,size=size1), conv_img1(r,size=size1)
    img[:,:,0], img[:,:,1], img[:,:,2] = b1, g1, r1
    return img

def convshots(img,shots=1,size=32):
    img_list=[]
    for i in range(shots):
        conv2 = conv1_rgb(img,size1=size)
        img_list += [conv2]
    converted = np.zeros((size,size,3))
    sh = 0
    print(len(img),len(img[0]),len(img[0][0]))
    for i in range(0,len(img)):
         for j in range(0,len(img[0])):
             for k in range(0,len(img[0][0])):
                #val = {}
                val = 0
                for l in range(shots):
                    #print(i,j,k,l,img_list[l][i][j][k])
                    val += img_list[l][i][j][k]
                    '''
                    if img_list[l][i][j][k] in val:
                        val[img_list[l][i][j][k]]+=1
                    else:
                        val[img_list[l][i][j][k]]=1
                keys = list(val.keys())
                print(val)
                if(len(keys)>1):
                    if val[keys[0]]>val[keys[1]]:
                        converted[i][j][k] = keys[0]
                    else:
                        converted[i][j][k] = keys[1]
                else:
                    converted[i][j][k] = keys[0]
                    '''
                converted[i][j][k] = val/shots
                #print(sh)
                sh+=1
    return converted


def grey_convshots(img,shots=1):
    img_list=[]
    for i in range(shots):
        conv2 = conv_img3_arcsin(img)
        img_list += [conv2]
    converted = np.zeros((256,256))
    sh = 0
    print(len(img),len(img[0]))
    for i in range(0,len(img)):
         for j in range(0,len(img[0])):
                #val = {}
                val = 0
                for l in range(shots):
                    #print(i,j,k,l,img_list[l][i][j][k])
                    val += img_list[l][i][j]
                    '''
                    if img_list[l][i][j][k] in val:
                        val[img_list[l][i][j][k]]+=1
                    else:
                        val[img_list[l][i][j][k]]=1
                keys = list(val.keys())
                print(val)
                if(len(keys)>1):
                    if val[keys[0]]>val[keys[1]]:
                        converted[i][j][k] = keys[0]
                    else:
                        converted[i][j][k] = keys[1]
                else:
                    converted[i][j][k] = keys[0]
                    '''
                converted[i][j] = val/shots
                #print(sh)
                sh+=1
    return converted

df = pd.DataFrame()
for filey in files:
    print(filey)
    for k in (1,10,100,1000):
      imgk = cv2.imread(filey)
      small = cv2.resize(imgk,(256,256))
      real = small
      conv = convshots(real,shots=k,size=256)
      cv2_imshow(conv)
      cv2.imwrite(filey.split(".")[0]+str(k)+"_conv_a.jpg",conv)
      restored = cv2.imread(filey.split(".")[0]+str(k)+"_conv_a.jpg")

      values = {
          "Name": filey,
          "MSE": np.round(mse(restored,real),4),
          "RMSE": np.round(rmse(restored, real),4),
          "PSNR": np.round(psnr(restored, real),4),
          "SSIM": (np.round(ssim(restored, real)[0],4),np.round(ssim(restored, real)[1],4)),
          "UQI": np.round(uqi(restored, real),4),
          "MSSSIM": np.round(msssim(restored, real).real,4),
          "ERGAS": np.round(ergas(restored, real),4),
          "SCC": np.round(scc(restored, real),4),
          "RASE": np.round(rase(restored, real),4),
          "SAM": np.round(sam(restored, real),4)
      }
      df = pd.concat([df,pd.DataFrame.from_dict([values])])
