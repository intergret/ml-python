import os
import Image
import time
from numpy import array,exp
from random import random

class ANN:
	def __init__(self,trainPath,verifyPath,testPath):
		self.trainPath = trainPath
		self.verifyPath = verifyPath
		self.testPath = testPath
	
	def sigmoid(self,z):
		return 1.0 / (1.0 + exp(-z))
		
	def build(self,inNum,hidNum,outNum):
		# node number
		self.inNum = inNum
		self.hidNum = hidNum
		self.outNum = outNum
		# node outputs
		self.inOutput = [0.0]*inNum
		self.hidOutput = [0.0]*hidNum
		self.outOutput = [0.0]*outNum
		# node outputs error
		self.hidOutputError = [0.0]*hidNum
		self.outOutputError = [0.0]*outNum
		# weights matrix
		self.wIn2Hid = [[0.0]*self.hidNum for i in xrange(self.inNum)]
		self.wHid2Out = [[random()/10]*self.outNum for j in xrange(self.hidNum)]
		
	def feedForward(self):
		for j in xrange(self.hidNum):
			sum = 0.0
			for i in xrange(self.inNum):
				sum += self.inOutput[i]*self.wIn2Hid[i][j]
			self.hidOutput[j] = self.sigmoid(sum)
		
		for k in xrange(self.outNum):
			sum = 0.0
			for j in xrange(self.hidNum):
				sum += self.hidOutput[j] * self.wHid2Out[j][k]
			self.outOutput[k] = self.sigmoid(sum)
			
	def backPropagate(self,N=0.3):
		# calculate errors for output
		for k in xrange(self.outNum):
			error = self.targets[k]-self.outOutput[k]
			self.outOutputError[k] = self.outOutput[k]*(1-self.outOutput[k])*error
		
		# calculate errors for hidden layer
		for j in xrange(self.hidNum):
			error = 0.0
			for k in xrange(self.outNum):
				error += self.outOutputError[k]*self.wHid2Out[j][k]
			self.hidOutputError[j] = self.hidOutput[j]*(1-self.hidOutput[j])*error
		
		# update hid-output weights
		for j in xrange(self.hidNum):
			for k in xrange(self.outNum):
				change = N*self.outOutputError[k]*self.hidOutput[j]
				self.wHid2Out[j][k] += change
				
		# update input-hid weights
		for i in xrange(self.inNum):
			for j in xrange(self.hidNum):
				change = N*self.hidOutputError[j]*self.inOutput[i]
				self.wIn2Hid[i][j] += change
	
	def readPgm(self,file):
		im = Image.open(file)
		pixels = array(im.getdata())
		pixels = pixels.reshape(1,-1)/255.0
		return pixels.tolist()[0]
	
	def train(self):
		diremap = {'straight':0,'right':1,'left':2,'up':3}
		loop = 0
		while True:
			for root,dirs,files in os.walk(self.trainPath):
				for file in files:
					dire = file.split('_')[1]
					self.targets = [0.1]*self.outNum
					self.targets[diremap[dire]] = 0.9
					self.inOutput = self.readPgm(root+'\\'+file)
					self.feedForward()
					self.backPropagate()
			loop += 1
			if loop%20 == 0 and self.verify()>0.9:
				break
	
	def verify(self):
		right = 0
		wrong = 0
		diremap = {'straight':0,'right':1,'left':2,'up':3}
		for root,dirs,files in os.walk(self.verifyPath):
			for file in files:
				dire = file.split('_')[1]
				rightanswer = diremap[dire]
				
				self.inOutput = self.readPgm(root+'\\'+file)
				self.feedForward()
				answer = array(self.outOutput).argmax()
				if answer==rightanswer:
					right += 1
				else:
					wrong += 1
		p = 1.0*right/(right+wrong)
		print	p
		return p
		
	def test(self):
		right = 0
		wrong = 0
		diremap = {'straight':0,'right':1,'left':2,'up':3}
		for root,dirs,files in os.walk(self.testPath):
			for file in files:
				dire = file.split('_')[1]
				rightanswer = diremap[dire]
				
				self.inOutput = self.readPgm(root+'\\'+file)
				self.feedForward()
				answer = array(self.outOutput).argmax()
				if answer==rightanswer:
					right += 1
				else:
					wrong += 1
					
		print 'Test:',1.0*right/(right+wrong)
		
				
if __name__=='__main__':
	trainPath = 'C:\\Users\\Administrator\\Desktop\\ANN\\train\\'
	verifyPath = 'C:\\Users\\Administrator\\Desktop\\ANN\\verify\\'
	testPath = 'C:\\Users\\Administrator\\Desktop\\ANN\\test\\'
	
	
	TIMEFORMAT='%Y-%m-%d %X'
	print time.strftime(TIMEFORMAT,time.localtime(time.time()))
	myANN = ANN(trainPath,verifyPath,testPath)
	myANN.build(960,3,4)
	myANN.train()
	myANN.test()
	print time.strftime(TIMEFORMAT,time.localtime(time.time()))
	