#coding=utf-8
from random import random

def square_distance(pointA, pointB):
    # squared euclidean distance
    distance = 0
    dimensions = len(pointA)
    for dimension in range(dimensions):
        distance += (pointA[dimension] - pointB[dimension])**2
    return distance

class KDTreeNode():
    def __init__(self, point, left, right):
        self.point = point
        self.left = left
        self.right = right
    
    def is_leaf(self):
        return (self.left == None and self.right == None)

class KDTreeNeighbours():
    """ 
		Internal structure used in nearest-neighbours search.
    """
    def __init__(self, query_point, k):
        self.query_point = query_point
        self.k = k
        self.largest_distance = 0
        self.current_best = []

    def calculate_largest(self):
        if self.k >= len(self.current_best):
            self.largest_distance = self.current_best[-1][1]
        else:
            self.largest_distance = self.current_best[self.k-1][1]

    def add(self, point):
        sd = square_distance(point, self.query_point)
        # run through current_best, try to find appropriate place
        for i, e in enumerate(self.current_best):
            # enough neighbours, this one is farther, let's forget it
			if i == self.k:
				return
			if e[1] > sd:
				self.current_best.insert(i, [point, sd])
				self.calculate_largest()
				return
        # append it to the end otherwise
        self.current_best.append([point, sd])
        self.calculate_largest()
    
    def get_best(self):
        return [element[0] for element in self.current_best[:self.k]]
        
class KDTree():
    """ Example usage:
			from kdtree import KDTree
            data = <load data>  # iterable of points (which are also iterable, same length)
            point = <the point of which neighbours we're looking for>
            tree = KDTree.construct_from_data(data)
            nearest = tree.query(point, k=4) # find nearest 4 points
    """
    def __init__(self, data):
        def build_kdtree(point_list, depth):
            if not point_list:
                return None
			
			# select axis based on depth so that axis cycles through all valid values
            axis = depth % len(point_list[0]) # assumes all points have the same dimension

            # sort point list and choose median as pivot point,
            # TODO: better selection method, linear-time selection, distribution
            point_list.sort(key=lambda point: point[axis])
            median = len(point_list)/2 # choose median

            # create node and recursively construct subtrees
            node = KDTreeNode(point = point_list[median],
                              left  = build_kdtree(point_list[0:median], depth+1),
                              right = build_kdtree(point_list[median+1:], depth+1))
            return node
        self.root_node = build_kdtree(data, depth=0)
    
    @staticmethod
    def construct_from_data(data):
        tree = KDTree(data)
        return tree

    def query(self, query_point, k=1):
        def nn_search(node, query_point, k, depth, best_neighbours):
            if node == None:
                return
            # if we have reached a leaf, let's add to current best neighbours,
            # (if it's better than the worst one or if there is not enough neighbours)
            if node.is_leaf():
                best_neighbours.add(node.point)
                return
            
            # this node is no leaf
            
            # select dimension for comparison (based on current depth)
            axis = depth % len(query_point)
            
            # figure out which subtree to search
            near_subtree = None # near subtree
            far_subtree = None # far subtree (perhaps we'll have to traverse it as well)
            
            # compare query_point and point of current node in selected dimension
            # and figure out which subtree is farther than the other
            if query_point[axis] < node.point[axis]:
                near_subtree = node.left
                far_subtree = node.right
            else:
                near_subtree = node.right
                far_subtree = node.left

            # recursively search through the tree until a leaf is found
            nn_search(near_subtree, query_point, k, depth+1, best_neighbours)

            # while unwinding the recursion, check if the current node
            # is closer to query point than the current best,
            # also, until k points have been found, search radius is infinity
            best_neighbours.add(node.point)
            
            # check whether there could be any points on the other side of the
            # splitting plane that are closer to the query point than the current best
            if (node.point[axis] - query_point[axis])**2 < best_neighbours.largest_distance:
                nn_search(far_subtree, query_point, k, depth+1, best_neighbours)
            
            return
        
        # if there's no tree, there's no neighbors
        if self.root_node != None:
            neighbours = KDTreeNeighbours(query_point, k)
            nn_search(self.root_node, query_point, k, depth=0, best_neighbours=neighbours)
            result = neighbours.get_best()
        else:
            result = []
		
        return result
		
if __name__=='__main__':
	num = 30
	scale = 100
	data = [(int(random()*scale),int(random()*scale)) for i in range(num)]
	point = (int(random()*scale),int(random()*scale))
	tree = KDTree.construct_from_data(data)
	nearest = tree.query(point,k=2)
	print data
	print point
	print nearest
	