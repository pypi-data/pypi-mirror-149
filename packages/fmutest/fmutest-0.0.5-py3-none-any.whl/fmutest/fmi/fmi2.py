from fmpy import extract, read_model_description, instantiate_fmu, simulate_fmu
from fmpy.simulation import apply_start_values, settable_in_instantiated, settable_in_initialization_mode, simulateME, Input, ForwardEuler, Recorder
from fmpy.fmi2 import FMU2Model, fmi2False
from time import time as current_time
import numpy as np
import shutil

# absolute tolerance for equality when comparing two floats
eps = 1e-13;

# simulation tolerance
rel_tol = 1e-5

class FMU(FMU2Model):
    def __init__(self, fmu):
        uzd = extract(fmu)
        self.model_description = read_model_description(uzd)
        super(FMU, self).__init__(guid=self.model_description.guid, unzipDirectory=uzd, modelIdentifier=self.model_description.modelExchange.modelIdentifier, instanceName = 'ME1')
        self.instantiate()

    def _get_(self, start_values):
        start_values = apply_start_values(self, self.model_description, start_values)
        return simulate_fmu(self.unzipDirectory,
                            start_values=start_values,
                            model_description=self.model_description,
                            fmu_instance=self)

    def _me_(self, start_values, solver_name, start_time=0, stop_time=1, step_size=1):
        start_values = apply_start_values(self, self.model_description, start_values)
        return simulateME(model_description=self.model_description,
                          fmu=self,
                          start_time=start_time,
                          stop_time=stop_time,
                          solver_name='Euler',
                          step_size=step_size,
                          relative_tolerance=rel_tol,
                          start_values=start_values,
                          apply_default_start_values=False,
                          input_signals=None,
                          output=None,
                          output_interval=None,
                          record_events=True,
                          timeout=None,
                          step_finished=None, 
                          validate=True)

    def _euler_(self, start_values, start_time=0, stop_time=1, step_size=1):

        # check step size
        output_interval = step_size  
        if not np.isclose(round(output_interval / step_size) * step_size, output_interval):
            raise Exception("output_interval must be a multiple of step_size for fixed step solvers")

        # setup and initialization
        time = start_time
        self.setupExperiment(startTime=start_time, stopTime=stop_time)
        self.start_values = apply_start_values(self, self.model_description, start_values, settable=settable_in_instantiated)
        self.enterInitializationMode()
        self.start_values = apply_start_values(self, self.model_description, self.start_values, settable=settable_in_initialization_mode)     
        input = Input(self, self.model_description, None)
        input.apply(time)
        self.exitInitializationMode()  
        self.enterContinuousTimeMode() # (newDescreteStatesNeeded = False is assumed everywhere)

        # common solver constructor argument (fixed_step = True is assumed everywhere)
        solver_args = {
            'nx': self.model_description.numberOfContinuousStates,
            'nz': self.model_description.numberOfEventIndicators,
            'get_x': self.getContinuousStates,
            'set_x': self.setContinuousStates,
            'get_dx': self.getDerivatives,
            'get_z': self.getEventIndicators,
            'input': input
        }
        solver = ForwardEuler(**solver_args) # select the solver 

        # record the values for time == start_time
        recorder = Recorder(fmu=self,
                            modelDescription=self.model_description,
                            variableNames=None,
                            interval=output_interval)
        recorder.sample(time)  

        # simulation loop for fixed step simulation
        n_fixed_steps = 0
        while time < stop_time:
            t_next = start_time + n_fixed_steps * step_size            
            if t_next > stop_time:
                break
            n_fixed_steps += 1

            if t_next - time > eps:
                state_event, roots_found, time = solver.step(time, t_next) # do step
            else:
                state_event = False
                roots_found = []
                time = t_next

            self.setTime(time)            
            input.apply(time, discrete=False) # apply continuous inputs

            # check for step event, e.g. dynamics state selection
            step_event, _ = self.completedIntegratorStep()
            step_event = step_event != fmi2False
            if input.nextEvent(time) <= t_next or state_event or step_event:
                raise ArgumentError(f'Events have been detected. Please enable event handling!')

            # record current state
            if abs(time - round(time/output_interval)*output_interval) < eps and time > recorder.lastSampleTime + eps:
                recorder.sample(time, force=True)

        return recorder.result()

    def _terminate_(self):
        self.terminate()
        self.freeInstance()
        shutil.rmtree(self.unzipDirectory, ignore_errors=True)
        del solver