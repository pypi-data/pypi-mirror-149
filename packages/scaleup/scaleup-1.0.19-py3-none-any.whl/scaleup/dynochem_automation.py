"""Helper routines for COM automation of Dynochem Runtime scripting"""


import pythoncom 
from win32com.client import VARIANT

from scaleup.dynochem_automation_defs import *
from scaleup.script_utils import *

# Creates a script parameters class, adding the standard params
#   targetType of 1 is Excel 
#   targetType of 2 is Reaction Lab

def create_script_parameters(name : str , file_name : str, options : str = '', dataSheets = None):
	"""Creates a script parameters class

	:param name: Name of the automation job
	:type name: str
	:param file_name: Name of the model file
	:type file_name: str
	:param options: Options e.g. Show/Hide the UI, defaults to ''
	:type options: str, optional
	:param dataSheets: Custom Datasheets, defaults to None
	:type dataSheets: [type], optional
	:raises ValueError: If the model is not of a supported type (must be .xls? or .rxm)
	:return: COM object of script parameters
	:rtype: COM object
	"""

	target_type = get_run_type(file_name)

	if target_type == 0:
		raise ValueError('{} is not of a supported model type'.format(file_name))

	parameters = create_script_parameters_w32()
	parameters.Name = name
	parameters.TargetType = target_type
	parameters.ModelDetails = file_name
	parameters.Options = options
	if(dataSheets != None):
		set_datasheets(parameters, dataSheets)
	return parameters


def create_simulation_step(scenarios = [], writeProfiles : bool = False, returnProfiles : bool = False) -> pythoncom.VT_DISPATCH:
	"""Creates a simulation step

	:param scenarios: The scenarios to be run, If empty, all are run, defaults to []
	:type scenarios: list, optional
	:param writeProfiles: Write the profiles to an file, defaults to False
	:type writeProfiles: bool, optional
	:param returnProfiles: return the profiles as well as the endpoints, defaults to False
	:type returnProfiles: bool, optional
	:return: Script step
	:rtype: COM Object
	"""
	step = create_script_step_w32("SIMULATION")
	stepParameters = create_simulation_parameters_w32()
	
	stepParameters.Scenarios = scenarios
	
	stepParameters.RunType = 1 if len(scenarios) == 0 else 3
	stepParameters.writeProfiles = writeProfiles
	stepParameters.ReturnProfiles = returnProfiles
	step.StepParameters = stepParameters
	return step

def create_fitting_step(scenarios, parameters , fitEachScenario : bool, updateToSource : bool = False ) -> pythoncom.VT_DISPATCH:
	"""Creates a Fitting step

	:param scenarios: The scenarios to be fitted
	:type scenarios: list
	:param parameters: The parameters to be fitted
	:type parameters: list
	:param fitEachScenario: Fit to each scenario or not
	:type fitEachScenario: bool
	:param updateToSource: Write the fitted values back to the model, defaults to False
	:type updateToSource: bool, optional
	:return: Script step
	:rtype: COM Object
	"""
	step = create_script_step_w32("FITTING")
	stepParameters = create_fitting_parameters_w32()
	
	stepParameters.Scenarios = scenarios
	stepParameters.Parameters = parameters
	stepParameters.FitEachScenario = fitEachScenario
	stepParameters.UpdateToSource = updateToSource
	stepParameters.DeselectThreshold = -1
	
	step.StepParameters = stepParameters
	return step
	
	
def create_verification_step(scenarios = [], verificationType : int = 1 ) -> pythoncom.VT_DISPATCH:
	"""Creates a Verification step

	:param scenarios: The scenarios to be run. If empty, all scenarios are run, defaults to []
	:type scenarios: list, optional
	:param verificationType: The Verification Type. 1 for full report, 2 for residuals, 3 for SSQs, defaults to 1
	:type verificationType: int, optional
	:return: Script step
	:rtype: COM Object
	"""
	step = create_script_step_w32("VERIFICATION")
	stepParameters = create_verification_parameters_w32()
	stepParameters.Scenarios = scenarios
	stepParameters.RunType = 1 if len(scenarios) == 0 else 3
	stepParameters.VerificationType = verificationType
	
	step.StepParameters = stepParameters
	return step
	
	
def create_optimization_step(scenarioName : str, factors, responses, updateToSource : bool = False) -> pythoncom.VT_DISPATCH:
	"""Creates an Optimization step

	:param scenarioName: The name of the scenario to be used
	:type scenarioName: str
	:param factors: The factors to vary
	:type factors: list
	:param responses: The Responses to be optimized
	:type responses: list
	:param updateToSource: Whether the optimized scenario and data sheet are written back to the model, defaults to False
	:type updateToSource: bool, optional
	:return: Script step
	:rtype: COM Object
	"""
	step = create_script_step_w32("OPTIMIZATION")
	stepParameters = create_optimization_parameters_w32()
	stepParameters.ScenarioName = scenarioName
	stepParameters.Factors = factors
	stepParameters.Responses = responses
	stepParameters.UpdateToSource = updateToSource
	
	step.StepParameters = stepParameters
	return step	

def set_datasheets(script, datasheets):
	datasheets_variant = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, datasheets)
	script.DataSheets = datasheets_variant

#=================================================================================================
# ScriptType generated from filename
	
def run_script(file_name : str, script_name : str, steps, options : str = '', dataSheets = None) -> pythoncom.VT_DISPATCH:
	"""Runs a script

	:param file_name: The file name for the model
	:type file_name: str
	:param script_name: The name of the job - displayed in the UI if visible
	:type script_name: str
	:param steps: The steps to be executed
	:type steps: list
	:param options: Option string for run (Show/Hide UI, Use Excel interop or not for Excel Models), defaults to ''
	:type options: str, optional
	:param dataSheets: Replacement Datasheets to inject data into the model, defaults to None
	:type dataSheets: list, optional
	:return: Script Result
	:rtype: COM Object
	"""

	parameters = create_script_parameters(script_name, file_name, options, dataSheets)
	parameters.Steps = steps

	runner = create_model_automate_w32()
	result = runner.RunScript(file_name,
								parameters)

	return result

