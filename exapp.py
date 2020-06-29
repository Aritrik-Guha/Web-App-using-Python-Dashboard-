import streamlit as st
import numpy as np
import csv
import time
import mysql.connector
from mysql.connector import Error
import dash
import dash_core_components as dcc
import dash_html_components as html
import pgeocode#for getting city name from pincode
from datetime import date#for getting current data
import altair as alt
import pandas as pd

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

nomi = pgeocode.Nominatim('in')
try:
    connection = mysql.connector.connect(host='156.67.222.211',
                                         database='u461278309_sentrifugo_tem',
                                         user='u461278309_temp',
                                         password='E~]hZI&!')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        #print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        #print("You're connected to database: ", record)
        query = "select isactive,department_name from main_employees_summary";
        cursor.execute(query)
        record = cursor.fetchall()

        #for gettig information about no. of employee in each departments.
        
        i=0
        count = []#for storing no. of employees in all departments
        depart = []#for storing name of all departments
        while i<len(record):
            if record[i][0]!=1:#check for the active members
                record.pop(i)
                i=i-1
            i=i+1
        record.pop(0)#removing none department
        for i in record:
            depart.append(i[1]) #extracting all the names of the department from the output of query
        unique_depart = list(dict.fromkeys(depart))#taking out unique values of department
    #unique_department is assigned with the names of all department.
        for i in range(len(unique_depart)):
            count.append(0)
            for j in depart:
                if unique_depart[i]==j:
                    count[i]=count[i]+1#counting no. of people belonging to a paticular department.
        #print(unique_depart)
        #print(count)

        #NOW unique depart is assigned with the names of all the departments.
        #count is a list assigned with the count of people belonging to any department.
        #count[i] is the count of people belonging to unique_depart[i].


        #finding employee on leave
        dd=date.today()
        query =query = "select user_name,to_date from main_leaverequest_summary where isactive=1 and leavestatus='Approved' and to_date<"+str(dd);
        cursor.execute(query)
        record = cursor.fetchall()
        names=[]
        for i in record:
            print(i)
            names.append(str(i[0])+',')
        #print(names)
        names.insert(0,'EMPLOYEES ON LEAVE:-  ')
        if len(names)==1:
           names.insert(1,'NONE')


        #counting no. of males and female employees
        query = "select count(prefix_name) from main_employees_summary where isactive=1 and prefix_name='Mr'";
        cursor.execute(query)
        record = cursor.fetchall()
        male_count = record[0][0]
        query = "select count(prefix_name) from main_employees_summary where isactive=1 and prefix_name='Ms'";
        cursor.execute(query)
        record = cursor.fetchall()
        female_count = record[0][0]
        #print(male_count)
        #print(female_count)


        #finding information about the positions at codepth
        query = "SELECT distinct(positionname) FROM  main_positions WHERE isactive=1;"
        cursor.execute(query)
        record = cursor.fetchall()
        position=[]
        for i in record:
            position.append(str(i[0])+',')
        position.insert(0,'POSITIONS AT CODEPTH:-  ')



        #finding names of city from where employees are present:-
        query = "SELECT distinct(current_pincode) FROM  main_empcommunicationdetails WHERE isactive=1 and current_pincode IS NOT NULL;"
        cursor.execute(query)
        record = cursor.fetchall()
        city=[]
        for i in record:
            x=nomi.query_postal_code(str(i[0]))
            city.append(str(x['county_name'])+',')
        city = list(dict.fromkeys(city))
        city.insert(0,'LOCATION OF EMPLOYEES:-  ')

        #finding no of employees from different years
        query = "SELECT educationlevel FROM  main_empeducationdetails where isactive=1;"
        cursor.execute(query)
        record = cursor.fetchall()
        education_level_count=[0,0,0,0,0,0]
        for i in record:
            education_level_count[i[0]-1]=education_level_count[i[0]-1]+1
        #print(education_level_count)
        education_level_label=['FIRST YEAR','SECOND YEAR','THIRD YEAR','FOURTH YEAR','FIFTH YEAR','GRADUATE']    
        #print(education_level_label)


        #finding count of each positions at codepth
        count_position=[]
        query = "select count(jobtitleid) from main_positions where jobtitleid in(1,2,3,4) and isactive=1";
        cursor.execute(query)
        record = cursor.fetchall()
        count_position.append(record[0][0])
        query="select count(jobtitleid) from main_positions where jobtitleid in(5,6,8,10,12) and isactive=1";
        cursor.execute(query)
        record = cursor.fetchall()
        count_position.append(record[0][0])
        query = "select count(jobtitleid) from main_positions where jobtitleid in(11,13,14,15,16,17,18,19,20,21) and isactive=1";
        cursor.execute(query)
        record = list(cursor.fetchall())
        count_position.append(record[0][0])
        query = "select count(jobtitleid) from main_positions where jobtitleid in(22) and isactive=1";
        cursor.execute(query)
        record = cursor.fetchall()
        count_position.append(record[0][0])
        label_position=['OFFICER','MANAGER','DEVELOPER','INTERN']
        #print(count_position)

        
        connection.close()
except Error as e:
    print("Error while connecting to MySQL", e)


#st.balloons()
from PIL import Image
image = Image.open('codepth2.jpg')
st.image(image, caption='Codepth Technologies',use_column_width=True)

st.title('DASHBOARD')
st.header('Welcome to **Codepth Technologies!!**') 
st.subheader('With this visualized tour, learn more about our employees and operations...')


t1="<h3><div><span class='highlight red'>Employees and their status</span></div></h3>"
st.markdown(t1,unsafe_allow_html=True)


mes=pd.read_csv("main_employees_summary.csv")
mes=mes.fillna('NA')
mes2=pd.read_csv("employee_status.csv")
mes2=mes2.fillna('NA')
mes2


t2="<h3><div><span class='highlight red'>Employee Gender Ratio</span></div></h3>"
st.markdown(t2,unsafe_allow_html=True)

import plotly.express as px
fig = px.pie(mes, values=[male_count,female_count], names=['MALE EMPLOYEE','FEMALE EMPLOYEE'])
#fig.show()
st.plotly_chart(fig, use_container_width=True)

t3="<h3><div><span class='highlight red'>Employee Count in each Department</span></div></h3>"
st.markdown(t3,unsafe_allow_html=True)

fig2 = px.bar(mes, x=unique_depart, y=count)
st.plotly_chart(fig2, use_container_width=True)

t4="<h3><div><span class='highlight red'>Employee and Intern Backgrounds</span></div></h3>"
st.markdown(t4,unsafe_allow_html=True)


mes3=pd.read_csv("main_empeducationdetails.csv")
mes3=mes3.fillna('NA')

fig3 = px.bar(mes3, x=education_level_label, y=education_level_count)
st.plotly_chart(fig3, use_container_width=True)

t5="<h3><div><span class='highlight red'>Positions in Codepth and No. of Employees in each position</span></div></h3>"
st.markdown(t5,unsafe_allow_html=True)


mes4=pd.read_csv("main_positions.csv")
mes4=mes4.fillna('NA')

fig4 = px.bar(mes4, x=label_position, y=count_position)
st.plotly_chart(fig4, use_container_width=True)
