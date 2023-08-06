"""source: https://gist.github.com/enamoria/fa9baa906f23d1636c002e7186516a7b
"""
import pandas as pd


def memory_usage(df: pd.DataFrame) -> str:
    """A helper function that evaluates memory in a DataFrame.

    :param df: A Pandas DataFrame
    :return: An f-string that indicates DataFrame memory usage in MB.
    """
    mem = df.memory_usage().sum() / 1024 ** 2

    return '{:.2f} MB'.format(mem)
