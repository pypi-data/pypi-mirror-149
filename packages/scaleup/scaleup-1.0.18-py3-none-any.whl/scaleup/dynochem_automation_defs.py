"""COM Object creation Helpers"""
import win32com.client as w32c

#==================================================================================================

def create_model_automate_w32():
	"""Creates ModelAutomate object

	:return: ModelAutomate COM object for running scripts
	:rtype: COM Object
	"""
	automate = w32c.Dispatch("ModelAutomation.ModelAutomate")
	return automate

def create_script_parameters_w32():
	"""Creates Script parameters COM Object

	:return: Script parameters COM Object
	:rtype: COM Object
	"""
	parameters = w32c.Dispatch("ModelAutomation.ScriptParameters")
	return parameters
	
def create_script_step_w32(stepType : str):
	"""Create a script step object

	:param stepType: Creates a script step
	:type stepType: str
	:return: [description]
	:rtype: [type]
	"""
	step = w32c.Dispatch("ModelAutomation.ScriptStep")
	step.StepType = stepType
	return step
	
def create_simulation_parameters_w32():
	"""Create a simulation parameters object
	
	:return: COM Object with simulation specific parameters
	:rtype: COM Object
	"""
	stepParams = w32c.Dispatch("ModelAutomation.SimulationAutomationParameters")
	return stepParams
	
def create_verification_parameters_w32():
	"""Create a verification parameters object
	
	:return: COM Object with verification specific parameters
	:rtype: COM Object
	"""
	stepParams = w32c.Dispatch("ModelAutomation.VerificationAutomationParameters")
	return stepParams	
	
def create_fitting_parameters_w32():
	"""Create a fitting parameters object
	
	:return: COM Object with fitting specific parameters
	:rtype: COM Object
	"""
	stepParams = w32c.Dispatch("ModelAutomation.FittingAutomationParameters")
	return stepParams	

def create_optimization_parameters_w32():
	"""Create an optimization parameters object
	
	:return: COM Object with optimization specific parameters
	:rtype: COM Object
	"""
	stepParams = w32c.Dispatch("ModelAutomation.OptimizationAutomationParameters")
	return stepParams	
