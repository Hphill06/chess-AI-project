#this file is not really used atm, but it was planned to be able to idetnify 
#the openeing being used and could be added in later

import csv
import numpy as np
import chessmain as cm
class chessopen:
	def __init__(self,open1):
		self.openings = np.array(list(csv.reader(open("files/openfiles.csv", "r"))))[1:]
		
		self.open1 = ""
		self.full = self.getstr(open1)
		
		self.correctopen = ""
		for i in range(len(open1)):
			if(self.findopening(moves = self.getstr(open1,remove = i)) != "no opening found"):
				self.correctopen = self.findopening(moves = self.getstr(open1,remove = i))
				break
		
				
				
		
		
	def getstr(self,open1,remove = 0):
		x1 = 0
		x2 = 1
		open2 = ""
		if remove == 0:
			for i in open1:
				val = x1 % 2
				if(val == 0):	
					open2 = open2 + str(x2)+ "." + i.notation1() + " "
					x2 += 1
				else:
					open2 = open2 + (i.notation1()) + " " 
				x1 += 1
		else:
			for i in open1[0:-(remove)]:
				val = x1 % 2
				if(val == 0):	
					open2 = open2 + str(x2)+ "." + i.notation1() + " "
					x2 += 1
				else:
					open2 = open2 + (i.notation1()) + " " 
				x1 += 1
		return open2[0:-1]
	def clean(self,array,col):
		dex = {}
		for i in array:
			if i[col] in dex:
				dex[i[col]] += 1
			else:
				dex[i[col]] = 1
		for i in range(len(array)):
			if(dex[array[i][col]] != 1):
				dex[array[i][col]] -= 1
				array[i] = "null"
		finalarr = []
		for i in array:
			if (not i[0].__eq__("null")):
				finalarr.append(i)
		return finalarr
		
	def findopening(self,moves, perfectmatch = True):
		form = "name: {name}\nmoves: {moves}"
		if(perfectmatch):
			for i in self.openings:
				if(moves == i[2]):
					return form.format(name = i[1], moves =i[2])
		
		else:
			arr = np.array([])
			for i in openings:
				if(moves in (i[2])):
					arr = np.append(arr,i)
			return arr
		return "no opening found"
	

