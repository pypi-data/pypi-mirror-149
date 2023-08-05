from math import isclose
from scipy.io import loadmat
from .utils import function_details
from unittest import TestCase
from fmutest import simulate, me_step, euler_step#, optimization

rel_tol = 1e-5

def equal_with_tolerance(a, b, rel_tol):
    return all([isclose(a[i], b[i], rel_tol=rel_tol) for i in range(len(a))])


class Test(TestCase):
    
    def __init__(self, 
                 test_name='Single Step Simulation', 
                 fmu_path='resources\FMUs\test.fmu', 
                 input: dict ={'in1': 40,
                             'in2': 30, 
                             'in3': 0.5, 
                             'in4': 0.3}):

        super(Test, self).__init__(test_name)
        self.fmu = fmu_path
        self.input = input

    @function_details
    def test_me_step(self):
        result=me_step(fmu_path, input_dict, 'Euler', step_size=1)
        isclose(result[1], 2193.71875, rel_tol=rel_tol)
        equal_with_tolerance(result, (1, 2193.71875), rel_tol=rel_tol)

    @function_details
    def test_euler_step(self):
        result=euler_step(self.fmu, self.input, step_size=1)
        isclose(result[1], 2193.71875, rel_tol=rel_tol)
        equal_with_tolerance(result, (1, 2193.71875), rel_tol=rel_tol)


    @function_details    
    def test_euler_steps(self):
        result=euler_step(self.fmu, self.input, step_size=1)
        isclose(result[1], 2193.71875, rel_tol=rel_tol)
        equal_with_tolerance(result, (1, 2193.71875), rel_tol=rel_tol)