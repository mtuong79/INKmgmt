# MT@OUCRU

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import date
import base64
import smtplib, ssl
from email.message import EmailMessage

def Email_Order(msgbody):
    # Less secure app access on Gmail Security: Turn on

    port = 587  # starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "it.oucru@gmail.com"
    receiver_email = "manhtuong@gmail.com; mtuong@eocru.org"
    password = "Wellcome2"

    message = f"""\
    Hi !
    Please order the Ink Cartrdiges with the code and quantity as below,
    
    {msgbody}
    
    Thanks,
    ServiceDesk"""

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Ink Catridges'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        #server.sendmail(sender_email, receiver_email, message)
        server.send_message(msg)

    st.success(f"Your order is conformed and sent to manhtuong@gmail.com")

def Xuat_Kho(df):
    file = "Data/Data_InkMgmt.csv"
    st.subheader("STOCK EXPORT")
    #st.write(df)
    #st.dataframe(df.style.highlight_min(axis=0))
    df['Inventory'] = df['Inventory'].astype(int)
    df['Admin'] = df['Admin'].astype(int)
    df['Account'] = df['Account'].astype(int)
    df['CTU'] = df['CTU'].astype(int)
    df['EI'] = df['EI'].astype(int)
    df['IT'] = df['IT'].astype(int)
    df['Estate'] = df['Estate'].astype(int)
    df['MolEPI'] = df['MolEPI'].astype(int)
    df['Modelling'] = df['Modelling'].astype(int)
    df['PE'] = df['PE'].astype(int)
    df['Malaria'] = df['Malaria'].astype(int)
    df['CNS'] = df['CNS'].astype(int)
    df['Dengue'] = df['Dengue'].astype(int)
    df['TB'] = df['TB'].astype(int)
    df['Lab'] = df['Lab'].astype(int)
    df['MicroLab'] = df['MicroLab'].astype(int)
    df['Zoonoses'] = df['Zoonoses'].astype(int)
    df['VA-ward'] = df['VA-ward'].astype(int)
    df['InkTotal'] = df['InkTotal'].astype(int)

    with st.form("my_form"):
        department = st.selectbox("Department", ('Admin', 'Account', 'CTU', 'EI','IT', 'Estate' ,'MolEPI', 'Modelling', 'PE', 'Malaria', 'CNS', 'Dengue', 'TB', 'Lab', 'MicroLab', 'Zoonoses', 'VA-ward'))
        inkcode = st.selectbox("Ink Code",df['InkCode'])
        #x_quantity = st.number_input(f"Quantity", value=0)

        submitted = st.form_submit_button("Submit")
        if submitted:
            Thang =  date.today().strftime("%b")

            inventory = df.loc[inkcode, 'Inventory']

            if inventory > 0:
                df.loc[inkcode, 'Inventory'] = inventory - 1
                df.loc[inkcode, department] += 1
                df.loc[inkcode, Thang] += 1
                st.success(f"Successfully Exported: {inkcode} for {department}")
            else:
                st.error("Out of Stock")

        st.write(df)

    df.to_csv(file, index=True)

