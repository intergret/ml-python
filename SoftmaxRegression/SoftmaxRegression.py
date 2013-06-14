from numpy import *
import matplotlib.pyplot as plt

class SoftmaxRegression:
	def __init__(self):
		self.dataMat = []
		self.labelMat = []
		self.weights = []
		self.M = 0
		self.N = 0
		self.K = 0
		self.alpha = 0.001
		
	def loadDataSet(self,inputfile):
		for line in open(inputfile,'r'):
			items = line.strip().split()
			self.dataMat.append([1.0, float(items[0]), float(items[1])])
			self.labelMat.append(int(items[2]))
			
		self.K = len(set(self.labelMat))
		self.dataMat = mat(self.dataMat)
		self.labelMat = mat(self.labelMat).transpose()
		self.M,self.N = shape(self.dataMat)
		self.weights = mat(ones((self.N,self.K)))
		
		# self.weights = [[-1.19792777,6.05913226,-4.44164147,3.58043698],
 # [ 1.78758743,0.47379819,0.63335518,1.1052592 ],
 # [ 1.48741185,-0.18748907,1.79339685,0.90668037]]
 
 
	def likelihoodfunc(self):
		likelihood = 0.0
		for i in range(self.M):
			t = exp(self.dataMat[i]*self.weights)
			likelihood += log(t[0,self.labelMat[i,0]]/sum(t))
		print likelihood
	
	def gradientAscent(self):
		for l in range(10):
			error = exp(self.dataMat*self.weights)
			rowsum = -error.sum(axis=1)
			rowsum = rowsum.repeat(self.K, axis=1)
			error = error/rowsum
			for m in range(self.M):
				error[m,self.labelMat[m,0]] += 1
			self.weights = self.weights + self.alpha * self.dataMat.transpose()* error
			
			self.likelihoodfunc()
		print self.weights
	
	def stochasticGradientAscent_V0(self):
		for l in range(500):
			for i in range(self.M):
				error = exp(self.dataMat[i]*self.weights)
				rowsum = -error.sum(axis=1)
				rowsum = rowsum.repeat(self.K, axis=1)
				error = error/rowsum
				error[0,self.labelMat[i,0]] += 1
				self.weights = self.weights + self.alpha * self.dataMat[i].transpose()* error
				
				# self.likelihoodfunc()
		print self.weights
	
	
	def stochasticGradientAscent_V1(self):
		for l in range(500):
			idxs = range(self.M)
			for i in range(self.M):
				alpha = 4.0/(1.0+l+i)+0.01
				rdmidx = int(random.uniform(0,len(idxs)))
				error = exp(self.dataMat[rdmidx]*self.weights)
				rowsum = -error.sum(axis=1)
				rowsum = rowsum.repeat(self.K, axis=1)
				error = error/rowsum
				error[0,self.labelMat[rdmidx,0]] += 1
				self.weights = self.weights + alpha * self.dataMat[rdmidx].transpose()* error
				del(idxs[rdmidx])
				
				# self.likelihoodfunc()
		print self.weights
		
	def classify(self,X):
		p = X * self.weights
		return p.argmax(1)[0,0]
		
	def test(self):
		xcord0 = []; ycord0 = []
		xcord1 = []; ycord1 = []
		xcord2 = []; ycord2 = []
		xcord3 = []; ycord3 = []
		
		for i in range(50):
			for i in arange(80):
				x = random.uniform(-3.0, 3.0)
				y = random.uniform(0.0, 15.0)
				c = self.classify(mat([[1.0,x,y]]))
				if c==0:
					xcord0.append(x); ycord0.append(y)
				if c==1:
					xcord1.append(x); ycord1.append(y)
				if c==2:
					xcord2.append(x); ycord2.append(y)
				if c==3:
					xcord3.append(x); ycord3.append(y)
		
		# for i in range(self.M):
			# if self.labelMat[i]==0:
				# xcord0.append(self.dataMat[i,1]); ycord0.append(self.dataMat[i,2])
			# elif self.labelMat[i]==1:
				# xcord1.append(self.dataMat[i,1]); ycord1.append(self.dataMat[i,2])
			# elif self.labelMat[i]==2:
				# xcord2.append(self.dataMat[i,1]); ycord2.append(self.dataMat[i,2])
			# else:
				# xcord3.append(self.dataMat[i,1]); ycord3.append(self.dataMat[i,2])
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.scatter(xcord0, ycord0, s=20, c='yellow', marker='s')
		ax.scatter(xcord1, ycord1, s=20, c='blue')
		ax.scatter(xcord2, ycord2, s=20, c='red')
		ax.scatter(xcord3, ycord3, s=20, c='black')
		
		plt.title('inference')
		# plt.title('train data')
		plt.xlabel('X1')
		plt.ylabel('X2');
		plt.show()
	
if __name__=='__main__':
	inputfile = 'C:\\Users\\Administrator\\Desktop\\MachineLearning\\SoftmaxRegression\\SoftInput.txt'
	myclassification = SoftmaxRegression()
	myclassification.loadDataSet(inputfile)
	# myclassification.gradientAscent()
	myclassification.stochasticGradientAscent_V0()
	# myclassification.stochasticGradientAscent_V1()
	myclassification.test()
	