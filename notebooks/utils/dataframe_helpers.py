

import pandas as pd
import re
from datetime import datetime 
import unicodedata
import sys
import subprocess
from typing import Iterable, List, Any, Dict, Tuple

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'unidecode'])

from unidecode import unidecode


def df_general_preprocess(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Make general cleaning for a DataFrame including string format, \
    duplicate and None drop.
    Args:
        dataframe (pd.DataFrame): The DataFrame to be processed
    Returns:
        pd.DataFrame: The cleaned dataframe with the expected format
    """
    processed_df = dataframe.drop_duplicates()

    return _df_format_strings(processed_df)


def _df_format_strings(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Format all strings in a DataFrame, replacing empty strings with None \
    and transforming valid strings to uppercase.
    Args:
        dataframe (pd.dataframe.DataFrame): The DataFrame to be transformed
    Returns:
        pd.dataframe.DataFrame: The transformed DataFrame with formatted \
        strings.
    """
    
    dataframe = dataframe.dropna()
    remove_str = lambda x: unidecode(re.sub(r"[\"\t\n\'\[\];]", "", x)).str.strip() if isinstance(x, str) else x
    
    for field, dtype in zip(dataframe.columns, dataframe.dtypes):
        if field == "date":
            dataframe[field] = pd.to_datetime(dataframe[field])
        elif dtype=="object":
            dataframe[field] = remove_str(dataframe[field]).str.lower()
    return dataframe

def clean_column_name(column):
        special_chars = "!/\#$^&*(),:.'"
        column = strip_accents(column).replace(" ", "_")
        for special_char in special_chars:
            column = column.replace(special_char, "")
        return column

def strip_accents(
    string: str,
    accents: Tuple = (
        "COMBINING ACUTE ACCENT",
        "COMBINING GRAVE ACCENT",
        "COMBINING TILDE",
    ),
):
    """Strip accents for given string"""
    accents = set(map(unicodedata.lookup, accents))
    chars = [c for c in unicodedata.normalize("NFD", str(string)) if c not in accents]
    return unicodedata.normalize("NFC", "".join(chars))