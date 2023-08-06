from scaleup.scripts import *
from scaleup.script_utils import *
from scaleup.dynochem_automation import *


def run_simulation(file_name :str, scenarios = [], return_profiles : bool = False, show_progress = True, alt_reader = True):
    """Runs a Simulation step

    :param file_name: name of the model file
    :type file_name: str
    :param scenarios: String representations of the scenarios to be run. If empty, runs all scenarios in the model, defaults to []
    :type scenarios: list, optional
    :param return_profiles: Return the profiles as well as the endpoints, defaults to False
    :type return_profiles: bool, optional
    :param show_progress: Show the progress indicator when running, defaults to True
    :type show_progress: bool, optional
    :param alt_reader: Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True
    :type alt_reader: bool, optional
    :return: ScriptResult object
    :rtype: ScriptResult object
    """
    options = create_script_option_string(show_progress, alt_reader)
    step = create_simulation_step(scenarios, returnProfiles=return_profiles)
    result = run_script(file_name, "Simulation Automation", [step], options)

    ret = ScriptResult([step], result)

    return ret


def run_verification(file_name : str, scenarios = [], verification_type : int = 1, show_progress = True, alt_reader = True):
    """Runs a Verification step

    :param file_name: name of the model file
    :type file_name: str
    :param scenarios: String representations of the scenarios to be run. If empty, runs all scenarios in the model, defaults to []
    :type scenarios: list, optional
    :param verification_type: Verification type. 1 for full report, 2 for residuals, 3 for SSQs, defaults to 1
    :type verification_type: int, optional
    :param show_progress: Shoe the UI when running, defaults to True
    :type show_progress: bool, optional
    :param alt_reader: Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True
    :type alt_reader: bool, optional
    :return: ScriptResult object
    :rtype: ScriptResult object
    """
    options = create_script_option_string(show_progress, alt_reader)
    step = create_verification_step(scenarios, verification_type)
    result = run_script(file_name, "Verification Automation", [step], options)

    ret = ScriptResult([step], result)

    return ret

def run_fitting(file_name : str, scenarios, parameters, fit_to_each : bool = False, show_progress : bool = True, alt_reader : bool = True, update_to_source : bool = False):
    """Runs a Fitting step

    :param file_name: name of the model file
    :type file_name: str
    :param scenarios: the names of the scenarios to be fitted
    :type scenarios: list
    :param parameters: string representations of the parameters to be fitted
    :type parameters: list
    :param fit_to_each: Whether to fit to each scenario, defaults to False
    :type fit_to_each: bool, optional
    :param show_progress: Shoe the UI when running, defaults to True
    :type show_progress: bool, optional
    :param alt_reader: Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True
    :type alt_reader: bool, optional
    :param update_to_source: Write back the fitted values to the original model, defaults to False
    :type update_to_source: bool, optional
    :return: ScriptResult object
    :rtype: ScriptResult
    """

    run_type_excel = get_run_type(file_name) == 1
    if(run_type_excel and update_to_source):
        xl=w32c.Dispatch("Excel.Application")
        xl.Visible = True #Update to Source requires this
        wb=xl.Workbooks.Open(file_name)
        xl.WindowState = 2

    try:

        options = create_script_option_string(show_progress, alt_reader)
        step = create_fitting_step(scenarios, parameters, fit_to_each, update_to_source)
        result = run_script(file_name, "Fitting Automation", [step], options)

        ret = ScriptResult([step], result)

    finally:
        if(run_type_excel and update_to_source):
            wb.Close(True)
            xl.Quit()

    return ret

def run_optimization(file_name : str, scenario : str, factors, responses, show_progress : bool = True, alt_reader : bool = True, update_to_source : bool = False):
    """Runs an Optimization step

    :param file_name: name of the model file
    :type file_name: str
    :param scenario: The name of the scenario to be optimized
    :type scenario: str
    :param factors: string respresentations of the factors to be varied
    :type factors: list
    :param responses: string representations of the responses to optimize
    :type responses: list
    :param show_progress: Shoe the UI when running, defaults to True
    :type show_progress: bool, optional
    :param alt_reader: Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True
    :type alt_reader: bool, optional
    :param update_to_source: Write back the fitted values to the original model, defaults to False
    :type update_to_source: bool, optional
    :return: ScriptResult object
    :rtype: ScriptResult
    """
    run_type_excel = get_run_type(file_name) == 1
    if(run_type_excel and update_to_source):
        xl=w32c.Dispatch("Excel.Application")
        xl.Visible = True #Update to Source requires this
        wb=xl.Workbooks.Open(file_name)
        xl.WindowState = 2

    try:
        options = create_script_option_string(show_progress, alt_reader)
        step = create_optimization_step(scenario, factors, responses, update_to_source)
        result = run_script(file_name, "Optimization Automation", [step], options)

        ret = ScriptResult([step], result)

    finally:
        if(run_type_excel and update_to_source):
            wb.Close(True)
            xl.Quit()

    return ret

def run_multiple_steps(file_name : str, steps, show_progress : bool = True, alt_reader : bool = True, update_to_source : bool = False):
    """Run multiple steps in sequence

    :param file_name: name of the model file
    :type file_name: str
    :param steps: the steps to run
    :type steps: list
    :param show_progress: Shoe the UI when running, defaults to True
    :type show_progress: bool, optional
    :param alt_reader: Use the alternate reader for Excel Models (i.e. not Excel Interop), defaults to True
    :type alt_reader: bool, optional
    :param update_to_source: Write back the fitted values to the original model, defaults to False
    :type update_to_source: bool, optional
    :return: ScriptResult object
    :rtype: ScriptResult
    """
    run_type_excel = get_run_type(file_name) == 1
    if(run_type_excel and update_to_source):
        xl=w32c.Dispatch("Excel.Application")
        xl.Visible = True #Update to Source requires this
        wb=xl.Workbooks.Open(file_name)
        xl.WindowState = 2

    try:
        options = create_script_option_string(show_progress, alt_reader)
        result = run_script(file_name, "Multi-step Automation", steps, options)

        ret = ScriptResult(steps, result)
        
    finally:
        if(run_type_excel and update_to_source):
            wb.Close(True)
            xl.Quit()

    return ret
