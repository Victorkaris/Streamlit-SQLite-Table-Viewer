import streamlit as st
import pandas as pd
import sqlite3

st.title('SQLite Table Viewer')

st.write('This app allows you to view and filter data from an SQLite database.')

uploaded_file = st.file_uploader("Upload a SQLite .db file", type=["db"])

if uploaded_file is not None:
    with open("temp.db", 'wb') as file:
        file.write(uploaded_file.getbuffer())

        connection = sqlite3.connect("temp.db")
        cursor = connection.cursor()

        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        connection.close()

        if tables:
            selected_table = st.selectbox("Select a table", table_names)

            if selected_table:
                connection = sqlite3.connect("temp.db")
                df = pd.read_sql_query(f"SELECT * FROM {selected_table}", connection)
                connection.close()
                st.dataframe(df)

            else:
                st.warning("No tables found in the database.")
