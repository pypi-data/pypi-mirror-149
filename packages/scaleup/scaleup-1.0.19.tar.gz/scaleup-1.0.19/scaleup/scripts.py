import numpy as np
import pandas as pd


class ScriptResult:
    """ScriptResult contains either an ErrorMessage or a list of step results
    """

    def __init__(self, steps, script_result):
        
        if ((script_result.ErrorMessage is None) or (len(script_result.ErrorMessage) == 0)):
            self.ErrorMessage = ''
            self.steps = [self.__make_step_result(step.StepType, result) for (step, result)  in zip(steps, script_result.Results) ]
        else:
            self.ErrorMessage = script_result.ErrorMessage
            self.steps = []

    __builders = { 'SIMULATION' : (lambda res : SimulationStepResult(res)),
               'VERIFICATION' : (lambda res : VerificationStepResult(res)),
               'OPTIMIZATION' : (lambda res : OptimizationStepResult(res)),
               'FITTING' : (lambda res : FittingStepResult(res)),
    }

    def __make_step_result(self, step_type : str, step_result):
        return self.__builders[step_type](step_result)





class StepResult:
    """Base class for the StepResults
    """

    def __init__(self, type : str):
        self.type = type

    def __repr__(self): 
        return self.type 
    
    def __str__(self): 
        return self.type


class SimulationStepResult(StepResult):
    """Simulation Step Result. Contains a pandas dataframe of the endpoints and (optionally) the profiles report for each scenario.
    :param StepResult: COM Step Result to be converted to Python result
    :type StepResult: COM Object
    """

    def __init__(self, result):
        StepResult.__init__(self, "SIMULATION")
        self.profiles = []
        self.__add_endpoints(result)
        self.__add_profiles(result)

    def __add_endpoints(self, result):
        sheet = result.Entries[0].Values[0]
        headings = ['{} ({})'.format(sheet[1][0],sheet[2][0])] + \
                   ['{}.{} ({})'.format(sheet[0][r],sheet[1][r],sheet[2][r]) for r in range(1,len(sheet[0]))] 
        self.endpoints =  pd.DataFrame(sheet[3:], columns=headings).astype(float)       

    def __add_profiles(self, result):
        for profile in result.Entries[0].Values[1:]:
            self.profiles.append(SimulationProfile(profile))

    


def __make_report__(entry):
    def make_row(row):
        def make_value(value : str):
            try:
                return float(value)
            except:
                return value
        return [make_value(v) for v in row ]
    return [make_row(r) for r in entry]

class SimulationProfile:
    """Scenario profile report for Simulation Step Result
    """

    def __init__(self, entry):
        self.report = __make_report__(entry)
        self.scenario_name = entry[0][0]
        self.solver_steps = float(entry[1][1])
        self.total_time = float(entry[2][1])
        self.matrix_size = float(entry[3][1])
        self.plotted_points = float(entry[4][1])
        self.integration_method = entry[5][1]
        self.accuracy = float(entry[6][1])
        self.run_time = float(entry[7][1])
        
        sheet = entry[9:]
        headings = ['{} ({})'.format(sheet[1][0],sheet[2][0])] + \
                    ['{}.{} ({})'.format(sheet[0][r],sheet[1][r],sheet[2][r]) for r in range(1,len(sheet[0]))]   
        self.results =  pd.DataFrame(sheet[4:], columns=headings).astype(float)
        
        

    def __str__(self): 
        return "Simulation Profile:\n" + \
                "Scenario Name : {}\n".format(self.scenario_name) + \
                "Solver Steps : {}\n".format(self.solver_steps) + \
                "Total Time : {}\n".format(self.total_time) + \
                "Matrix Size : {}\n".format(self.matrix_size) + \
                "Plotted Points : {}\n".format(self.plotted_points) + \
                "Integration Method : {}\n".format(self.integration_method) + \
                "Accuracy : {}\n".format(self.accuracy) + \
                "Run Time : {}\n".format(self.run_time)

class VerificationStepResult(StepResult):
    
    def __init__(self, result):
        StepResult.__init__(self, "VERIFICATION")
        self.report = result.Entries[0].Values[0]


class FittingStepResult(StepResult):
    
    def __init__(self, result):
        StepResult.__init__(self, "FITTING")
        self.report = result.Entries[0].Values[0]


class OptimizationStepResult(StepResult):
    
    def __init__(self, result):
        StepResult.__init__(self, "OPTIMIZATION")
        self.report = result.Entries[0].Values[0]

