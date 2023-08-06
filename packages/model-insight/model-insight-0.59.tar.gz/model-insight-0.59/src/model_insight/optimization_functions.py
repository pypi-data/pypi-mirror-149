# -*- coding: utf-8 -*-
"""
Created on April 13,  2022

@author: wang Haihua
"""
import pandas as pd
import pulp
from datetime import datetime
import numpy as np

#################################################################################################
###############################     1 Heuristic Algorithms        ###############################
#################################################################################################

####***************************     1.1 Simulated Annealing       ****************************###

def Simulated_Annealing(f, x, alpha=.99, t=10000, delta=.1, maxIter=1000):
        
    ''' Simulated Annealing Algorithm (objective: find global minimum)

    Parameters:
    ----------
    f - objective function, R^n -> R
    x - inital solution, starting point, R^n
    alpha - annealing schedule parameter
    t - inital temperature
    delta - neighborhood radius
    maxIter - maximum no. of iterations  
    
    Yields :
    --------
    result : a dictionary contains the following parameters
        - 'x_opt' : the optimal x value(s)
        - 'f_opt' : the optimal value of the objective function
        - 'x_hist': the array of x values
        - 'f_hist': the array of the objective function
        - 'time'  : time
    ''' 

    
    # initializing starting parameters
    results = {'x_opt':x, 'f_opt':f(x), 'x_hist':[x], 'time':[0],
               'f_hist':[f(x)], 'temp':[t], 'transProb':[0]}
    
    currIter = 1
    finished = False
    x_s = x    
    time_0 = datetime.now() # to measure speed
    
    while not finished:
        
        # x_c - uniformly drawing a candidate solution from neighborhood of x_s
        unif = np.random.rand(len(x_s))
        x_c = x_s + (-delta + 2*delta*unif)
    
        # A - calculating Metropolis activation function
        A = np.minimum(1, np.exp(-(f(x_c) - f(x_s)) / t))
    
        # transition to candidate solution
        if bool(np.random.rand(1) < A):
            x_s = x_c
        
        # temperature update for the next iteration
        t = alpha * t

    
        if currIter < maxIter:
            
            # if better solution, update results
            if f(x_s) < f(results['x_opt']):
                results['x_opt'] = x_s
                results['f_opt'] = f(x_s)
            
            # update results history
            results['x_hist'].append(x_s)
            results['f_hist'].append(f(x_s))
            results['time'].append((datetime.now() - time_0).microseconds)

            results['transProb'].append(A)
        else:
            finished = True
        
        # if currIter % 250 == 0:
        #     print(f"f_opt after {currIter} iterations: {results['x_opt']} \n")
        
        currIter += 1
    print('The optimal x:',results['x_opt'])
    print('The optimal objective function :',results['f_opt'])
    return results['x_opt'],results['f_opt']


####***************************     1.2 Genetic Algorithm       ****************************###

# two helper functions
def binToInt(x):
    # Translate the binary chromosome to real values
    flipped = np.flipud(x)
    idx = np.argwhere(flipped==1).reshape(-1,)
    return (2**idx).sum()
  
def getCoords(population, cel, x_min, x_max):
    # Transform the binary chromosome of size 'cel' into real values of size 2
    coords = np.zeros((population.shape[0], 2))
    for i in range(population.shape[0]):
        for j in range(2): # test for more dimensions in spare time
            coordTemp = binToInt(population[i, (j*cel):((j+1)*cel)])
            # ensuring we are not leaving bounding box
            coords[i, j] = ((x_max[j]-x_min[j])/(2**cel))*coordTemp + x_min[j]
            
    return(coords)


