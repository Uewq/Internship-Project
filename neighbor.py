import pandas as pd
from pandasql import sqldf

df1 = pd.read_csv('datasets/df_1.csv')

def join_and_filter2(source_name):
    source_name1 = source_name.upper() 
    
    df_2 = pd.read_csv('datasets/df_2.csv')
    q = f"""
            SELECT DISTINCT df_2.SOURCE_ACCT_NO AS 'Source Account', df_2.TARGET_NAME AS Neighbours, df_2.TARGET_ACCT_NO AS 'Account Number'
            FROM df_2
            WHERE df_2.SOURCE_NAME = '{source_name}'
        """
    result = sqldf(q, locals())
    return result