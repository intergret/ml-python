#coding=utf-8
from numpy import *

class NBClassification:
	def __init__(self,class0file,class1file,class0testfile,class1testfile,WordsToFilter):
		self.Class0File = class0file
		self.Class1File = class1file
		self.Class0TestFile = class0testfile
		self.Class1TestFile = class1testfile
		self.WordsToFilter = set(WordsToFilter)
		
		self.VocabSet = {}
		self.C0Vec = None;
		self.C1Vec = None;
		self.C0Prob = 0.0;

	def createVocabSet(self):
		id = 0
		for line in open(self.Class0File,'r'):
			for word in line.strip().split('\t')[1].split('&'):
				if word not in self.WordsToFilter and word not in self.VocabSet:
					self.VocabSet[word] = id
					id += 1
		
		for line in open(self.Class1File,'r'):
			for word in line.strip().split('\t')[1].split('&'):
				if word not in self.WordsToFilter and word not in self.VocabSet:
					self.VocabSet[word] = id
					id += 1
		
	def trainNB(self):
		numWords = len(self.VocabSet)
		self.C0Vec = ones(numWords); self.C1Vec = ones(numWords);
		c0WordNum = 2.0; c1WordNum = 2.0;
		c0Num = 0; c1Num = 0;
		
		for line in open(class0file,'r'):
			c0Num += 1
			for word in line.strip().split('\t')[1].split('&'):
				if word not in WordsToFilter :
					self.C0Vec[self.VocabSet[word]] += 1
					c0WordNum += 1
		
		for line in open(class1file,'r'):
			c1Num += 1
			for word in line.strip().split('\t')[1].split('&'):
				if word not in WordsToFilter :
					self.C1Vec[self.VocabSet[word]] += 1
					c1WordNum += 1
		
		self.C0Vec = log(self.C0Vec/c0WordNum)
		self.C1Vec = log(self.C1Vec/c1WordNum)
		self.C0Prob = 1.0*c0Num/(c0Num+c1Num)

	
	def classifyNB(self,doc):
		c0 = log(self.C0Prob)
		c1 = log(1-self.C0Prob)
		
		for word in doc:
			if word in self.VocabSet:
				wordid = self.VocabSet[word]
				c0 += self.C0Vec[wordid]
				c1 += self.C1Vec[wordid]
		
		return 0 if c0 > c1 else 1
		
		
	def testNB(self):
		c0test = 0; c0errCount = 0;
		for line in open(self.Class0TestFile,'r'):
			c0test += 1
			doc = [word for word in line.strip().split('\t')[1].split('&') if word not in self.WordsToFilter]
			if self.classifyNB(doc) != 0:
				c0errCount += 1
				
		c1test = 0; c1errCount = 0;
		for line in open(self.Class1TestFile,'r'):
			c1test += 1
			doc = [word for word in line.strip().split('\t')[1].split('&') if word not in self.WordsToFilter]
			if self.classifyNB(doc) != 1:
				c1errCount += 1
		
		print 'clas0:',c0test-c0errCount,'/',c0test,'=',(c0test-c0errCount)*1.0/c0test
		print 'clas1:',c1test-c1errCount,'/',c1test,'=',(c1test-c1errCount)*1.0/c1test
		print 'total:',(c0test-c0errCount + c1test-c1errCount)*1.0/(c0test+c1test)
		
	def runClassify(self):
		self.createVocabSet()
		self.trainNB()
		self.testNB()

	
if __name__=='__main__':
	dirpath = 'C:\\Users\\Administrator\\Desktop\\Naive Bayes\\'
	dirpath = './'
	
	class0file = dirpath + 'movie.txt'
	class1file = dirpath + 'notmovie.txt'
	class0testfile = dirpath + 'movietest.txt'
	class1testfile = dirpath + 'notmovietest.txt'
	
	WordsToFilter = ['2012']
	
	myNB = NBClassification(class0file,class1file,class0testfile,class1testfile,WordsToFilter)
	myNB.runClassify()