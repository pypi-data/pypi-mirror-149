"""Various utilities for using with scripts"""

import os
import math
from enum import Enum
from csv import reader

__string_delim = '~'
__datasheet_delim = '~'
__opt_string_delim = '\t'
delim_escape = '&TLD;'


__writers = { 
	"SIMULATION" : (lambda writer, res, sep : __write_simulation_step_result__(writer, res, sep)),
	"FITTING" : (lambda writer, res, sep : __write_report_step_result__(writer, res, sep)),
	"VERIFICATION" : (lambda writer, res, sep : __write_report_step_result__(writer, res, sep)),
	"OPTIMIZATION" : (lambda writer, res, sep : __write_report_step_result__(writer, res, sep)),
	}

class OptTarget(Enum):
	"""Enumeration for Optimization Target"""
	Target  = 1,
	Min = 2,
	Max = 3


#=============================================================================================================
# recurrently used methods


def get_file_path(file_name : str, folder_name : str = None):
	"""Returns the path of a file relative to the current folder

	:param file_name: the name of the file
	:type file_name: str
	:param folder_name: sub-folder in which the file can be found, defaults to None
	:type folder_name: str, optional
	:return: Full path to the file
	:rtype: str
	"""

	folder = os.getcwd()
	eff_folder = '' if folder_name == None else folder_name
	ret = os.path.join(folder, eff_folder, file_name)
	return ret


#Creates the simulation scenario escaping any tildes in the scenario name
def escape_name(scenName : str):
	"""Escapes a name containing tilde (~) characters, replacing each ~ with &TLD;  
	This is	used when generating tilde delimited strings to safely send names which contains tildes.

	:param scenName: name to be escaped
	:type scenName: str
	:return: Escaped version of the input string
	:rtype: str
	"""
	ret = scenName.replace(__string_delim, delim_escape)
	return ret


def create_simulation_scenario(scen_name : str, ds_name : str, values = []):
	"""Creates a simulation scenario for use with Simulation and Verification steps.

	:param scen_name: scenario name
	:type scen_name: str
	:param ds_name: datasheet name
	:type ds_name: str
	:param values: parameter values for the scenario, defaults to []
	:type values: list, optional
	:return: String representation of the scenario for use with Simulation and Verification steps.
	:rtype: str
	"""
	scen = __string_delim.join([escape_name(scen_name), ds_name])
	scen = scen if len(values) == 0 else (scen + __string_delim + __string_delim.join(str(v) for v in values))
	return scen


# creates the option string
def create_script_option_string(show_progress : bool = True, alt_reader : bool = False):
	"""Generates the script option string

	:param show_progress: Show the Automation UI when running, defaults to True
	:type show_progress: bool, optional
	:param alt_reader: Use the alternate file reader for Excel models (i.e. not Excel Interop), defaults to False
	:type alt_reader: bool, optional
	:return: Formatted string of options
	:rtype: str
	"""
	ret = 'SHOWUI:{}~ALTREADER:{}'.format(('TRUE' if show_progress else 'FALSE'), ('TRUE' if alt_reader else 'FALSE'))
	return ret


# creates a fitting parameter
def create_fitting_parameter(parameter_name : str, unit : str, initial_value : float, max_value : float, min_value : float, fit_to_log : bool = False):
	"""Create a fitting parameter

	:param parameter_name: name of the parameter
	:type parameter_name: str
	:param unit: unit of measure for the parameter
	:type unit: str
	:param initial_value: inital value
	:type initial_value: float
	:param max_value: max value
	:type max_value: float
	:param min_value: min value
	:type min_value: float
	:param fit_to_log: Fit to the log of the value, defaults to False
	:type fit_to_log: bool, optional
	:return: Formatted parameter details for use with fitting step
	:rtype: str
	"""
	ret = __string_delim.join([parameter_name, unit, '' if math.isnan(initial_value) else str(initial_value), str(max_value), str(min_value), str(fit_to_log)])
	return ret


# creates an optimization factor
def create_optimization_factor(name : str, unit : str, initial_value : float , min = None, max = None):
	"""Create optimization Factor

	:param name: Factor name
	:type name: str
	:param unit: factor unit
	:type unit: str
	:param initial_value: initial value
	:type initial_value: float
	:param min: min value for factor. If not set, uses half of the initial value
	:type min: float, optional
	:param max: max value for factor. If not set, uses twice the initial value
	:type max: float, optional
	:return: Formatted factor for use in optimization step
	:rtype: str
	"""
	ret = __opt_string_delim.join([name, str(initial_value), unit, str(min if min != None else initial_value / 2.0 ), str(max if max != None else initial_value * 2.0)])
	return ret


