import pandas as pd
import re


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """A helper function to standardize column names.

    :param df: A Pandas DataFrame.
    :return: A DataFrame with lowercase column names and spaces as underscore separators.
    """
    df.columns = [re.sub(r'[^\w\s]', ' ', i) for i in df.columns]
    cols = list(map(str.split, df.columns))
    cols = [' '.join(i) for i in cols]
    df.columns = cols
    df.columns = map(str.strip, df.columns)

    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('-', '_')
    return df
