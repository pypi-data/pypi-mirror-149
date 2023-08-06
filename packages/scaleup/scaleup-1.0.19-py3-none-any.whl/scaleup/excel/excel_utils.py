import warnings
import pandas as pd
import itertools
import math

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

__exclusions = ["|", "nan"] #header content that should cause that column or row to be ignored for set-up

def get_sheet(workbook, sheet_name : str):
    """Gets the sheet from the workbook

    :param workbook: Excel Workbook
    :type workbook: ExcelFile
    :param sheet_name: Worksheet name
    :type workbook: str
    """
    all_names = [name.lower() for name in workbook.sheet_names]
    index = -1
    try:
        index = all_names.index(sheet_name.lower())
    except ValueError:
        return None
    
    ret = pd.read_excel(workbook, sheet_name=index, header=None)
    return ret

def read_sheet(file_path : str, sheet_name : str):
    """Reads the contents of a worksheet into memory.

    :param file_path: path of file
    :type file_path: str
    :param sheet_name: sheet name to be read (case-insensitive)
    :type sheet_name: str
    """
    workbook = pd.ExcelFile(file_path)
    worksheet = get_sheet(workbook, sheet_name)
    return worksheet

def get_scenario_names(df) -> list:
    """Reads the scenario names from the sheet

    :param df: pandas data frame representing the scenarios sheet
    :type df: DataFrame
    :return: list of the scenario names
    :rtype: list
    """
    names = [scen_name for scen_name in get_scenarios(df)[0].keys()]
    return names

def get_scenario_headers(df) -> list:
    """Gets the headers and indices for scenario headers skipping commented and blanks

    :param df: pandas data frame representing the scenarios sheet
    :type df: DataFrame
    :return: list containing tuples (col index, parameter name)
    :rtype: list
    """

    items_row = next((i[0], i[1]) for i in df[0].iteritems() if i[1] == "Items")[0]
    inter = [(r[0], r[1].tolist()) for r in itertools.islice(df.iteritems(),2,None) if not(any(x in str(r[1][1]) for x in __exclusions))]
    scens = [(col[0], '{}.{} ({})'.format(col[1][items_row], col[1][items_row+1], col[1][items_row+2])) for col in inter]
    return scens    

def get_scenarios(df) -> dict:
    """Gets the scenarios and headers from a scenario sheet exlcuding commented headers

    :param df: pandas data frame representing the scenarios sheet
    :type df: DataFrame
    :return: dictionary containing the scenarios keyed to scenario name, list of the scenario headers
    :rtype: dict, list
    """

    headers = get_scenario_headers(df)
    header_indices = [header[0] for header in headers]
    inter = [r[1].tolist() for r in itertools.islice(df.iterrows(),4,None) if not(any(x in str(r[1][0]) for x in __exclusions))] 
    scens = dict([(scen[0], scen[0:2] + [scen[h] for h in header_indices]) for scen in inter])
    
    return scens, headers

def __make_header__(dfheaders, col):
    ret =  '{}.{} ({})'.format(dfheaders[col][1], dfheaders[col][2], dfheaders[col][3]) if (isinstance(dfheaders[col][1],str)) else '{} ({})'.format(dfheaders[col][2], dfheaders[col][3])
    return ret

def get_datasheet(file_path : str, dataset_name : str):
    """Reads a datasheet

    :param file_path: file name of the model
    :type file_path: str
    :param dataset_name: dataset name for the datasheet. Either sheet_name or sheet_name.block_name
    :type dataset_name: str
    """

    pieces = dataset_name.split('.')

    sheet_name = pieces[0]
    block_name = '' if len(pieces) == 1 else pieces[1]

    dfdata = read_sheet(file_path, sheet_name)

    #find the size of the frame and get ready to locate the numbers
    rowsd, colsd=dfdata.shape[0], dfdata.shape[1]
    start_row=4
    end_row=-1
    inblock = False
    reached_next = False
    #start_row, end_row
    #find the blockname on the datasheet and the next blockname if any
    if block_name != '': #find top of the current block
        for irow in [row for row in dfdata.iterrows()][3:]:
            if block_name==str(irow[1][0]):
                start_row=irow[0]+1
                inblock = True
                continue
            if inblock:
                end_row=irow[0]
                if isinstance(irow[1][0], str):
                    reached_next = True
                    break
        #if not reached next then we need to add a row to end as we've hit the end of the data
        if (not reached_next):
            end_row += 1

    dfheaders=dfdata.iloc[:4,:] #assumes headers are in top rows - excel rows 2-4
    dfnumbers= dfdata.iloc[start_row:end_row,:] if end_row != -1 else dfdata.iloc[start_row:,:]
    headers = [__make_header__(dfheaders, col) for col in dfheaders]
    dfdata = pd.DataFrame(dfnumbers)
    dfdata.columns = headers
    if(math.isnan(dfdata[dfdata.columns[0]][dfdata.index.start])):
        dfdata.drop([dfdata.index.start], inplace=True)
    return dfdata

