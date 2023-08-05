from fmutest.fmi import fmi2

def simulate(fmu_path, inputs):

    fmu = fmi2.FMU(fmu_path)
    output = fmu._get_(inputs)   
    return output 


def me_step(fmu_path, inputs, solver_name, step_size=1):

    fmu = fmi2.FMU(fmu_path)
    output = fmu._me_(inputs, solver_name, start_time=0, stop_time=step_size, step_size=step_size) 
    return output[-1]


def euler_step(fmu_path, inputs, step_size=1):

    fmu = fmi2.FMU(fmu_path)
    output = fmu._euler_(inputs, start_time=0, stop_time=step_size, step_size=step_size)
    return output[-1]