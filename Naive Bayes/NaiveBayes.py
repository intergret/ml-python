from numpy import *

def LoadCorpus(dirpath):
	docList=[]; classList = [];

	for line in open(dirpath+'movie.txt','r'):
		mid = line.strip().split('\t')[0]
		blog = line.strip().split('\t')[1]
		wordList = [item for item in blog.split('&') if len(item)>3 and item!='2012']
		if len(wordList)>0:
			docList.append(wordList)
			classList.append(1)
	
	for line in open(dirpath+'notmovie.txt','r'):
		mid = line.strip().split('\t')[0]
		blog = line.strip().split('\t')[1]
		wordList = [item for item in blog.split('&') if len(item)>3 and item!='2012']
		if len(wordList)>0:
			docList.append(wordList)
			classList.append(0)
			
	return docList,classList
	
def createVocabList(dataSet):
	vocabSet = {}; id=0
	for document in dataSet:
		for word in document:
			if word not in vocabSet:
				vocabSet[word] = id
				id+=1
	return vocabSet

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList[word]] = 1
    return returnVec

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList[word]] += 1
    return returnVec

def trainNB(trainMatrix,trainClasses):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainClasses)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainClasses[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p0Vect = log(p0Num/p0Denom)
    p1Vect = log(p1Num/p1Denom)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else: 
        return 0
   
def MovieDetect(dirpath):
	docList,classList = LoadCorpus(dirpath)
	vocabList = createVocabList(docList)

	trainingSet = range(len(docList)); testSet=[]; sample=int(0.25*len(docList))
	for i in range(sample):
		randIndex = int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
		
	trainMatrix=[]; trainClasses = []
	for docIndex in trainingSet:
		trainMatrix.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])

	p0V,p1V,pSpam = trainNB(array(trainMatrix),array(trainClasses))

	errorCount = 0
	for docIndex in testSet:
		wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
			errorCount += 1
	print 'the error rate is: ',float(errorCount)/len(testSet)
	
if __name__=='__main__':
	dirpath = 'C:\\Users\\Administrator\\Desktop\\moviedetect\\'
	dirpath = './'
	MovieDetect(dirpath)