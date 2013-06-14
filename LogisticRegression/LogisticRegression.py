from numpy import *
import matplotlib.pyplot as plt

class LogisticRegression:
	def __init__(self):
		self.dataMat = []
		self.labelMat = []
		self.weights = []
		self.M = 0
		self.N = 0
		self.alpha = 0.001
		
	def loadDataSet(self,inputfile):
		for line in open(inputfile,'r'):
			items = line.strip().split()
			self.dataMat.append([1.0, float(items[0]), float(items[1])])
			self.labelMat.append(int(items[2]))
		
		self.dataMat = mat(self.dataMat)
		self.labelMat = mat(self.labelMat).transpose()
		self.M,self.N = shape(self.dataMat)
		self.weights = mat(ones((self.N,1)))
		# self.weights = [[3.0317079],[0.58242302],[-0.58782357]]
		
	def sigmoid(self,z):
		return 1.0 / (1.0 + exp(-z))
	
	def classify(self,X):
		return 1 if self.sigmoid(sum(X*self.weights)) > 0.5 else 0
	
	def gradientAscent(self):
		for k in range(1000):
			error = (self.labelMat - self.sigmoid(self.dataMat*self.weights))
			self.weights += self.alpha * self.dataMat.transpose()* error
		print self.weights
		
	def stochasticGradientAscent_V0(self):
		for l in range(300):
			for i in range(self.M):
				error = self.labelMat[i] - self.sigmoid(sum(self.dataMat[i]*self.weights))
				self.weights += self.alpha * self.dataMat[i].transpose() * error
				
	def stochasticGradientAscent_V1(self):
		for l in range(300):
			idxs = range(self.M)
			for i in range(self.M):
				alpha = 4.0/(1.0+l+i)+0.01
				rdmidx = int(random.uniform(0,len(idxs)))
				error = self.labelMat[rdmidx] - self.sigmoid(sum(self.dataMat[rdmidx]*self.weights))
				self.weights += self.alpha * self.dataMat[rdmidx].transpose() * error
				del(idxs[rdmidx])
	
	def plotSeperator(self):
		xcord1 = []; ycord1 = []
		xcord2 = []; ycord2 = []
		for i in range(self.M):
			if int(self.labelMat[i])== 1:
				xcord1.append(self.dataMat[i,1]); ycord1.append(self.dataMat[i,2])
			else:
				xcord2.append(self.dataMat[i,1]); ycord2.append(self.dataMat[i,2])
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.scatter(xcord1, ycord1, s=30, c='yellow', marker='s')
		ax.scatter(xcord2, ycord2, s=30, c='blue')
		x = arange(-3.0, 3.0, 0.1)
		w = self.weights.getA()
		y = (-w[0]-w[1]*x)/w[2]
		ax.plot(x, y)
		plt.xlabel('X1')
		plt.ylabel('X2');
		plt.show()
		
if __name__=='__main__':
	inputfile = 'C:\\Users\\Administrator\\Desktop\\MachineLearning\\LogisticRegression\\LogisticInput.txt'
	myregression = LogisticRegression()
	myregression.loadDataSet(inputfile)
	# myregression.gradientAscent()
	# myregression.stochasticGradientAscent_V0()
	myregression.stochasticGradientAscent_V1()
	myregression.plotSeperator()