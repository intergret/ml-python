#coding=utf-8
from numpy import *
import operator
from os import listdir
import time

class KNN:
	def __init__(self,workdir):
		self.WorkDir = workdir
	
	def classify(self,vectorTest, dataSet, labels, K):
		dataSetSize = dataSet.shape[0]
		diffMat = tile(vectorTest, (dataSetSize,1)) - dataSet
		sqDiffMat = diffMat**2
		sqDistances = sqDiffMat.sum(axis=1)
		distances = sqDistances**0.5
		sortedDistIndicies = distances.argsort()
		classCount={}
		for i in range(K):
			voteIlabel = labels[sortedDistIndicies[i]]
			classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
		sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
		return sortedClassCount[0][0]
	
	def img2vector(self,filename):
		returnVect = zeros((1,1024))
		fr = open(self.WorkDir+filename)
		for i in range(32):
			lineStr = fr.readline()
			for j in range(32):
				returnVect[0,32*i+j] = int(lineStr[j])
		return returnVect
	
	def classifyHandWriting(self,K):
		hwLabels = []
		trainingFileList = listdir(self.WorkDir+'trainingDigits')
		m = len(trainingFileList)
		trainingMat = zeros((m,1024))
		for i in range(m):
			fileNameStr = trainingFileList[i]
			fileStr = fileNameStr.split('.')[0]
			classNumStr = int(fileStr.split('_')[0])
			hwLabels.append(classNumStr)
			trainingMat[i,:] = self.img2vector('trainingDigits//%s' % fileNameStr)
		
		testFileList = listdir(self.WorkDir+'testDigits')
		errorCount = 0.0
		mTest = len(testFileList)
		for i in range(mTest):
			fileNameStr = testFileList[i]
			fileStr = fileNameStr.split('.')[0]
			classNumStr = int(fileStr.split('_')[0])
			vectorTest = self.img2vector('testDigits//%s' % fileNameStr)
			classifierResult = self.classify(vectorTest, trainingMat, hwLabels, K)
			
			if (classifierResult != classNumStr):
				errorCount += 1.0
		
		print "\nthe total error rate is: %f" % (errorCount/float(mTest))
	
if __name__=='__main__':
	workdir = 'C:\\Users\\Administrator\\Desktop\\MachineLearning\\k-Nearest Neighbor\\'
	begin = time.time()
	myKNN = KNN(workdir)
	myKNN.classifyHandWriting(6)
	print str(time.time()-begin)+' seconds'
	