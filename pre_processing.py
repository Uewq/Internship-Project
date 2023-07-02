
import networkx as nx
import pandas as pd
import numpy
from pandasql import sqldf

def processing(df0, df1, df2):
    
    

    # Create a directed graph from the dataframe
    G = nx.from_pandas_edgelist(df1, source='SOURCE_ACCT_NO', target='TARGET_ACCT_NO', edge_attr=['TXN_COUNT'], create_using=nx.DiGraph())

    #G = nx.from_pandas_edgelist(df1, source='SOURCE_ACCT_NO', target='TARGET_ACCT_NO', edge_attr='TXN_COUNT', create_using=nx.DiGraph())

    
    # Degree number
    degreez = G.degree
    # Convert output to a list of dictionaries
    rows0 = [{'node': node, 'degree': degree} for node, degree in degreez]

    # Create dataframe from list of dictionaries
    degree = pd.DataFrame(rows0)

    # In Degree
    in_degreez = G.in_degree
    # Convert output to a list of dictionaries
    rows0 = [{'node': node, 'in_degree': in_degree} for node, in_degree in in_degreez]

    # Create dataframe from list of dictionaries
    in_degree = pd.DataFrame(rows0)

    # Out Degree
    out_degreez = G.out_degree
    # Convert output to a list of dictionaries
    rows1 = [{'node': node, 'out_degree': out_degree} for node, out_degree in out_degreez]
    #pd.reset_option('display.max_rows',None)
    # Create dataframe from list of dictionaries
    out_degree = pd.DataFrame(rows1)

    # Betweenes Centrality
    # Calculate betweenness centrality of each node
    betweenness = nx.betweenness_centrality(G)

    # Convert dictionary to Pandas series and reset the index
    betweenness_series = pd.Series(betweenness).reset_index()

    # Rename the columns of the dataframe
    betweenness_series.columns = ['node', 'betweenness_centrality']


    # Closeness Centrality
    closeness_centrality = nx.centrality.closeness_centrality(G)

    # Convert dictionary to Pandas series and reset the index
    closeness_series = pd.Series(closeness_centrality).reset_index()

    # Rename the columns of the dataframe
    closeness_series.columns = ['node', 'closeness_centrality']

    # Degree Centrality
    degree_centrality = nx.centrality.degree_centrality(G)

    # Convert dictionary to Pandas series and reset the index
    degree_centrality_series = pd.Series(degree_centrality).reset_index()

    # Rename the columns of the dataframe
    degree_centrality_series.columns = ['node', 'degree_centrality']

    # Page Rank
    # Calculate the PageRank centrality of nodes in the graph
    pr = nx.pagerank(G, alpha=0.85)

    # Convert dictionary to Pandas series and reset the index
    page_rank_series = pd.Series(pr).reset_index()

    # Rename the columns of the dataframe
    page_rank_series.columns = ['node', 'page_rank']
    
    
    ## Bank_Acct Dataset
    # PAGE RANK
    for index, row in page_rank_series.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'PAGE_RANK'] = row['page_rank']

    # DEGREE CENTRALITY    
    for index, row in degree_centrality_series.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'DEGREE_CENTRALITY'] = row['degree_centrality']

    # CLOSENESS CENTRALITY 
    for index, row in closeness_series.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'CLOSENESS_CENTRALITY'] = row['closeness_centrality']

    # BETWEENNESS CENTRALITY
    for index, row in betweenness_series.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'BETWEENNESS_CENTRALITY'] = row['betweenness_centrality']

    # DEGREE
    for index, row in degree.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'DEGREE'] = row['degree']    

    # OUT DEGREE
    for index, row in out_degree.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'OUT_DEGREE'] = row['out_degree']

    # IN DEGREE 
    for index, row in in_degree.iterrows():
        df0.loc[df0['ACCT_NO'] == row['node'], 'IN_DEGREE'] = row['in_degree']
        
    
    ## Summary Dataset
    # PAGE RANK
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_PAGE_RANK'] = row['PAGE_RANK']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_PAGE_RANK'] = row['PAGE_RANK']  

    # DEGREE CENTRALITY    
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_DEGREE_CENTRALITY'] = row['DEGREE_CENTRALITY']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_DEGREE_CENTRALITY'] = row['DEGREE_CENTRALITY']  

    # CLOSENESS CENTRALITY       
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_CLOSENESS_CENTRALITY'] = row['CLOSENESS_CENTRALITY']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_CLOSENESS_CENTRALITY'] = row['CLOSENESS_CENTRALITY']  

    # BETWEENNESS CENTRALITY
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_BETWEENNESS_CENTRALITY'] = row['BETWEENNESS_CENTRALITY']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_BETWEENNESS_CENTRALITY'] = row['BETWEENNESS_CENTRALITY']  


    # DEGREE
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_DEGREE'] = row['DEGREE']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_DEGREE'] = row['DEGREE']      


    # OUT DEGREE
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_OUT_DEGREE'] = row['OUT_DEGREE']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_OUT_DEGREE'] = row['OUT_DEGREE']  

    # IN DEGREE    
    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'S_IN_DEGREE'] = row['IN_DEGREE']
    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'T_IN_DEGREE'] = row['IN_DEGREE']  

    for index, row in df0.iterrows():
        df1.loc[df1['SOURCE_ACCT_NO'] == row['ACCT_NO'], 'SOURCE_NAME'] = row['NAME']


    for index, row in df0.iterrows():
        df1.loc[df1['TARGET_ACCT_NO'] == row['ACCT_NO'], 'TARGET_NAME'] = row['NAME']  

        df1['id'] = df1['SOURCE_ACCT_NO'].astype(str) + df1['TARGET_ACCT_NO'].astype(str)
    
    
    ## Details Dataset
    #df2['id'] = df2['SOURCE_ACCT_NO'].astype(str) + df2['TARGET_ACCT_NO'].astype(str)
    
    return df0, df1, df2