def Genetic_Algorithm(f, x_min=[-20, -20], x_max=[20, 20], cel=50,
                     popSize=30, pMut=0.05, maxIter=1000):

    ''' Genetic Algorithm (objective: find global minimum)

    Parameters:
    ----------
    - f: objective function, R^n -> R
    - x_min: vector of the minimum values of coordinates, 
    - x_max: vector of the maximum values of coordinates
    - cel: coordinate encryption length, number of genes in a single chromosome
    - popSize: size of the population
    - pMut: probability of single genome mutation
    - maxIter: number of generations
    
    Yields :
    --------
    results : a dictionary contains the following parameters
        - 'x_opt' : the optimal x value(s)
        - 'f_opt' : the optimal value of the objective function
        - 'x_hist': the array of x values
        - 'f_hist': the array of the objective function
        - 'time'  : time
    ''' 

  
    # initializing history
    results = {'x_opt':[], 'f_opt':[], 'x_hist':[], 'f_mean':[], 
               'f_hist':[], 'time':[]}

    # Check the number of dimensions
    d = len(x_min) 
        
    # Initialize population
    population = np.zeros((popSize, cel*d))
      
    for i in range(popSize):
        # .5 chosen arbitrarily
        population[i,] = np.random.uniform(size=cel*d) > .5 
    
    coordinates = getCoords(population, cel, x_min, x_max)
      
    # Calculate fittness of individuals
    objFunction = np.zeros((popSize,))
    for i in range(popSize):
        objFunction[i] = f(coordinates[i,])
    
    # Assign the first population to output 
    results['x_opt'] = coordinates[np.argmin(objFunction),]
    results['f_opt'] = f(coordinates[np.argmin(objFunction),])
      
    # The generational loop
    finished = False
    currIter = 1
    time_0 = datetime.now() # to measure speed

    
    while not finished:
        # Assign the output
        if currIter <= maxIter:
            if results['f_opt'] > f(coordinates[np.argmin(objFunction),]):
                results['x_opt'] = coordinates[np.argmin(objFunction),]
                results['f_opt'] = f(coordinates[np.argmin(objFunction),])
          
            results['f_hist'].append(results['f_opt'])
            results['x_hist'].append(coordinates[np.argmin(objFunction),])
            results['f_mean'].append(np.mean(objFunction))
            results['time'].append((datetime.now() - time_0).microseconds)
        else:
          finished = True

        
        # Translate binary coding into real values to calculate function value
        coordinates = getCoords(population, cel, x_min, x_max)
        
        # Calculate fittness of the individuals
        objFunction = np.zeros((popSize,))
        for i in range(popSize):
            objFunction[i] = f(coordinates[i,])
        
        np.warnings.filterwarnings('ignore')

        rFitt = np.divide(min(objFunction), objFunction) # relative fittness
        # relative normalized fittness (sum up to 1) :
        nrFitt = np.divide(rFitt, sum(rFitt))
                
        # Selection operator (roulette wheel), analogy to disk
        selectedPool = np.zeros((popSize,))
        for i in range(popSize):
            selectedPool[i] = np.argmin(np.random.uniform(size=1) > np.cumsum(nrFitt))

        
        # Crossover operator (for selected pool)
        nextGeneration = np.zeros((popSize, cel*d))
        for i in range(popSize):
            parentId = int(np.round(np.random.uniform(1, popSize-1, 1)))
            cutId = int(np.round(np.random.uniform(1, d*cel-2, 1)))
            # Create offspring
            nextGeneration[i, :cutId] = population[int(selectedPool[i]), :cutId]
            nextGeneration[i, cutId:(d*cel)] = population[int(selectedPool[parentId]), cutId:(d*cel)]
        
        # Mutation operator
        for i in range(popSize):
            # Draw the genomes that will mutate
            genomeMutId = np.argwhere(np.random.rand(d*cel) < pMut)
            for j in range(len(genomeMutId)):
                nextGeneration[i, genomeMutId[j]] = not nextGeneration[i, genomeMutId[j]] 
        
        # Replace the old population
        population = nextGeneration
        currIter += 1

    print('The optimal x:',results['x_opt'])
    print('The optimal objective function :',results['f_opt'])
    return results['x_opt'],results['f_opt']


####***************************     1.3 Particle Swarm Optimization       ****************************###

