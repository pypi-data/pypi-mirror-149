from script_utils import *


if __name__ == "__main__":
    ds = create_data_sheet_from_csv(get_file_path('singlesheet.csv'), delimiter=',')
    print(ds)
