from numpy import *

def loadDataSet():
	return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	#use frozen set so we can use it as a key in a dict
	return map(frozenset, C1)

def scanD(D, Ck, minSupport):
	ssCnt = {}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if not ssCnt.has_key(can): ssCnt[can]=1
				else: ssCnt[can] += 1
	numItems = float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support >= minSupport:
			retList.insert(0,key)
		supportData[key] = support
	return retList, supportData

def aprioriGen(Lk, k):
	#creates Ck
	retList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i+1, lenLk):
			L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
			L1.sort(); L2.sort()
			#if first k-2 elements are equal
			if L1 == L2:
				#set union
				retList.append(Lk[i] | Lk[j])
	return retList

def apriori(dataSet, minSupport = 0.5):
	C1 = createC1(dataSet)
	D = map(set, dataSet)
	L1,supportData = scanD(D, C1, minSupport)
	L = [L1]
	k = 2
	while (len(L[k-2]) > 0):
		Ck = aprioriGen(L[k-2], k)
		Lk, supK = scanD(D, Ck, minSupport)
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L, supportData

def generateRules(L, supportData, minConf=0.7):
	bigRuleList = []
	#only get the sets with two or more items
	for i in range(1, len(L)):
		for freqSet in L[i]:
			H1 = [frozenset([item]) for item in freqSet]
			if (i > 1):
				rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
			else:
				calcConf(freqSet, H1, supportData, bigRuleList, minConf)
	return bigRuleList		   

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
	prunedH = []
	for conseq in H:
		conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
		if conf >= minConf: 
			brl.append((freqSet-conseq, conseq, conf))
			prunedH.append(conseq)
	return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
	m = len(H[0])
	#try further merging
	if (len(freqSet) > (m + 1)):
		#create Hm+1 new candidates
		Hmp1 = aprioriGen(H, m+1)
		#create Hm+1 new candidates
		Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
		#need at least two sets to merge
		if (len(Hmp1) > 1):
			rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__=='__main__':
	dataSet = loadDataSet()
	L,suppData = apriori(dataSet)
	for set,supp in suppData.iteritems():
		print set,'support:',supp
	
	rules = generateRules(L,suppData, minConf=0.7)
	for preseq,conseq,conf in rules:
		print preseq,'-->',conseq,'conf:',conf