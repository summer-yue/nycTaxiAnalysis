#description     :# Using linear optimization techniques to find out the optimal selection of rides
#					Given a constraint on the number of taxi the company owns.
#author          :Summer Yue
#python_version  :2.7.12_2  
#==============================================================================

import pulp
import numpy
from numpy import dot
import numpy as np
import pandas as pd
import csv

#Import time vector and revenue vector from preprocessed files
revFileName = 'revenue.csv'
rev = pd.read_csv(revFileName, header=None)
rev = rev.as_matrix()
print rev
timeFileName = 'time.csv'
time = pd.read_csv(timeFileName, header=None)
time = time.as_matrix()
print time

def solveModel(capacity, timeVect, revenueVect):
	"""Linear Optimization Model for NYC taxi rides selection.
    Params: @capacity: number of taxis the company owns
    		@timeVect: binary 2D matrix with row representing each ride and column being time
    		@revenueVect: Vector on revenue on each ride, ordering same as timeVect
    """
	print("Solving model for "+ str(capacity))

	timeSectionNum = timeVect.shape[1]
	model = pulp.LpProblem("Profit maximizing problem", pulp.LpMaximize)

	tripNum = numpy.size(revenueVect)
	RANGE = range(tripNum)
	assignment = pulp.LpVariable.dicts('assignment', RANGE, cat='Binary')

	#Maximize revenue, set objective
	totalRev = 0
	for j in range(tripNum):
		totalRev += assignment[j]*revenueVect[j][0]
	model += totalRev

	time = []
	#print "Time Vect: ", timeVect
	for i in xrange(timeSectionNum):
		time.append(pulp.LpAffineExpression([(assignment[j], timeVect[j][i]) for j in range(tripNum)]))

	print('time')
	print(time)
	#Setting time constraint
	for temp in xrange(timeSectionNum):
		timeVal = time[temp]
		# print('timeVal')
		# print(timeVal)
		# print('capacity')
		# print(capacity)
		
		print(timeVal <= capacity)
		model += pulp.LpConstraint(e=timeVal, sense=-1, name=str(temp)+"time_constraint", rhs=capacity)
	print "Objective was: ", model
	optimization_result = model.solve()
	# print('Objective becomes')
	# print pulp.value(model.objective)
	# print('optimization_result')
	# print(optimization_result)
	# print(time)
	with open("result.csv","wb") as out:
		writer = csv.writer(out)
		for i in xrange(tripNum):
			print (assignment[i].value())
			writer.writerow(assignment[i].value())

solveModel(5, time, rev)

