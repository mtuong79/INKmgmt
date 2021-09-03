# https://towardsdatascience.com/data-apps-with-pythons-streamlit-b14aaca7d083
# https://towardsdatascience.com/how-to-read-csv-file-using-pandas-ab1f5e7e7b58
# https://towardsdatascience.com/how-to-use-loc-and-iloc-for-selecting-data-in-pandas-bd09cb4c3d79
# https://towardsdatascience.com/how-to-change-column-type-in-pandas-dataframes-d2a5548888f8
# https://realpython.com/convert-python-string-to-int/
# https://towardsdatascience.com/data-visualization-using-streamlit-151f4c85c79a

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def explore(df):
    # DATA
    st.write('Data:')
    st.write(df)
    # SUMMARY
    df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
    numerical_cols = df_types[~df_types['Data Type'].isin(['object',
                                                           'bool'])].index.values

    df_types['Count'] = df.count()
    df_types['Unique Values'] = df.nunique()
    df_types['Min'] = df[numerical_cols].min()
    df_types['Max'] = df[numerical_cols].max()
    df_types['Average'] = df[numerical_cols].mean()
    df_types['Median'] = df[numerical_cols].median()
    df_types['St. Dev.'] = df[numerical_cols].std()
    st.write('Summary:')
    st.write(df_types)

def get_df(file):
    # get extension and read file
    extension = file.name.split('.')[1]
    if extension.upper() == 'CSV':
        df = pd.read_csv(file)
    elif extension.upper() == 'XLSX':
        df = pd.read_excel(file, engine='openpyxl')
    elif extension.upper() == 'PICKLE':
        df = pd.read_pickle(file)
    return df

def Xuat_Kho(df):
    file = "Data/InkMgmt.csv"
    st.write("Xuat Kho")
    #st.write(df)
    #st.dataframe(df.style.highlight_min(axis=0))
    df['Inventory'] = df['Inventory'].astype(int)
    df['Admin'] = df['Admin'].astype(int)
    df['Account'] = df['Account'].astype(int)
    df['CTU'] = df['CTU'].astype(int)
    df['EI'] = df['EI'].astype(int)
    df['Modelling'] = df['Modelling'].astype(int)
    df['PE'] = df['PE'].astype(int)
    df['Malaria'] = df['Malaria'].astype(int)
    df['CNS'] = df['CNS'].astype(int)
    df['Dengue'] = df['Dengue'].astype(int)
    df['Lab'] = df['Lab'].astype(int)
    df['MicroLab'] = df['MicroLab'].astype(int)
    df['VA-ward'] = df['VA-ward'].astype(int)

    with st.form("my_form"):
        department = st.selectbox("Department", ('Admin', 'Account', 'CTU', 'EI', 'Estate', 'Modelling', 'PE', 'Malaria', 'CNS', 'Dengue', 'Lab', 'Microlab', 'VA-ward'))
        inkcode = st.selectbox("Ink Code",df['InkCode'])
        x_quantity = st.number_input(f"Nhap so luong", value=0)

        submitted = st.form_submit_button("Submit")
        if submitted:
            inventory = df.loc[inkcode, 'Inventory']
            if inventory > 0:
                df.loc[inkcode, 'Inventory'] = inventory - x_quantity
                df.loc[inkcode, department] = df.loc[inkcode, department] + int(x_quantity)
            else:
                st.error("Het muc")

        st.write(df)

    df.to_csv(file, index=True)

def Nhap_Kho(df):
    file = "Data/InkMgmt.csv"
    #st.write("Nhap Kho")
    #st.dataframe(df[['Printer','InkCode','Inventory','IT-Warehouse']])
    df['Inventory'] = df['Inventory'].astype(int)

    with st.form("my_form"):
        inkcode = st.selectbox("Ink Code",df['InkCode'])
        n_quantity = st.number_input("Nhap so luong", value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            inventory = df.loc[inkcode, 'Inventory']
            df.loc[inkcode, 'Inventory'] = inventory + n_quantity

            st.write(f"Update Inventory: {inkcode} , SL: {df.loc[inkcode, 'Inventory']}")

        st.write(df[['Printer','InkCode','Inventory','IT-Warehouse']])

    df.to_csv(file, index=True)

def Thong_Ke(df):
    st.title("Report")
    tk = st.radio("",('Out of Stock', 'Usage by Department', 'Max of Ink Cartridge'))

    if tk == 'Out of Stock':
        st.bar_chart(df['Inventory'])
        st.subheader("INK Out of Stock")

        for inv in df['InkCode']:
            quantity = df.loc[inv, 'Inventory']
            if quantity == 0:
                st.write(f"Ink {inv} out of Stock")
    elif tk == 'Usage by Department':
        st.write("Usage by Department")
    else:
        st.write("Max of Ink Cartridge")

def main():
    st.title("INK MANAGEMENT")

    fileUpload = st.file_uploader("Upload file", type=['csv','xlsx','pickle'])

    file = "Data/InkMgmt.csv"
    # df = get_df(file)
    df = pd.read_csv(file,
                     index_col=['CodeIndex'])

    task = st.sidebar.radio('Task', ['Xuat Kho', 'Nhap Kho', 'Thong Ke'], 0)
    if task == 'Xuat Kho':
        Xuat_Kho(df)
    elif task == 'Nhap Kho':
       Nhap_Kho(df)
    else:
        Thong_Ke(df)

main()