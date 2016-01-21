#!/usr/bin/python

import sys

#if a number cannot be parsed from the argument, we return None
#None will be treated as infinity in this script
def evaluate(number):
	try:
		return int(number)
	except ValueError:
		return None
def evaluateWrite(number):
	wr = evaluate(number)
	if wr == None:
		return 'INF'
	else:
		return wr

#just checking if it really is a matrix
#and if it is square
def checkMatrix(matrix):
	for x in matrix:
		if len(x) != len(matrix):
			return False
	return True

#copies a matrix
def copyMatrix(matrix):
	return [[x for x in y] for y in matrix]

#similar to the function above, just altered to match path reconstruction 
#we also have and indicator whether old > new1+new2 or not
def calculateMinimumPath(old, new1, new2):
	old = evaluate(old)
	new1 = evaluate(new1)
	new2 = evaluate(new2)

	if(old==None):
		if(new1==None or new2==None):
			return ("infinity", False)
		return (new1+new2, True)
	elif(new1==None or new2==None):
		return (old, False)
	if(new1+new2 < old):
		return (new1+new2, True)
	return (old, False) 

#floydWarshall with path reconstruction 
def floydWarshallReconstructMine(graphMatrix):
	if checkMatrix(graphMatrix) == False:
		return None

	#all the matrices 
	distances = []

	#initial distance matrix
	distances = distances + [copyMatrix(graphMatrix)]

	#the path length matrix we'll be changing
	dist = copyMatrix(distances[0])

	#the path matrix
	pathList = [[[-1 for x in y] for y in graphMatrix]]

	path = copyMatrix(pathList[0])

	#for easier access
	numVertices = len(graphMatrix)

	for k in xrange(numVertices):
		for i in xrange(numVertices):
			for j in xrange(numVertices):
				minWithPath = calculateMinimumPath(dist[i][j], dist[i][k], dist[k][j])
				if(minWithPath[1]):
					dist[i][j] = minWithPath[0]
					path[i][j] = k
			if dist[i][i] < 0:
				return None
		distances = distances + [copyMatrix(dist)]
		pathList = pathList + [copyMatrix(path)]

	#pathList[k][i][j] == k if node k is in the minimal path between the nodes i and j 
	return (distances[1:], pathList[1:])

#a recursive function used to reconstruct the path of the graph
def reconstructMine(distances, pathList, v1, v2):
	#indices out of bound
	if(v1 < 0 or v2< 0 or v1 >= len(pathList[0]) or v2 >= len(pathList[0])):
		return None
	#if minimum distance is infinite, there is no path
	if(evaluate(distances[v1][v2])==None):
		return None
	#if path index is -1 but there is a branch between v1 and v2, and that branch is the shortest path 
	if(pathList[v1][v2]==-1 and evaluate(distances[v1][v2]) != None):
		return [v1, v2]

	#otherwise, we return None since there is no path
	if(pathList[v1][v2]==-1):
		return None
	#we split the path on the vertex indexed by pathList[v1][v2] and reconstruct two paths, then add them together
	path1 = reconstructMine(distances, pathList, v1, pathList[v1][v2])
	path2 = reconstructMine(distances, pathList, pathList[v1][v2], v2)
	return path1[:-1]+path2


############
#just for checking purposes
matrix = [["infinity", 3, 2, "infinity"],[1, "infinity", "infinity", 3],["infinity", -2, "infinity", 4],["infinity", "infinity", "infinity","infinity"]]
solution = [[1,0,2,3], [1,1,3,3], [-1, -2, 1, 1],["infinity", "infinity", "infinity","infinity"]]
############


#parses the input file into a matrix
def parseInputFile(path):
	try:
		openFile = open(path, 'r')
		lines = openFile.readlines()
		#lines = [x.strip() for x in lines]
		graphMatrix = [x.split() for x in lines]
		graphMatrix = [x for x in graphMatrix if x != []]
		return graphMatrix
	except IOError:
		return None

##########the beggining of the script
if len(sys.argv) != 2:
	print "You have to pass exactly 1 command line argument (path)"
	quit()
#parse the input
graphMatrix = parseInputFile(sys.argv[1])
#obtain the solution
solutionPair = floydWarshallReconstructMine(graphMatrix)

if solutionPair == None:
	print 'All the shortest paths couldn\'t be found in this graph.'
	exit()

#determine the vertices
v1=input('The first vertex of a path: ')
v2=input('The second vertex of a path: ')
#calculate the path and print it
path = reconstructMine(solutionPair[0][-1], solutionPair[1][-1], v1, v2)
if path==None:
	print 'There is no path between those two vertices.'
else:
	print 'Putanja: ', path, '	Njena tezina: ', solutionPair[0][-1][v1][v2]


#output part
lineLen = 20*len(solutionPair[0][-1])
outputFile = open('solution.txt', 'w')
for k in xrange(len(solutionPair[0])):
#	if k==0:
#		str1 = 'Distance matrix'
#		str2 = 'Path matrix'
#		str3 = str1.center(lineLen/2-len(str1)) + str2.center(lineLen/2-len(str2))+'\n\n'
#		outputFile.write(str3)
	strg = '\nIteracija broj: ' + str(k+1) + '\n'
	outputFile.write(strg)
	
	for l in xrange(len(solutionPair[0][k])):
		stringic = '| '
		for j in xrange(len(solutionPair[0][k][l])):
			stringic += str(evaluateWrite(solutionPair[0][k][l][j])).center(5)
		stringic += '  |  '
		for j in xrange(len(solutionPair[1][k][l])):
			stringic += str(evaluateWrite(solutionPair[1][k][l][j])).center(5)
		stringic += ' |\n'
		outputFile.write(stringic)
	