def PSO(f, swarm_size=20, max_iter=200, x_min=[-20,-20], x_max=[20,20],
        c1=1, c2=1, omega=.5):

    ''' Particle Swarm Optimization (objective: find global minimum)

    Parameters:
    ----------
    - f: objective function, R^n -> R,
    - x_min: vector of the minimum values of coordinates, 
    - x_max: vector of the maximum values of coordinates,
    - swarm_size: number of particles in the swarm
    - max_iter: maximum number of iterations
    - c1: weight of personal best result of a particule
    - c2: weight of global best result of a swarm
    - omega: weight of current velocity
    
    Yields :
    --------
    results : a dictionary contains the following parameters
        - 'x_opt' : the optimal x value(s)
        - 'f_opt' : the optimal value of the objective function
        - 'x_hist': the array of x values
        - 'f_hist': the array of the objective function
        - 'time'  : time
    '''

    
    dim = len(x_min) 
    r = np.empty((swarm_size, dim))
    s = np.empty((swarm_size, dim))
    
    # initializing swarm
    swarm = np.empty((swarm_size, dim))
    velocity = np.empty((swarm_size, dim))
    p_best = np.empty((swarm_size, dim))
    swarm_result = np.empty((swarm_size, 1))
    
    # for each particle and each dimension initialize starting points
    for i in range(swarm_size):
        for j in range(dim):
            swarm[i, j] = np.random.uniform(low=x_min[j], high=x_max[j], size=1)
        velocity[i,:] = np.random.uniform(low=0, high=1, size=dim)
        p_best[i,:] = swarm[i,:]
        swarm_result[i] = f(swarm[i,:])
        g_best = swarm[np.argmin(swarm_result),:] # updating global best solution
    
    results = {'x_opt': [g_best], 'f_opt':[f(g_best)], 'x_hist':[g_best],
               'f_hist':[f(g_best)], 'time':[0]}

    
    pocz_iter = datetime.now()
    
    for k in range(max_iter):
        
        for m in range(swarm_size):
            r[m, :] = np.random.uniform(low=0, high=1, size=dim)
            s[m, :] = np.random.uniform(low=0, high=1, size=dim)
            
            # calculating components of new velocity
            old_vel = omega * velocity[m,:] # old velocity comp.
            best_pers_vel = c1 * r[m,:] * (p_best[m,:]-swarm[m,:]) # personal best comp.
            best_glob_vel = c2 * s[m,:] * (g_best-swarm[m,:]) # global best comp.
            # calculating new velocity
            velocity[m, :] = old_vel + best_pers_vel + best_glob_vel 
            # moving a particle in a new direction
            swarm[m, :] += velocity[m, :]
            
            # updating best solution for particle m
            if f(swarm[i,]) < f(p_best[i,]):
                p_best[m, :] = swarm[m, :]
            swarm_result[m] = f(swarm[m, :])
 

       
        # updating global best particle in iteration k
        if min(swarm_result)[0] < f(g_best):
            g_best = swarm[np.argmin(swarm_result), :]
        
        # saving history
        if results['f_opt'] > f(g_best):
            results['x_opt'] = swarm[np.argmin(swarm_result),:]
            results['f_opt'] = f(swarm[np.argmin(swarm_result),:])
        
        results['x_hist'].append(g_best)
        results['f_hist'].append(f(g_best))
        results['time'].append((datetime.now()-pocz_iter).microseconds)
    print('The optimal x:',results['x_opt'])
    print('The optimal objective function :',results['f_opt']) 
    return results['x_opt'],results['f_opt']


#################################################################################################
###############################     2 DEA                         ###############################
#################################################################################################

# The core DEA class, setting up and solving the linear programming
# problems using PuLP.


