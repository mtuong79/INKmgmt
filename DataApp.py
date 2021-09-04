# @M.Tuong - OUCRU

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
    st.subheader("STOCK EXPORT")
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
    df['Zoonoses'] = df['Zoonoses'].astype(int)
    df['VA-ward'] = df['VA-ward'].astype(int)
    df['InkTotal'] = df['InkTotal'].astype(int)

    with st.form("my_form"):
        department = st.selectbox("Department", ('Admin', 'Account', 'CTU', 'EI', 'Estate', 'Modelling', 'PE', 'Malaria', 'CNS', 'Dengue', 'Lab', 'Microlab', 'Zoonoses', 'VA-ward'))
        inkcode = st.selectbox("Ink Code",df['InkCode'])
        x_quantity = st.number_input(f"Exporting Quantity", value=0)

        submitted = st.form_submit_button("Submit")
        if submitted:
            inventory = df.loc[inkcode, 'Inventory']
            if inventory > 0:
                df.loc[inkcode, 'Inventory'] = inventory - x_quantity
                df.loc[inkcode, department] = df.loc[inkcode, department] + int(x_quantity)
                #st.write(f"Xuat kho {x_quantity} {inkcode} cho phong {department}")
                st.success(f"Successfully Exported:  {x_quantity} {inkcode} for {department}")
            else:
                st.error("Het muc")

        st.write(df)

    df.to_csv(file, index=True)

def Nhap_Kho(df):
    file = "Data/InkMgmt.csv"
    st.subheader("STOCK IMPORT")
    #st.dataframe(df[['Printer','InkCode','Inventory','IT-Warehouse']])
    df['Inventory'] = df['Inventory'].astype(int)

    with st.form("my_form"):
        inkcode = st.selectbox("Ink Code",df['InkCode'])
        n_quantity = st.number_input("Importing Quantity", value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            inventory = df.loc[inkcode, 'Inventory']
            total = df.loc[inkcode, 'InkTotal']
            df.loc[inkcode, 'Inventory'] = inventory + n_quantity
            df.loc[inkcode, 'InkTotal'] = total + n_quantity

            #st.write(f"Successfully Updated Inventory: {inkcode} , Totlal: {df.loc[inkcode, 'Inventory']}")
            st.success(f"Successfully Imported: {inkcode} , Total: {df.loc[inkcode, 'Inventory']}")

        st.write(df[['Printer','InkCode','Inventory','IT-Warehouse']])

    df.to_csv(file, index=True)

def Thong_Ke(df):
    st.subheader("STOCK REPORT")
    tk = st.radio("",('Inventory Summary', 'Usage by Department', 'Total of Ink Cartridges'))

    if tk == 'Inventory Summary':
        st.bar_chart(df['Inventory'])
        st.subheader("Out of Stock")

        for inv in df['InkCode']:
            quantity = df.loc[inv, 'Inventory']
            if quantity == 0:
                st.write(f"{inv}: out of stock")

    elif tk == 'Usage by Department':
        st.write("Usage by Department")
        data = df[['Admin','Account','CTU','EI','Modelling','PE','Malaria','CNS','Dengue','Lab','MicroLab','Zoonoses','VA-ward']]
        st.bar_chart(data)
    else:
        st.write("Total of Ink Cartridges")
        tdata = df[['Printer','InkCode','InkTotal']]
        idmin = df['InkTotal'].idxmin()
        idmax = df['InkTotal'].idxmax()

        st.bar_chart(tdata['InkTotal'])
        st.write(tdata)
        st.write(f"Max of Ink {idmax} is {df.loc[idmax, 'InkTotal']}")
        st.write(f"Min of Ink {idmin} is {df.loc[idmin, 'InkTotal']}")

def main():
    st.title("INK MANAGEMENT")

    fileUpload = st.file_uploader("Upload file", type=['csv','xlsx','pickle'])

    file = "Data/InkMgmt.csv"
    # df = get_df(file)
    df = pd.read_csv(file,
                     index_col=['CodeIndex'])

    task = st.sidebar.radio('TASK', ['Stock Export', 'Stock Import', 'Stock Report'], 0)
    if task == 'Stock Export':
        Xuat_Kho(df)
    elif task == 'Stock Import':
       Nhap_Kho(df)
    else:
        Thong_Ke(df)

main()
