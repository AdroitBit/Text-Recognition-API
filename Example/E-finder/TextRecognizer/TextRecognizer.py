import numpy as nm
from math import *
import random
from glob import *
import os

import tkinter as tk
from tkinter import filedialog
import re as regex#finding a way to do string.split("regexp string","regexp attribute") instead of regex.split("regexp string","string")
#well...python should be prototype language...like javascript does
import types 

import cv2
import pytesseract
from pytesseract import Output
from PIL import ImageGrab
import pyautogui
pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe";
root=tk.Tk();
root.withdraw()
def isreal(x):
	return not isnan(x)
def forallNaN(*x):
	for	i in x:
		if isreal(i):
			return False
	return True
def forsomeNaN(*x):
	for i in x:
		if isnan(i):
			return True
	return False
def forallReal(*x):
	for i in x:
		if isnan(i):
			return False
	return True
def forsomeReal(*x):
	for i in x:
		if isreal(i):
			return True
	return False
def isiterable(x):
	if isinstance(x,list):
		return True
	else:
		return hasattr(x, '__iter__')
def forallNone(*x):
	for i in x:
		if not(i is None):
			return False
	return True
def forsomeNone(*x):
	for i in x:
		if i is None:
			return True
	return False
def pickFolder(title="",startDir=""):
	return filedialog.askdirectory(title=title,initialdir=startDir)
def pickFiles(title="",startDir=""):
	return filedialog.askopenfilenames(title=title,initialdir=startDir)
def pickFile(title="",startDir=""):
	return filedialog.askopenfilename(title=title,initialdir=startDir)
def show_img(img,wait=True):
	cv2.imshow("asd",img.data);
	if(wait):
		cv2.waitKey(0);
	return img
def show_imgs(imgs,wait=True):
	for i in imgs.imgs:
		show_img(i,wait);
	return imgs
def createPath(path):
		try:
			os.makedirs(path)
		except OSError:
			if(os.path.isdir(path)):
				return -2
			else:
				return -1
		else:
			return 0
	

from TextRecognizer.TextManager import *
from TextRecognizer.Image import *