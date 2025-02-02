# utils/data_transformer.py
import pandas as pd

def transform_options_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms options DataFrame by:
    1. Extracting 'Ticker' from 'contractSymbol' or 'currentSymbol'
    2. Dropping unnecessary columns like 'lastTradeDate'
    3. Returning the transformed DataFrame
    """
    df = df.copy()

    # Extract 'Ticker' from 'contractSymbol'
    if 'contractSymbol' in df.columns:
        df['Ticker'] = df['contractSymbol'].str.extract(r'^([A-Za-z]+)')
        df.drop(columns=['contractSymbol'], inplace=True)
    
    # Some yfinance versions use 'currentSymbol'
    if 'currentSymbol' in df.columns:
        df['Ticker'] = df['currentSymbol'].str.extract(r'^([A-Za-z]+)')
        df.drop(columns=['currentSymbol'], inplace=True)

    # Drop 'lastTradeDate' if it exists
    if 'lastTradeDate' in df.columns:
        df.drop(columns=['lastTradeDate'], inplace=True)
        df.drop(columns=['currency'],inplace=True)
        df.drop(columns=['contractSize'],inplace=True)
    
    return df

def reorder_and_round(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorders columns to make 'Ticker' the first column and rounds numeric columns to 2 decimals.
    """
    df = df.copy()

    # Make 'Ticker' the first column
    if 'Ticker' in df.columns:
        new_cols = ['Ticker'] + [col for col in df.columns if col != 'Ticker']
        df = df[new_cols]
    
    # Round numeric columns to 2 decimals
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns
    df[numeric_cols] = df[numeric_cols].round(2)
    
    return df
