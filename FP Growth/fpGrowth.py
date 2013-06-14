#coding=utf-8

class treeNode:
	def __init__(self, nameValue, numOccur, parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None
		self.parent = parentNode      #needs to be updated
		self.children = {} 
	
	def inc(self, numOccur):
		self.count += numOccur
		
	def disp(self, ind=1):
		print '  '*ind, self.name, ' ', self.count
		for child in self.children.values():
			child.disp(ind+1)

def createTree(dataSet, minSup=1):
	headerTable = {}
	#go over dataSet counts frequency of occurance
	for trans in dataSet:
		for item in trans:
			headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
			
	#remove items not meeting minSup
	for k in headerTable.keys():
		if headerTable[k] < minSup: 
			del(headerTable[k])
	
	freqItemSet = set(headerTable.keys())
	#if no items meet min support -->get out
	if len(freqItemSet) == 0:
		return None, None
	#reformat headerTable to use Node link
	for k in headerTable:
		headerTable[k] = [headerTable[k], None]
	#create tree
	retTree = treeNode('Null Set', 1, None)
	for tranSet, count in dataSet.items():
		localD = {}
		#put transaction items in order
		for item in tranSet:
			if item in freqItemSet:
				localD[item] = headerTable[item][0]
		if len(localD) > 0:
			orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
			#populate tree with ordered freq itemset
			updateTree(orderedItems, retTree, headerTable, count)
	return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
	#check if orderedItems[0] in retTree.children
	if items[0] in inTree.children:
		#incrament count
		inTree.children[items[0]].inc(count)
	else:
		#add items[0] to inTree.children
		inTree.children[items[0]] = treeNode(items[0], count, inTree)
		if headerTable[items[0]][1] == None: #update header table 
			headerTable[items[0]][1] = inTree.children[items[0]]
		else:
			updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
	#call updateTree() with remaining ordered items
	if len(items) > 1:
		updateTree(items[1::], inTree.children[items[0]], headerTable, count)
		
def updateHeader(nodeToTest, targetNode):
	while (nodeToTest.nodeLink != None):
		nodeToTest = nodeToTest.nodeLink
	nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath):
	#ascends from leaf node to root
	if leafNode.parent != None:
		prefixPath.append(leafNode.name)
		ascendTree(leafNode.parent, prefixPath)
	
def findPrefixPath(basePat, treeNode):
	#treeNode comes from header table
	condPats = {}
	while treeNode != None:
		prefixPath = []
		ascendTree(treeNode, prefixPath)
		if len(prefixPath) > 1: 
			condPats[frozenset(prefixPath[1:])] = treeNode.count
		treeNode = treeNode.nodeLink
	return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
	bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
	#start from bottom of header table
	for basePat in bigL:
		newFreqSet = preFix.copy()
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
		#construct cond FP-tree from cond. pattern base
		myCondTree, myHead = createTree(condPattBases, minSup)
		#mine cond. FP-tree
		if myHead != None:
			mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def loadSimpDat():
	simpDat = [['r', 'z', 'h', 'j', 'p'],
			   ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
			   ['z'],
			   ['r', 'x', 'n', 'o', 's'],
			   ['y', 'r', 'x', 'z', 'q', 't', 'p'],
			   ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
	return simpDat

def createInitSet(dataSet):
	retDict = {}
	for trans in dataSet:
		retDict[frozenset(trans)] = 1
	return retDict

if __name__ == '__main__':
	minSup = 3
	simpDat = loadSimpDat()
	initSet = createInitSet(simpDat)
	
	myFPtree, myHeaderTab = createTree(initSet, minSup)
	myFPtree.disp()
	
	myFreqList = []
	mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
	print myFreqList
