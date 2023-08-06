# Scaleup

Scale-up Suite Automation. This library provides a set of high level methods for scripting automation of Dynochem(R) and Reaction Lab(TM) models through the ```RunScript Automation``` interface. These methods wrap the COM calls to Scale-up Suite's ```ModelAutomation.exe``` allowing end users to write shorter and simpler scripts and focus on what they want to achieve rather than the mechanics of doing it.  

Contact your [Scale-up Systems](https://www.scale-up.com) representative to obtain access to the ```RunScript Automation``` product to which this library connects.

## Dependencies

* [pywin32](https://github.com/mhammond/pywin32)
* [pandas](https://pypi.org/project/pandas/)
* [openpyxl](https://pypi.org/project/openpyxl/)

## Installation

```python
pip install scaleup
```


# scaleup package

The `scaleup` package contains the routines for invoking automation, and helper routines to set up runs, along with classes representing the result of a script invocation along with results for the individual steps.


## scaleup.scripts

### scaleup.scripts.ScriptResult

This class contains the result for a script run.

* **Fields**

    * **error_message** (*str*) -- If an erorr occurred when running the script then this field with contain the error message. Otherwise None or empty.

    * **steps** (*list*) -- This contains a list of results for the steps executed. One step result per step.



### scaleup.scripts.SimulationStepResult

This contains the result of a Simulation step. It contains a *[pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)* which holds the results for each scenario along with (if requested) a list of `SimulationProfile` instances which holds the profiles for each scenario. 


* **Fields**

    * **type** (*str*) -- 'SIMULATION'
    * **endpoints** (*DataFrame*) -- DataFrame containing the results for the scenarios.
    * **profiles** (*list*) -- list of `SimulationProfile` instances, one per scenario (if requested).



### scaleup.scripts.SimulationProfile

Details of the scenario profile

* **Fields**

    * **scenario_name** (*str*)  -- the name of the scenario
    * **solver_steps** (*float*) --  number of steps
    * **total_time** (*float*) --  total time (seconds)
    * **matrix_size** (*float*) --  matrix size
    * **plotted_points** (*float*) -- plotted points
    * **integration_method** (*str*) -- integration method
    * **accuracy** (*float*) -- accuract
    * **run_time** (*float*) -- run time (seconds)
    * **results** (*DataFrame*) -- profile values for the scenario


### scaleup.scripts.FittingStepResult

Contains the result of a Fitting Simulation step.

* **Fields**

    * **type** (*str*) -- 'FITTING'
    * **report** (*list*) -- The Fitting report


### scaleup.scripts.OptimizationStepResult

Contains the result of a Optimization Simulation step.

* **Fields**

    * **type** (*str*) -- 'OPTIMIZATION'
    * **report** (*list*) -- The Optimization report


### scaleup.scripts.VerificationStepResult

Contains the result of a Verification Simulation step.

* **Fields**

    * **type** (*str*) -- 'VERIFICATION'
    * **report** (*list*) -- The Verification report


---


## scaleup.scaleup module

Short-cut routines for quick running of steps


### scaleup.scaleup.run_simulation(file_name: str, scenarios=[], return_profiles: bool = False, show_progress=True, alt_reader=True)
Runs a Simulation step


* **Parameters**

    
    * **file_name** (*str*) – name of the model file


    * **scenarios** (*list**, **optional*) – String representations of the scenarios to be run. If empty, runs all scenarios in the model, defaults to []


    * **return_profiles** (*bool**, **optional*) – Return the profiles as well as the endpoints, defaults to False


    * **show_progress** (*bool**, **optional*) – Show the progress indicator when running, defaults to True


    * **alt_reader** (*bool**, **optional*) – Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True



* **Returns**

    ScriptResult object


### scaleup.scaleup.run_fitting(file_name: str, scenarios, parameters, fit_to_each: bool = False, show_progress: bool = True, alt_reader: bool = True, update_to_source: bool = False)
Runs a Fitting step


* **Parameters**

    
    * **file_name** (*str*) – name of the model file


    * **scenarios** (*list*) – the names of the scenarios to be fitted


    * **parameters** (*list*) – string representations of the parameters to be fitted


    * **fit_to_each** (*bool**, **optional*) – Whether to fit to each scenario, defaults to False


    * **show_progress** (*bool**, **optional*) – Shoe the UI when running, defaults to True


    * **alt_reader** (*bool**, **optional*) – Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True


    * **update_to_source** (*bool**, **optional*) – Write back the fitted values to the original model, defaults to False



* **Returns**

    ScriptResult object



### scaleup.scaleup.run_optimization(file_name: str, scenario: str, factors, responses, show_progress: bool = True, alt_reader: bool = True, update_to_source: bool = False)
Runs an Optimization step


* **Parameters**

    
    * **file_name** (*str*) – name of the model file


    * **scenario** (*str*) – The name of the scenario to be optimized


    * **factors** (*list*) – string respresentations of the factors to be varied


    * **responses** (*list*) – string representations of the responses to optimize


    * **show_progress** (*bool**, **optional*) – Shoe the UI when running, defaults to True


    * **alt_reader** (*bool**, **optional*) – Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True


    * **update_to_source** (*bool**, **optional*) – Write back the fitted values to the original model, defaults to False



* **Returns**

    ScriptResult object



### scaleup.scaleup.run_verification(file_name: str, scenarios=[], verification_type: int = 1, show_progress=True, alt_reader=True)
Runs a Verification step


* **Parameters**

    
    * **file_name** (*str*) – name of the model file


    * **scenarios** (*list**, **optional*) – String representations of the scenarios to be run. If empty, runs all scenarios in the model, defaults to []


    * **verification_type** (*int**, **optional*) – Verification type. 1 for full report, 2 for residuals, 3 for SSQs, defaults to 1


    * **show_progress** (*bool**, **optional*) – Shoe the UI when running, defaults to True


    * **alt_reader** (*bool**, **optional*) – Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True



* **Returns**

    ScriptResult object




### scaleup.scaleup.run_multiple_steps(file_name: str, steps, show_progress: bool = True, alt_reader: bool = True, update_to_source: bool = False)
Run multiple steps in sequence


* **Parameters**

    
    * **file_name** (*str*) – name of the model file


    * **steps** (*list*) – the steps to run


    * **show_progress** (*bool**, **optional*) – Shoe the UI when running, defaults to True


    * **alt_reader** (*bool**, **optional*) – Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True


    * **update_to_source** (*bool**, **optional*) – Write back the fitted values to the original model, defaults to False



* **Returns**

    ScriptResult object


---


## scaleup.dynochem_automation module

Helper routines for COM automation of Dynochem Runtime scripting


### scaleup.dynochem_automation.create_fitting_step(scenarios, parameters, fitEachScenario: bool, updateToSource: bool = False)
Creates a Fitting step

* **Parameters**

    
    * **scenarios** (*list*) -- The scenarios to be fitted


    * **parameters** (*list*) -- The parameters to be fitted


    * **fitEachScenario** (*bool*) -- Fit to each scenario or not


    * **updateToSource** (*bool**, **optional*) -- Write the fitted values back to the model, defaults to False


* **Returns**

    Script step


* **Return type**

    COM Object



### scaleup.dynochem_automation.create_optimization_step(scenarioName: str, factors, responses, updateToSource: bool = False)
Creates an Optimization step


* **Parameters**

    
    * **scenarioName** (*str*) -- The name of the scenario to be used


    * **factors** (*list*) -- The factors to vary


    * **responses** (*list*) -- The Responses to be optimized


    * **updateToSource** (*bool**, **optional*) -- Whether the optimized scenario and data sheet are written back to the model, defaults to False



* **Returns**

    Script step



* **Return type**

    COM Object



### scaleup.dynochem_automation.create_script_parameters(name: str, file_name: str, options: str = '', dataSheets=None)
Creates a script parameters class


* **Parameters**

    
    * **name** (*str*) -- Name of the automation job


    * **file_name** (*str*) -- Name of the model file


    * **options** (*str**, **optional*) -- Options e.g. Show/Hide the UI, defaults to ''


    * **dataSheets** (*[**type**]**, **optional*) -- Custom Datasheets, defaults to None



* **Raises**

    **ValueError** -- If the model is not of a supported type (must be .xls? or .rxm)



* **Returns**

    COM object of script parameters



* **Return type**

    COM object



### scaleup.dynochem_automation.create_simulation_step(scenarios=[], writeProfiles: bool = False, returnProfiles: bool = False)
Creates a simulation step


* **Parameters**

    
    * **scenarios** (*list**, **optional*) -- The scenarios to be run, If empty, all are run, defaults to []


    * **writeProfiles** (*bool**, **optional*) -- Write the profiles to an file, defaults to False


    * **returnProfiles** (*bool**, **optional*) -- return the profiles as well as the endpoints, defaults to False



* **Returns**

    Script step



* **Return type**

    COM Object



### scaleup.dynochem_automation.create_verification_step(scenarios=[], verificationType: int = 1)
Creates a Verification step


* **Parameters**

    
    * **scenarios** (*list**, **optional*) -- The scenarios to be run. If empty, all scenarios are run, defaults to []


    * **verificationType** (*int**, **optional*) -- The Verification Type. 1 for full report, 2 for residuals, 3 for SSQs, defaults to 1



* **Returns**

    Script step



* **Return type**

    COM Object



### scaleup.dynochem_automation.run_script(file_name: str, script_name: str, steps, options: str = '', dataSheets=None)
Runs a script


* **Parameters**

    
    * **file_name** (*str*) -- The file name for the model


    * **script_name** (*str*) -- The name of the job - displayed in the UI if visible


    * **steps** (*list*) -- The steps to be executed


    * **options** (*str**, **optional*) -- Option string for run (Show/Hide UI, Use Excel interop or not for Excel Models), defaults to ''


    * **dataSheets** (*list**, **optional*) -- Replacement Datasheets to inject data into the model, defaults to None



* **Returns**

    Script Result



* **Return type**

    COM Object



### scaleup.dynochem_automation.set_datasheets(script, datasheets)
## scaleup.dynochem_automation_defs module

COM Object creation Helpers


### scaleup.dynochem_automation_defs.create_fitting_parameters_w32()
Create a fitting parameters object


* **Returns**

    COM Object with fitting specific parameters



* **Return type**

    COM Object



### scaleup.dynochem_automation_defs.create_model_automate_w32()
Creates ModelAutomate object


* **Returns**

    ModelAutomate COM object for running scripts



* **Return type**

    COM Object



### scaleup.dynochem_automation_defs.create_optimization_parameters_w32()
Create an optimization parameters object


* **Returns**

    COM Object with optimization specific parameters



* **Return type**

    COM Object



### scaleup.dynochem_automation_defs.create_script_parameters_w32()
Creates Script parameters COM Object


* **Returns**

    Script parameters COM Object



* **Return type**

    COM Object



### scaleup.dynochem_automation_defs.create_script_step_w32(stepType: str)
Create a script step object


* **Parameters**

    **stepType** (*str*) -- Creates a script step



* **Returns**

    [description]



* **Return type**

    [type]



### scaleup.dynochem_automation_defs.create_simulation_parameters_w32()
Create a simulation parameters object


* **Returns**

    COM Object with simulation specific parameters



* **Return type**

    COM Object



### scaleup.dynochem_automation_defs.create_verification_parameters_w32()
Create a verification parameters object


* **Returns**

    COM Object with verification specific parameters



* **Return type**

    COM Object


## scaleup.scaleup module


### scaleup.scaleup.run_fitting(file_name: str, scenarios, parameters, fitToEach: bool = False, showUi: bool = True, altReader: bool = True, updateToSource: bool = False)
Runs a Fitting step


* **Parameters**

    
    * **file_name** (*str*) -- name of the model file


    * **scenarios** (*list*) -- the names of the scenarios to be fitted


    * **parameters** (*list*) -- string representations of the parameters to be fitted


    * **fitToEach** (*bool**, **optional*) -- Whether to fit to each scenario, defaults to False


    * **showUi** (*bool**, **optional*) -- Shoe the UI when running, defaults to True


    * **altReader** (*bool**, **optional*) -- Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True


    * **updateToSource** (*bool**, **optional*) -- Write back the fitted values to the original model, defaults to False



* **Returns**

    Script Result object



* **Return type**

    COM object



### scaleup.scaleup.run_multiple_steps(file_name: str, steps, showUi: bool = True, altReader: bool = True, updateToSource: bool = False)
Run multiple steps in sequence


* **Parameters**

    
    * **file_name** (*str*) -- name of the model file


    * **steps** (*list*) -- the steps to run


    * **showUi** (*bool**, **optional*) -- Shoe the UI when running, defaults to True


    * **altReader** (*bool**, **optional*) -- Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True


    * **updateToSource** (*bool**, **optional*) -- Write back the fitted values to the original model, defaults to False



* **Returns**

    Script Result object



* **Return type**

    COM object



### scaleup.scaleup.run_optimization(file_name: str, scenario: str, factors, responses, showUi: bool = True, altReader: bool = True, updateToSource: bool = False)
Runs an Optimization step


* **Parameters**

    
    * **file_name** (*str*) -- name of the model file


    * **scenario** (*str*) -- The name of the scenario to be optimized


    * **factors** (*list*) -- string respresentations of the factors to be varied


    * **responses** (*list*) -- string representations of the responses to optimize


    * **showUi** (*bool**, **optional*) -- Shoe the UI when running, defaults to True


    * **altReader** (*bool**, **optional*) -- Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True


    * **updateToSource** (*bool**, **optional*) -- Write back the fitted values to the original model, defaults to False



* **Returns**

    Script Result object



* **Return type**

    COM object



### scaleup.scaleup.run_simulation(file_name: str, scenarios=[], showUi=True, altReader=True)
Runs a Simulation step


* **Parameters**

    
    * **file_name** (*str*) -- name of the model file


    * **scenarios** (*list**, **optional*) -- String representations of the scenarios to be run. If empty, runs all scenarios in the model, defaults to []


    * **showUi** (*bool**, **optional*) -- Shoe the UI when running, defaults to True


    * **altReader** (*bool**, **optional*) -- Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True



* **Returns**

    Script Result object



* **Return type**

    COM object



### scaleup.scaleup.run_verification(file_name: str, scenarios=[], verificationType: int = 1, showUi=True, altReader=True)
Runs a Verification step


* **Parameters**

    
    * **file_name** (*str*) -- name of the model file


    * **scenarios** (*list**, **optional*) -- String representations of the scenarios to be run. If empty, runs all scenarios in the model, defaults to []


    * **verificationType** (*int**, **optional*) -- Verification type. 1 for full report, 2 for residuals, 3 for SSQs, defaults to 1


    * **showUi** (*bool**, **optional*) -- Shoe the UI when running, defaults to True


    * **altReader** (*bool**, **optional*) -- Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True



* **Returns**

    Script Result object



* **Return type**

    COM object


## scaleup.script_utils module

Various utilities for using with scripts


### _class_ scaleup.script_utils.OptTarget(value)
Bases: `enum.Enum`

Enumeration for Optimization Target


#### Max(_ = _ )

#### Min(_ = (2,_ )

#### Target(_ = (1,_ )

### scaleup.script_utils.create_fitting_parameter(parameter_name: str, unit: str, initial_value: float, max_value: float, min_value: float, fit_to_log: bool = False)
Create a fitting parameter


* **Parameters**

    
    * **parameter_name** (*str*) -- name of the parameter


    * **unit** (*str*) -- unit of measure for the parameter


    * **initial_value** (*float*) -- inital value


    * **max_value** (*float*) -- max value


    * **min_value** (*float*) -- min value


    * **fit_to_log** (*bool**, **optional*) -- Fit to the log of the value, defaults to False



* **Returns**

    Formatted parameter details for use with fitting step



* **Return type**

    str



### scaleup.script_utils.create_max_optimization_response(name: str, weighting: float = 1.0)
Creates a 'Maximize' target for a response


* **Parameters**

    
    * **name** (*str*) -- name of the response to maximize


    * **weighting** (*float**, **optional*) -- Weighting for this parameter, defaults to 1.0



* **Returns**

    Formatted response for use in the Optimization step



* **Return type**

    str



### scaleup.script_utils.create_min_optimization_response(name: str, weighting: float = 1.0)
Creates a 'Minimize' target for a response


* **Parameters**

    
    * **name** (*str*) -- name of the response to minimize


    * **weighting** (*float**, **optional*) -- Weighting for this parameter, defaults to 1.0



* **Returns**

    Formatted response for use in the Optimization step



* **Return type**

    str



### scaleup.script_utils.create_optimization_factor(name: str, unit: str, initial_value: float, min=None, max=None)
Create optimization Factor


* **Parameters**

    
    * **name** (*str*) -- Factor name


    * **unit** (*str*) -- factor unit


    * **initial_value** (*float*) -- initial value


    * **min** (*float**, **optional*) -- min value for factor. If not set, uses half of the initial value


    * **max** (*float**, **optional*) -- max value for factor. If not set, uses twice the initial value



* **Returns**

    Formatted factor for use in optimization step



* **Return type**

    str



### scaleup.script_utils.create_optimization_response(name: str, target: scaleup.script_utils.OptTarget, value: float = 0.0, weighting: float = 1.0)
Create a response for the optimization step


* **Parameters**

    
    * **name** (*str*) -- name of the response


    * **target** (*OptTarget*) -- Type of response. Min|Max|Target


    * **value** (*float**, **optional*) -- Target Value, defaults to 0.0


    * **weighting** (*float**, **optional*) -- Weighting for the parameter, defaults to 1.0



* **Returns**

    Formatted response for use in the Optimization step



* **Return type**

    str



### scaleup.script_utils.create_script_option_string(showInUi: bool = True, altReader: bool = False)
Generates the script option string


* **Parameters**

    
    * **showInUi** (*bool**, **optional*) -- Show the Automation UI when running, defaults to True


    * **altReader** (*bool**, **optional*) -- Use the alternate file reader for Excel models (i.e. not Excel Interop), defaults to False



* **Returns**

    Formatted string of options



* **Return type**

    str



### scaleup.script_utils.create_simulation_scenario(scen_name: str, ds_name: str, values=[])
Creates a simulation scenario for use with Simulation and Verification steps.


* **Parameters**

    
    * **scen_name** (*str*) -- scenario name


    * **ds_name** (*str*) -- datasheet name


    * **values** (*list**, **optional*) -- parameter values for the scenario, defaults to []



* **Returns**

    String representation of the scenario for use with Simulation and Verification steps.



* **Return type**

    str



### scaleup.script_utils.create_target_optimization_response(name: str, value: float, weighting: float = 1.0)
Creates a 'Target' target for a response


* **Parameters**

    
    * **name** (*str*) -- name of the response


    * **value** (*float*) -- Target value for the response


    * **weighting** (*float**, **optional*) -- Weighting for this parameter, defaults to 1.0



* **Returns**

    Formatted response for use in the Optimization step



* **Return type**

    str



### scaleup.script_utils.escape_name(scenName: str)
Escapes a name containing tilde (~) characters, replacing each ~ with &TLD;  
This is used when generating tilde delimited strings to safely send names which contains tildes.


* **Parameters**

    **scenName** (*str*) -- name to be escaped



* **Returns**

    Escaped version of the input string



* **Return type**

    str



### scaleup.script_utils.get_file_path(file_name: str, folder_name: Optional[str] = None)
Returns the path of a file relative to the current folder


* **Parameters**

    
    * **file_name** (*str*) -- the name of the file


    * **folder_name** (*str**, **optional*) -- sub-folder in which the file can be found, defaults to None



* **Returns**

    Full path to the file



* **Return type**

    str



### scaleup.script_utils.get_run_type(file_name: str)
Ascertains the run type of a file based on the extension.
 - Excel models "*.xls(?)" are 1
 - Reaction Lab Models "*.rxm" are 2
 - All others return 0


* **Parameters**

    **file_name** (*str*) -- name of the file


* **Returns**

    0, 1, or 2, depending on the file extension


* **Return type**

    int


### scaleup.script_utils.write_result(result, writer=None, separator: str = ',')
Write the contents of a script result.
A script result contain have an error message or an array of step results.
If it contains an error message, then this is written
If it contains step results, each result (each of which may contain multiple pages) is written as
lines of values separated by the passed in separator or a comma.

If no 'writer' method is passed in, then we print to console.


* **Parameters**

    
    * **result** (*COM Object*) -- Script Result object from RunScript()


    * **writer** (*method*) -- Method which takes in a string, if not set, 'print' is used.



### scaleup.script_utils.write_result_to_file(result, file_name: str, append: bool = True)
Write the contents of a script result.
A script result contain have an error message or an array of step results.
If it contains an error message, then this is written
If it contains step results, each result (each of which may contain multiple pages) is written as
lines of values separated by the passed in separator or a comma.

If no 'writer' method is passed in, then we print to console.


* **Parameters**

    
    * **result** (*COM Object*) -- Script Result object from RunScript()


    * **writer** (*method*) -- Method which takes in a string, if not set, 'print' is used.


    * **append** (*bool*) -- Append the output to the file (or overwrite). Default is True (append)


## Module contents