# creates an optimization response
def create_min_optimization_response(name : str, weighting : float = 1.0):
	"""Creates a 'Minimize' target for a response

	:param name: name of the response to minimize
	:type name: str
	:param weighting: Weighting for this parameter, defaults to 1.0
	:type weighting: float, optional
	:return: Formatted response for use in the Optimization step
	:rtype: str
	"""
	return create_optimization_response(name, OptTarget.Min, 0, weighting)


def create_max_optimization_response(name : str, weighting : float = 1.0):
	"""Creates a 'Maximize' target for a response

	:param name: name of the response to maximize
	:type name: str
	:param weighting: Weighting for this parameter, defaults to 1.0
	:type weighting: float, optional
	:return: Formatted response for use in the Optimization step
	:rtype: str
	"""
	return create_optimization_response(name, OptTarget.Max, 0, weighting)

def create_target_optimization_response(name : str, value : float, weighting : float = 1.0):
	"""Creates a 'Target' target for a response 

	:param name: name of the response
	:type name: str
	:param value: Target value for the response
	:type value: float
	:param weighting: Weighting for this parameter, defaults to 1.0
	:type weighting: float, optional
	:return: Formatted response for use in the Optimization step
	:rtype: str
	"""
	return create_optimization_response(name , OptTarget.Target, value , weighting)

def create_optimization_response(name : str, target : OptTarget, value : float = 0.0, weighting : float = 1.0):
	"""Create a response for the optimization step

	:param name: name of the response
	:type name: str
	:param target: Type of response. Min|Max|Target
	:type target: OptTarget
	:param value: Target Value, defaults to 0.0
	:type value: float, optional
	:param weighting: Weighting for the parameter, defaults to 1.0
	:type weighting: float, optional
	:return: Formatted response for use in the Optimization step
	:rtype: str
	"""
	ret = __opt_string_delim.join([name, str(value), str(weighting), target.name])
	return ret			



# Checks the result to see if there is an error message. if there is, it displays it,
# if not, it displays the pages of results 

def write_result(result, writer = None, separator : str = ','):
	"""
	Write the contents of a script result.
	A script result contain have an error message or an array of step results.
	If it contains an error message, then this is written
	If it contains step results, each result (each of which may contain multiple pages) is written as
	lines of values separated by the passed in separator or a comma.

	If no 'writer' method is passed in, then we print to console.

	:param result: Script Result object from RunScript()
	:type result: COM Object
	:param writer: Method which takes in a string, if not set, 'print' is used.	
	:type writer: method
	:param separator: separator used for joining values in a row. Default is ','
	:type separator: str
	"""

	if writer == None:
		writer = print

	if(result.ErrorMessage != None and len(result.ErrorMessage) > 0):
		writer(result.ErrorMessage)
	else:
		stepNumber = 1
		for stepResult in result.Results:
			writer('Step : {}\n'.format(stepNumber))
			for values in stepResult.Entries[0].Values:
				output = ''
				for row in values:
					output += separator.join(["" if v == None else str(v) for v in row]) + '\n'
				writer(output + '==\n')



def write_result_to_file(result, file_name : str, append : bool = True, separator : str = ','):
	"""
	Write the contents of a script result.
	A script result contain have an error message or an array of step results.
	If it contains an error message, then this is written
	If it contains step results, each result (each of which may contain multiple pages) is written as
	lines of values separated by the passed in separator or a comma.

	:param result: Script Result object from RunScript()
	:type result: COM Object
	:param file_name: name of the file to which we will write
	:type file_name: str
	:param append: Append the output to the file (or overwrite). Default is True (append)
	:type append: bool
	:param separator: separator used for joining values in a row. Default is ','
	:type separator: str
	"""

	try:
		file_path = get_file_path(file_name)
		mode = "a" if append else "w"
		f=open(file_path, mode)
		write_result(result, f.write, separator)
	finally:
		f.flush()
		f.close()


def __write_simulation_profile(writer, profile, separator : str):
	writer('Scenario name\t{}'.format(profile.scenario_name))
	writer('Solver steps\t{}'.format(int(profile.solver_steps)))
	writer('Total time\t{}'.format(profile.total_time))
	writer('Matrix size\t{}'.format(int(profile.matrix_size)))
	writer('Plotted points\t{}'.format(int(profile.plotted_points)))
	writer('Integration Method\t{}'.format(profile.integration_method))
	writer('Accuracy\t{}'.format(profile.accuracy))
	writer('Run Time\t{}'.format(profile.run_time))
	writer('\n')
	writer(separator.join(profile.results.columns))
	for _,r in profile.results.iterrows():
		writer(separator.join([str(v) for v in r]))
	writer('\n')


