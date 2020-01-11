# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 17:23:32 2019

@author: Steven Jonathan (github: tttdddstvn)
"""


import os
import sys
import cv2
import time
import numpy as np


inFileName = sys.argv[1]
outFileName = '2D_DFT.png'

if os.path.exists(inFileName):
    print("Input filename is: {:s}".format(inFileName))
    print("Processing DFT (may take a while for large size image) . . .")
    #-------------Convert spatial domain to frequency domain-----------
    start = time.time()  # Start time ticker###################################
    img = cv2.imread(inFileName, cv2.IMREAD_GRAYSCALE)  #Load in grayscale mode
    M, N = img.shape[0], img.shape[1]
    m = np.arange(M)  # Define a list of index by shape M
    j = np.arange(M).reshape((M,1))
    n = np.arange(N)  # Define a list of index by shape N
    k = np.arange(N).reshape((N,1))
    expUM = np.exp(-2J*np.pi*(j*m/M))  # Construct row-wise exp matrix
    expVN = np.exp(-2J*np.pi*(k*n/N))  # Construct column-wise exp matrix
    nDFT = []  # To contain the result of row wise operation
    # Using separable property of 2-D DFT -> two 1-D DFTs for faster operation
    for rows in range(M):  # Row wise operation of 1-D DFT
        tmp = img[rows, :]  # tmp is the row vector of image
        nDFT.append(np.sum(tmp*expVN, axis=1))  # Calculate without 1/MN
    nDFT = np.array(nDFT)
    nDFT = np.transpose(nDFT)  # For next operation, as if working with column
    nDFT2 = []  # To contain the result of column wise operation
    for cols in range(N):  # Column wise operation of 1-D DFT
        tmp = nDFT[cols, :]  # tmp is the column vector of image (transposed)
        nDFT2.append(np.sum(tmp*expUM, axis=1))  # Calculate without 1/MN
    nDFT2 = np.array(nDFT2)
    nDFT2 = np.transpose(nDFT2)
    print("Image DFT process done succesfully!")
    print("Shifting DC value to (0, 0) . . .")
    #----------------------Shifting the DFT image----------------------
    Mhalf = int(M/2)+int(M/2)%2  # +1 if the dimension is odd
    Nhalf = int(N/2)+int(N/2)%2  # +1 if the dimension is odd
    # Dividing the DFT result, swap and concatenate it
    uABCDver = np.concatenate((nDFT2[:, Nhalf:], nDFT2[:, :Nhalf]), axis=1)
    nDFTS2 = np.concatenate((uABCDver[Mhalf:, :], uABCDver[:Mhalf, :]), axis=0)
    end = time.time()  # End time ticker#######################################
    print("Shifting DC value done succesfully!")
    print("Converting done in {:.2f} second(s)".format(end - start))
    cv2.imwrite(outFileName, 20*np.log(abs(nDFTS2)))
    #cwd = os.path.dirname(os.path.abspath(__file__))  # Current working dir
    print("File {:s} is saved".format(outFileName))
else:
    print("File {:s} does not exist!".format(inFileName))