from posixpath import basename
import string
import inflect
import re
import pandas as pd
import os


def camel_to_snake(col_name):
    col_name = col_name.translate(str.maketrans('', '', string.punctuation))
    col_name = col_name.replace('-', '_')
    col_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', col_name)
    col_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', col_name).lower().replace(' ', '')
    return col_name


def read_original_file(input_file_path):
    if input_file_path.suffix == '.csv':
        df = pd.read_csv(input_file_path)
    elif input_file_path.suffix == '.xls' or input_file_path.suffix == '.xlsx':
        df = pd.read_excel(input_file_path)
    else:
        return
    return df


def preprocess_headers(df, reserved_words):
    p = inflect.engine()
    columns = list(df.columns.values)
    for col_idx, col in enumerate(columns):
        col = camel_to_snake(col_name=col)
        for c in col:
            if c.isdigit():
                col = col.replace(c, '_' + p.number_to_words(int(c)))
        if col.upper() in reserved_words:
            col = col + 'value'
        columns[col_idx] = col
    df.set_axis(columns, axis=1, inplace=True)
    return df


def save_csv(df, output_path, df_name):
    df_name = "clean.csv"
    df.to_csv(os.path.join(output_path, df_name), index=False)
    return df_name