def join_and_filter3(id_val):
    df_1 = pd.read_csv('datasets/df_1.csv')
    df_2 = pd.read_csv('datasets/df_2.csv')
    q = f""" 
            SELECT df_2.SOURCE_NAME,df_2.TARGET_NAME, df_2.TRAN_ID, df_2.TRAN_DATE, df_2.TRAN_AMT
            FROM df_1
            LEFT JOIN df_2 ON df_1.id = df_2.id
            WHERE df_1.id = {id_val}
        """
    result = sqldf(q, locals())
    return result

def join_and_filter(source_name):
    source_name1 = source_name.upper() 
    df_1 = pd.read_csv('datasets/df_1.csv')
    df_2 = pd.read_csv('datasets/df_2.csv')
    q = f""" 
            SELECT df_2.SOURCE_NAME, df_2.TARGET_NAME, df_2.TRAN_ID, df_2.TRAN_DATE, df_2.TRAN_AMT
            FROM df_2
            WHERE df_2.SOURCE_NAME = '{source_name}'
        """
    result = sqldf(q, locals())
    return result


def join_and_filter1(dft, dft1, id_val):
    
    q = f""" 
            SELECT dft1.TRAN_ID, dft1.TRAN_DATE, dft1.TRAN_AMT
            FROM dft
            LEFT JOIN dft1 ON dft.id = dft1.id
            WHERE dft.id = {id_val}
        """
    result = sqldf(q, locals())
    return result.to_dict('records')


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



def filter_BANK_ACCT(df):
    q = '''
            SELECT DISTINCT SOURCE_ACCT_NO as ACCT_NO, SOURCE_NAME as NAME
            FROM df
            UNION
            SELECT DISTINCT TARGET_ACCT_NO as ACCT_NO, TARGET_NAME as NAME
            FROM df

        ''' 
    
    result = sqldf(q, locals())
    return result


def filter_TXN_SUMMARY(df):
    q = '''
            SELECT  SOURCE_ACCT_NO, TARGET_ACCT_NO, COUNT(TRAN_AMT) as TXN_COUNT, SUM(TRAN_AMT) as TOTAL_AMOUNT, id
            FROM df
            GROUP BY id, SOURCE_ACCT_NO, TARGET_ACCT_NO 
        ''' 
    
    result = sqldf(q, locals())
    return result