class DEAProblem:

    """
    A container for the elements of a data envelopment analysis problem. Sets
    up the linear programmes and solves them with pulp.

    Requires:

        inputs: a pandas dataframe of the inputs to the DMUs
        outputs: a pandas dataframe of the outputs from the DMUs
        kind: 'VRS' or 'CRS'
        in_weights: the weight restriction to apply to all inputs to all DMUs
                    (default is [0, inf])
        out_weights: the weight restriction to apply to all outputs to all DMUs
                     (default is [0, inf)

    Weight restrictions must be specified as a list. To specify only one bound
    leave the other as None, eg. in_weights=[1, None].

    """

    def __init__(self, inputs, outputs, returns='CRS',
                 in_weights=[0, None], out_weights=[0, None]):
        """
        Set up the DMUs' problems, ready to solve.

        """
        self.inputs = _to_dataframe(inputs)
        self.outputs = _to_dataframe(outputs)
        self.returns = returns

        self.J, self.I = self.inputs.shape  # no of firms, inputs
        _, self.R = self.outputs.shape  # no of outputs
        self._i = range(self.I)  # inputs
        self._r = range(self.R)  # outputs
        self._j = range(self.J)  # DMUs

        self._in_weights = in_weights  # input weight restrictions
        self._out_weights = out_weights  # output weight restrictions

        # creates dictionary of pulp.LpProblem objects for the DMUs
        self.dmus = self._create_problems()

    def _create_problems(self):
        """
        Iterate over the inputs and create a dictionary of LP problems, one
        for each DMU.

        """

        dmu_dict = {}
        for j0 in self._j:
            dmu_dict[j0] = self._make_problem(j0)
        return dmu_dict

    def _make_problem(self, j0):
        """
        Create a pulp.LpProblem for a DMU.

        """

        # Set up pulp
        prob = pulp.LpProblem("".join(["DMU_", str(j0)]), pulp.LpMaximize)
        self.inputWeights = pulp.LpVariable.dicts("inputWeight", (self._j, self._i),
                                                  lowBound=self._in_weights[0], upBound=self._in_weights[1])
        self.outputWeights = pulp.LpVariable.dicts("outputWeight", (self._j, self._r),
                                                   lowBound=self._out_weights[0], upBound=self._out_weights[1])

        # Set returns to scale
        if self.returns == "CRS":
            w = 0
        elif self.returns == "VRS":
            w = pulp.LpVariable.dicts("w", (self._j, self._r))
        else:
            raise Exception(ValueError)

        # Set up objective function
        prob += pulp.LpAffineExpression(
            [(self.outputWeights[j0][r1], self.outputs.values[j0][r1]) for r1 in self._r]) - w

        # Set up constraints
        prob += pulp.LpAffineExpression([(self.inputWeights[j0][i1],
                                          self.inputs.values[j0][i1]) for i1 in self._i]) == 1, "Norm_constraint"
        for j1 in self._j:
            prob += self._dmu_constraint(j0, j1) - \
                w <= 0, "".join(["DMU_constraint_", str(j1)])
        return prob

    def _dmu_constraint(self, j0, j1):
        """
        Calculate and return the DMU constraint for a single DMU's LP problem.

        """

        eOut = pulp.LpAffineExpression(
            [(self.outputWeights[j0][r1], self.outputs.values[j1][r1]) for r1 in self._r])
        eIn = pulp.LpAffineExpression(
            [(self.inputWeights[j0][i1], self.inputs.values[j1][i1]) for i1 in self._i])
        return eOut - eIn

    def _solver(self):
        """
        Iterate over the dictionary of DMUs' problems, solve them, and collate
        the results into a pandas dataframe.

        """

        sol_status = {}
        sol_weights = {}
        sol_efficiency = {}

        for ind, problem in list(self.dmus.items()):
            problem.solve()
            sol_status[ind] = pulp.LpStatus[problem.status]
            sol_weights[ind] = {}
            for v in problem.variables():
                sol_weights[ind][v.name] = v.varValue
            sol_efficiency[ind] = pulp.value(problem.objective)
        return sol_status, sol_efficiency, sol_weights

    def _build_weight_results_dict(self, sol_weights):
        """
        Rename weights from input and output column names, then build a
        pandas dataframe of all weights.

        """
        import re
        tmp_dict = {}
        for dmu, d in list(sol_weights.items()):
            tmp_dict[dmu] = {}
            for key, _ in list(d.items()):
                m = re.search(r'[0-9]+$',key)
                i = int(m.group(0))
                if key.startswith("input"):
                    tmp_dict[dmu]["in_" + str(self.inputs.columns[i])] = d[key]
                if key.startswith("output"):
                    tmp_dict[dmu][
                        "out_" + str(self.outputs.columns[i])] = d[key]
        weight_results = pd.DataFrame.from_dict(tmp_dict).T

        return weight_results

    def solve(self, sol_type='technical'):
        """"
        Solve the problem and create attributes to hold the solutions.

        Takes:
            sol_type: 'technical'/'allocative'/'economic'
            dmus: tuple defining range of DMUs to solve for.

        """

        if sol_type == 'technical':
            sol_status, sol_efficiency, sol_weights = self._solver()
            weight_results = self._build_weight_results_dict(sol_weights)
            status_df = pd.Series(sol_status, name='Status')
            status_df.index = self.inputs.index
            efficiency_df = pd.Series(sol_efficiency, name='Efficiency')
            efficiency_df.index = self.inputs.index

            return DEAResults((('Status', status_df),
                               ('Efficiency', efficiency_df),
                               ('Weights', weight_results)))
        else:
            print("Solution type not yet implemented.")
            print("Solving for technical efficiency instead.")
            self.solve()


class DEAResults(dict):

    """
    A class to hold the results of a DEAProblem and provide methods for
    their examination. Essentially a dictionary of pandas Series with
    methods for conducting particular operations on DEA results.

    """

#    def __init__(self):
#        super(DEAResults, self).__init__()
#        pass

    def find_comparators(self, dmu):
        """
        Return the DMUs that form the frontier for the specified DMU.

        """
        pass

    def env_corr(self, env_vars, qq_plot=False):
        """
        Determine correlations with environmental/non-discretionary variables
        using a logit regression. Tobit will be implemented when available
        upstream in statsmodels.

        Takes:
            env_vars: A pandas dataframe of environmental variables

        Returns:
            corr_mod: the statsmodels' model instance containing the inputs
                      and results from the logit model.

        Note that there can be no spaces in the variables' names.
        """

        import matplotlib.pyplot as plt
        from statsmodels.regression.linear_model import OLS
        from statsmodels.graphics.gofplots import qqplot

        env_data = _to_dataframe(env_vars)
        corr_data = env_data.join(self['Efficiency'])
        corr_mod = OLS.from_formula(
            "Efficiency ~ " + " + ".join(env_vars.columns), corr_data)
        corr_res = corr_mod.fit()

        #plot qq of residuals
        if qq_plot:
            qqplot(corr_res.resid, line='s')
            plt.title('Distribution of residuals')

        print(corr_res.summary())

        return corr_res


def _to_dataframe(indata):
    """
    Indexers require input to be a dataframe but the user may pass a
    series. Check and cast series to dataframes.

    """

    if type(indata) == pd.core.frame.DataFrame:
        return indata
    elif type(indata) == pd.core.series.Series:
        return pd.DataFrame(indata, columns=['input_data'])
    else:
        raise TypeError(
            "Input data is not a valid pandas DataFrame or Series.")
