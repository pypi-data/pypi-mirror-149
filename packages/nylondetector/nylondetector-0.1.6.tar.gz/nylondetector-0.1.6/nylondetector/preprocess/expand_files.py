import pandas as pd

def expand_files(path, delimiter='||'):
    raw_file = pd.read_table(path, error_bad_lines=False)

    column = raw_file.columns[0]
    columns_list = column.split(delimiter)

    result = pd.DataFrame(list(raw_file[column].map(lambda x: x.split(delimiter))))
    result.columns = columns_list

    result.to_csv(f"{path.split('.csv')[0]}_expanded.csv", encoding='utf-8-sig')