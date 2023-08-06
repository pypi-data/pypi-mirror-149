def euler_step(fmu, inputs):
    fmu.setValues(inputs)
    fmu.initialize()
    fmu.setSolver()
    output = fmu.doStep()
    fmu.reset()
    return output[-1]