def Nhap_Kho(df):
    file = "Data/Data_InkMgmt.csv"
    st.subheader("STOCK IMPORT")
    #st.dataframe(df[['Printer','InkCode','Inventory','IT-Warehouse']])
    df['Inventory'] = df['Inventory'].astype(int)

    with st.form("my_form"):
        inkcode = st.selectbox("Ink Code",df['InkCode'])
        n_quantity = st.number_input("Quantity", value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            inventory = df.loc[inkcode, 'Inventory']
            total = df.loc[inkcode, 'InkTotal']
            df.loc[inkcode, 'Inventory'] = inventory + n_quantity
            df.loc[inkcode, 'InkTotal'] = total + n_quantity

            #st.write(f"Successfully Updated Inventory: {inkcode} , Totlal: {df.loc[inkcode, 'Inventory']}")
            st.success(f"Successfully Imported: {inkcode} , Total in Stock: {df.loc[inkcode, 'Inventory']}")

        st.write(df[['Printer','InkCode','Inventory','IT-Warehouse']])

    df.to_csv(file, index=True)

def Thong_Ke(df):
    file = "Data/Data_InkMgmt.csv"
    st.subheader("STOCK REPORT")
    tk = st.radio("",('Inventory Summary', 'Usage by Department', 'Total of Ink Cartridges','Order of Ink'))

    if tk == 'Inventory Summary':
        df.sort_values(by='Inventory', ascending=False)
        #st.bar_chart(df['Inventory'])
        chart = (
            alt.Chart(df).mark_bar().encode(
                x='Inventory',
                y=alt.Y('InkCode', sort='-x')
            )
                #.properties(width=800)
        )
        #text = chart.mark_text(align="left", baseline="middle", dx=3).encode(text="Number of data")
        st.altair_chart(chart)

        st.subheader("Out of Stock")

        for inv in df['InkCode']:
            quantity = df.loc[inv, 'Inventory']
            if quantity == 0:
                st.write(f"**{inv}**: _out of stock_")

    elif tk == 'Usage by Department':
        st.write("Usage by Department")
        data = df[['Admin','Account','CTU','EI','IT','Estate','MolEPI', 'Modelling','PE','Malaria','CNS','Dengue','TB','Lab','MicroLab','Zoonoses','VA-ward']]
        st.bar_chart(data)
    elif tk == 'Total of Ink Cartridges':
        st.subheader("Total of Ink Cartridges")
        tdata = df[['Printer','InkCode','InkTotal']].sort_values(by='InkTotal', ascending=False)
        idmin = df['InkTotal'].idxmin()
        idmax = df['InkTotal'].idxmax()

        st.write(f"Max of Ink {idmax} is {df.loc[idmax, 'InkTotal']}")
        st.write(f"Min of Ink {idmin} is {df.loc[idmin, 'InkTotal']}")
        st.bar_chart(tdata['InkTotal'])

        st.subheader("Ink-Cartridge Usage by Month")
        ydata = df[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
        T1 = df['Jan'].sum()
        T2 = df['Feb'].sum()
        T3 = df['Mar'].sum()
        T4 = df['Apr'].sum()
        T5 = df['May'].sum()
        T6 = df['Jun'].sum()
        T7 = df['Jul'].sum()
        T8 = df['Aug'].sum()
        T9 = df['Sep'].sum()
        T10 = df['Oct'].sum()
        T11 = df['Nov'].sum()
        T12 = df['Dec'].sum()

        source = pd.DataFrame({
            'Month': ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'),
            'TotalInk': (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12)
        })
        chart = (
            alt.Chart(source).mark_bar().encode(
                alt.X("Month", sort=None,title=""),
                y="TotalInk",
                #column='TotalInk',
                #color='Month'
            )
                .properties(width=600)
        )
        st.altair_chart(chart)
        st.bar_chart(ydata)

        st.write(tdata)

        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        href = f'<a href="data:file/csv;base64,{b64}" download={file} target="_blank">Download csv file</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:

        df['OrderQuantity'] = df['OrderQuantity'].astype(int)
        df['OrderDate'] = pd.to_datetime(df['OrderDate']) # format='%y%m%d'

        today = date.today()
        order_date = st.date_input('Order date', today)

        with st.form("order_form"):
            st.write("Select the Ink-Code to order")

            inkcode = df["InkCode"]

            sl_order = st.selectbox("", inkcode)
            q_order = st.number_input("Order Quantity", value=0)

            order_submitted = st.form_submit_button("Order")

            if order_submitted:
                df.loc[sl_order,'OrderQuantity'] = q_order
                df.loc[sl_order,'OrderDate'] = today
                st.success(f"Successfully put the inkcode: {sl_order} and quantity: {q_order} into the order list ")
                df.to_csv(file, index=True)

        #st.write(f"This is your order of Ink, date: {order_date}")
        #st.dataframe(df[['InkCode','OrderQuantity']])
        with st.form("conform_oder"):
            st.write(f"This is your order of Ink, date: {order_date}")
            msgbody = ""
            for inkcode in df['InkCode']:
                if df.loc[inkcode,'OrderDate'] == today:
                    st.write(f"{inkcode} : {df.loc[inkcode,'OrderQuantity']}")
                    msgbody += str(inkcode)
                    msgbody += ':'
                    msgbody += str(df.loc[inkcode,'OrderQuantity'])
                    msgbody += '--'

            conform_order = st.form_submit_button("Conform Order")
            if conform_order:
                Email_Order(msgbody)

def main():
    st.title("INK CARTRIDGE MANAGEMENT")

    st.markdown("")
    st.image("img/Img_Header.jpg")

    file = "Data/Data_InkMgmt.csv"
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
