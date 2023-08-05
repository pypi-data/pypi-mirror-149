from fmpy import extract, read_model_description, instantiate_fmu, simulate_fmu
from fmpy.simulation import apply_start_values, settable_in_instantiated, settable_in_initialization_mode, simulateME, Input, ForwardEuler, Recorder
from fmpy.fmi2 import FMU2Model, fmi2False
from time import time as current_time
import numpy as np

# absolute tolerance for equality when comparing two floats
eps = 1e-13;

# simulation tolerance
rel_tol = 1e-5

class FMU_ME(FMU2Model):

    def __init__(self, fmu, step_size):

        uzd = extract(fmu)
        self.model_description = read_model_description(uzd)
        self.step_size = step_size
        super(FMU_ME, self).__init__(guid=self.model_description.guid, unzipDirectory=uzd, modelIdentifier=self.model_description.modelExchange.modelIdentifier, instanceName = 'ME1')

        self.instantiate()
        self.setupExperiment(startTime=0, stopTime=self.step_size)


    def setValues(self, inputs):

        self.instantiate()
        self.start_values = inputs
        self.start_values = apply_start_values(self, self.model_description, self.start_values, settable=settable_in_instantiated)

    def initialize(self, start_values=None):

        if not start_values:
            start_values = self.start_values
        self.enterInitializationMode()
        self.start_values = apply_start_values(self, self.model_description, start_values, settable=settable_in_initialization_mode)
        self.input = Input(self, self.model_description, None)
        self.input.apply(0)
        self.exitInitializationMode()  
        self.enterContinuousTimeMode() # (newDescreteStatesNeeded = False is assumed everywhere)

        self.recorder = Recorder(fmu=self,
                                 modelDescription=self.model_description,
                                 variableNames=None,
                                 interval=self.step_size)


    def setSolver(self):

        solver_args = {
            'nx': self.model_description.numberOfContinuousStates,
            'nz': self.model_description.numberOfEventIndicators,
            'get_x': self.getContinuousStates,
            'set_x': self.setContinuousStates,
            'get_dx': self.getDerivatives,
            'get_z': self.getEventIndicators,
            'input': self.input
        }
        self.solver = ForwardEuler(**solver_args) # select the solver

    def doStep(self):

        time = 0
        self.recorder.sample(time)  

        # simulation loop for fixed step simulation
        n_fixed_steps = 0
        while time < self.step_size:
            t_next = n_fixed_steps * self.step_size            
            if t_next > self.step_size:
                break
            n_fixed_steps += 1

            if t_next - time > eps:
                state_event, roots_found, time = self.solver.step(time, t_next) # do step
            else:
                state_event = False
                roots_found = []
                time = t_next

            self.setTime(time)            
            self.input.apply(time, discrete=False) # apply continuous inputs

            # check for step event, e.g. dynamics state selection
            step_event, _ = self.completedIntegratorStep()
            step_event = step_event != fmi2False
            if self.input.nextEvent(time) <= t_next or state_event or step_event:
                raise ArgumentError(f'Events have been detected. Please enable event handling!')

            # record current state
            if abs(time - round(time/self.step_size)*self.step_size) < eps and time > self.recorder.lastSampleTime + eps:
                self.recorder.sample(time, force=True)

        return self.recorder.result()