def __write_simulation_step_result__(writer, step_result, separator : str):
	writer(separator.join(step_result.endpoints.columns))
	for _,r in step_result.endpoints.iterrows():
		writer(separator.join([str(v) for v in r]))
	writer('\n\n')
	for profile in step_result.profiles:
		__write_simulation_profile(writer, profile, separator)


def __write_report_step_result__(writer, step_result, separator : str = ','):
	for row in step_result.report:
		output = separator.join(["" if v == None else str(v) for v in row])
		writer(output + "\n")
	writer('==\n')		



def write_script_result(result, writer = None, separator : str = ","):
	"""
	Write the contents of a script result.
	A script result contain have an error message or a list of step results.
	If it contains an error message, then this is written
	If it contains step results, each result (each of which may contain multiple pages) is written.

	If no 'writer' method is passed in, then we print to console.

	:param result: ScriptResult object from RunScript()
	:type result: ScriptResult
	:param writer: Method which takes in a string, if not set, 'print' is used.	
	:type writer: method
	"""

	if writer == None:
		writer = print

	if(result.ErrorMessage != None and len(result.ErrorMessage) > 0):
		writer(result.ErrorMessage)
	else:
		step_number = 1
		for step_result in result.steps:
			writer('Step : {} ({})\n'.format(step_number, step_result.type))
			__writers[step_result.type](writer, step_result, separator)
			step_number += 1



def write_script_result_to_file(result, file_name : str, append : bool = True, separator : str = ","):
	"""
	Write the contents of a script result.
	A script result contain have an error message or an array of step results.
	If it contains an error message, then this is written
	If it contains step results, each result (each of which may contain multiple pages) is written 
	
	:param result: ScriptResult object from RunScript()
	:type result: ScriptResult
	:param file_name: name of the file to which we will write
	:type file_name: str
	:param append: Append the output to the file (or overwrite). Default is True (append)
	:type append: bool
	:param separator: separator used for joining values in a row. Default is ','
	:type separator: str
	"""

	try:
		file_path = get_file_path(file_name)
		mode = "a" if append else "w"
		f=open(file_path, mode)
		write_script_result(result, f.write, separator)
	finally:
		f.flush()
		f.close()



def get_run_type(file_name : str):
	"""	Ascertains the run type of a file based on the extension.
	Excel models "*.xls(?)" are 1.
	Reaction Lab Models "*.rxm" are 2
	All others return 0

	:param file_name: name of the file
	:type file_name: str
	:return: 0|1|2, depending on the file extension
	:rtype: int
	"""
	
	file_ext = os.path.splitext(file_name)[1]
	ret = 0
	if file_ext.lower().startswith('.xls'):
		ret = 1
	if file_ext.lower().startswith('.rxm'):
		ret = 2
	return ret

def create_data_sheet(datasheet_name : str, rows : list[list]):
	"""Generates a single data sheet from a list of lists

	:param datasheet_name: name of the data sheet - must replace one in the model
	:type datasheet_name: str
	:param rows: values
	:type rows: list[list]
	"""
	
	ret = [[datasheet_name]]
	
	ret.extend([__datasheet_delim.join([str(v) for v in r]) for r in rows])
	if(len(rows) > 0):
		count = len(rows[0])
		ret[0].extend(['' for _ in range(0, count-1)])
		ret[0] = __datasheet_delim.join(ret[0])
	return ret

def create_data_sheet_from_file(file_path : str, delimiter = '\t'):
	"""Generates a data sheets from a file. Default delimiter is tab but can be set.

	Can create one or many data sheets.

	Format:
	<Name1>
	<Values>*
	<Name2>
	<Values>*

	No blank lines in file - use line of delimiters instead of blank line

	:param file_path: name of path containing the data
	:type file_path: str
	"""
	with open(file_path, newline='') as f:
		values = reader(f, delimiter=delimiter)
		data = list(values)
	
	starts = [ index for index, line in enumerate(data) if len(line) == 1]
	starts.append(None)
	
	bounds = [(s, f if (f == None)  else f) for s,f in zip(starts, starts[1:])]
	ret = [create_data_sheet(data[s][0], data[s+1:f]) for s, f in bounds]

	return ret

