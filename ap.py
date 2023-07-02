import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pre_processing as pre
import gen_network as gn
import neighbor as ne


st.set_page_config(layout="wide")

st.title("Network Graph Visualization")



with st.container():
    # File upload widget
    uploaded_file = st.file_uploader("Upload the Transaction Details File")
    # Button to trigger the visualization
    if st.button("Upload and Preprocess"):
        if uploaded_file is not None:

            # Load the data into a Pandas DataFrame

            dt2 = pd.read_csv(uploaded_file)
            dt2['id'] = dt2['SOURCE_ACCT_NO'].astype(str) + dt2['TARGET_ACCT_NO'].astype(str)

            dt0 = pre.filter_BANK_ACCT(dt2)

            dt1 = pre.filter_TXN_SUMMARY(dt2)
        



            df_0, df_1, df_2 = pre.processing(dt0, dt1, dt2)

            # Define the file paths
            
            file_path_1 = 'datasets/df_1.csv'
            file_path_2 = 'datasets/df_2.csv'
            file_path_3 = 'datasets/df_0.csv'

            # Save the dataframes as CSV files
            
            df_1.to_csv(file_path_1, index=False)
            df_2.to_csv(file_path_2, index=False)
            df_0.to_csv(file_path_3, index=False)



with st.container():
    if st.button("Visualize"):
        df1 = pd.read_csv('datasets/df_1.csv')
        # Create a Pyvis visualization
        network = gn.generate_network(df1)
        network.save_graph('pyvis_graph.html')
        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=930, width=1200)



with st.container():
    st.header("Node and Edge Values")
    col1, col2 = st.columns(2)
    with col1:
        edge_id = st.text_input('Enter edge id', value='AJAY NARAYAN')
        result = pre.join_and_filter(edge_id)
        st.write(result)

    with col2:
        # Use a default value for the node_id
        node_id = st.text_input('Enter node id', value="ARUN")

        # Check if the node_id is not empty
        if node_id.strip():
            # Call the get_neighbor function with the node_id
            nodes_df = ne.join_and_filter2(node_id)
            st.dataframe(nodes_df)

        else:
            st.write("Enter Node id")

with st.container():
    st.header("Transactions")
    edge_id = st.text_input('Enter edge id', value='45230')
    result = pre.join_and_filter3(int(edge_id))
    st.write(result)