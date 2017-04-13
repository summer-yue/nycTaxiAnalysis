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

#Import time vector and revenue vector from preprocessed files
revFileName = 'testrev.csv'
rev = pd.read_csv(revFileName, header=None)
rev = rev.as_matrix()
print rev
timeFileName = 'testtime.csv'
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
	assignment = pulp.LpVariable.dicts('assignment', RANGE, lowBound=0, upBound=1, cat='Binary')

	#Maximize revenue, set objective
	totalRev = 0
	for j in range(tripNum):
		totalRev += assignment[j]*revenueVect[j][0]
	model += totalRev

	time = np.zeros((1, timeVect.shape[1]))

	print("TIME.SHAPE")
	print(time.shape)

	#capacity_vec = np.array([capacity]*timeSectionNum)
	for i in xrange(tripNum):
		if (assignment[i] == 1):
			time = np.add(time, timeVect[i][:])

	print(time.shape)

	#Setting time constraint
	#model += pulp.LpConstraint(e=np.array(time[0]), sense=-1, name="time_constraint", rhs=capacity_vec)
	for temp in xrange(timeSectionNum):
		timeVal = time[0][temp]
		print('timeVal')
		print(timeVal)
		print('capacity')
		print(capacity)
		
		print(timeVal <= capacity)
		model +=  pulp.LpConstraint(timeVal <= capacity)
		#model += pulp.LpConstraint(e=timeVal, sense=-1, name=str(temp)+"time_constraint", rhs=capacity)

	optimization_result = model.solve()
	print('Objective becomes')
	print pulp.value(model.objective)
	print('optimization_result')
	print(optimization_result == pulp.LpStatusOptimal)
	print(time)
	for i in xrange(tripNum):
		print (assignment[i].value())

solveModel(1, time, rev)

