from pyvis.network import Network
import pre_processing as pre
import pandas as pd
import re
df1 = pd.read_csv('datasets/df_1.csv')
df2 = pd.read_csv('datasets/df_2.csv')

def generate_network(df):
  # initializing the network graph 
  g = Network(height='900px', width='100%', bgcolor='black', font_color='white', notebook=True, cdn_resources='remote', filter_menu=True, select_menu=True, directed=True, neighborhood_highlight=True)

  # to show physics control of the layout
  # g.show_buttons(filter_=['physics'])

  # set physics layout of the network
  g.barnes_hut()


  sources = df['SOURCE_ACCT_NO']
  targets = df['TARGET_ACCT_NO']
  amount = df['TOTAL_AMOUNT']
  src_name = df['SOURCE_NAME']
  dst_name = df['TARGET_NAME']
  #color = t['T_IN_DEGREE_STD']
  txn_count = df['TXN_COUNT']
  src_degree = df['S_DEGREE']
  dst_degree = df['T_DEGREE']
  src_indegree = df['S_IN_DEGREE']
  dst_indegree = df['T_IN_DEGREE']


  edge_data = zip(sources, targets,amount,src_name,dst_name,txn_count,src_degree,dst_degree,src_indegree,dst_indegree) #color

  for e in edge_data:
      src = e[0]
      dst = e[1]
      amt = e[2]
      srcnm = e[3]
      dstnm = e[4]
      txnc = e[5]
      sd = e[6]
      td = e[7]
      sid = e[8]
      did = e[9]
      
      stitle = "{} - {}".format(src,srcnm)
      dtitle = "{} - {}".format(dst,dstnm)
      g.add_node(n_id=stitle, label=srcnm, title=str(stitle), physics=True, size = 8*sd,color='rgb(255,0,0)') #opacity=c #opacity=sid/10
      g.add_node(n_id=dtitle, label=dstnm, title=str(dtitle), physics=True,size = 8*td, color='rgb(255,0,0)') #opacity=c #opacity=did/10
      g.add_edge(stitle, dtitle, width=amt/100000, arrowStrikethrough=True, label=amt, color='rgb(163, 143, 243)', edge_id=str(src)+str(dst), physics=True)
      


  neighbor_map = g.get_adj_list()
  
  for node in g.nodes:
      #node['title'] = str(node['title']) + ' Neighbors: ' + ', '.join([str(neighbor) for neighbor in neighbor_map[node['id']]])
      
      node['title'] = [str(neighbor) for neighbor in neighbor_map[node["id"]]]
      node['title'] = ['NEIGHBOURS: ']
      for neighbor in neighbor_map[node["id"]]:
        node['title'].append(str(neighbor))
      node['title'] = '\n'.join(node['title'])
          

  
  for edge in g.edges:
      edge['title'] = pre.join_and_filter1(df1, df2, edge['edge_id'])

  # this step show the result of the title assignment of the edge attribute


  edges = g.get_edges()

  for i in range(len(edges)):
      
      tra = edges[i]['title']
      
      
      output_str= """\
      TRANSACTIONS:
      =============
      """

      for transaction in tra:
          output_str += f"TRAN_ID: {transaction['TRAN_ID']},\t"
          output_str += f"TRAN_DATE: {transaction['TRAN_DATE']},\t"
          output_str += f"TRAN_AMT: {transaction['TRAN_AMT']}\n" 
      
      
      edges[i]['title'] = output_str

    

  return (g)
    

a = generate_network(df1)

def gen(df):
        r = a.get_node(df)
        title = r['title']
        split_data = re.split(r'[:,]\s*', title)
        return split_data