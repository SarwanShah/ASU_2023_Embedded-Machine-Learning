# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 20:06:55 2024

@author: sarwa
"""

import numpy as np
from scipy.io.wavfile import write

def convertToWav(samples, sampleRate, depth, outputFile):
    maxVal = 2 ** (depth - 1) - 1
    normalizedSamples = np.clip(samples, -maxVal, maxVal).astype(np.int16)
    write(outputFile, sampleRate, normalizedSamples)

def getSamples(filePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 2:
                continue
            try:
                sample = int(parts[1])
                samples.append(sample)
            except ValueError:
                continue

filePath = "North.txt"
sampleRate = 16000 
bitDepth = 16 
outputFile = "output.wav" 
samples = getSamples(filePath)

convertToWav(np.array(samples), sampleRate, bitDepth, outputFile)
