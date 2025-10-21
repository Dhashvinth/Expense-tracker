from faker import Faker
import random
import streamlit as st
fake = Faker()
categories = ["Groceries", "Stationary", "Bills", "Subscription", "Investment", "Transportation"]
payment_modes = ["UPI","Cash","Credit card"]
bills = ["Water bill", "Electricity bill", "wifi", "Phone", "gas", "petrol", "food", "snacks","rent", "movie"]
subscription = ["spotify", "bend","gym","netflix"]

import pandas as pd
from datetime import datetime
from dateutil import parser
def gen_exp_data1(num_entries = 10,a = '2025,1,1',b = '2025,1,31',c='Jan'):
    a = parser.parse(a)
    b = parser.parse(b)
    data1=[]
    for _ in range(num_entries):
        expense1 = {
            "Date":fake.date_between_dates(date_start=a, date_end=b),
            "Category": random.choice(categories),
            "Payment_Mode": random.choice(payment_modes),
            "Description": fake.sentence(),
            "Amount": round(random.uniform(10,1000),2),
            "Cashback":round(random.uniform(10,100),2)
        }
        data1.append(expense1)
    return pd.DataFrame(data1)

Jan = gen_exp_data1(150,('Jan 1 2025'),('Jan 31 2025'))
Feb = gen_exp_data1(150,('Feb 1 2025'),('Feb 28 2025'))
Mar = gen_exp_data1(150,('Mar 1 2025'),('Mar 31 2025'))
Apr = gen_exp_data1(150,('Apr 1 2025'),('Apr 30 2025'))
May = gen_exp_data1(150,('May 1 2025'),('May 31 2025'))
June = gen_exp_data1(150,('June 1 2025'),('June 30 2025'))
July = gen_exp_data1(150,('July 1 2025'),('July 31 2025'))
August =  gen_exp_data1(150,('Aug 1 2025'),('Aug 31 2025'))
Sep = gen_exp_data1(150,('Sep 1 2025'),('Sep 30 2025'))
Oct = gen_exp_data1(150,('Oct 1 2025'),('Oct 31 2025'))
Nov= gen_exp_data1(150,('Nov 1 2025'),('Nov 30 2025'))
Dec = gen_exp_data1(150,('Dec 1 2025'),('Dec 31 2025'))

final = pd.concat([Jan,Feb,Mar,Apr,May,June,July,August,Sep,Oct,Nov,Dec])
updated = final['Payment_Mode'] == 'Cash'
final.loc[updated, 'Cashback'] = 0
updated1 = final['Payment_Mode'] == 'Credit card'
final.loc[updated1,'Cashback'] = 0.02*(final.loc[updated1,'Amount'])
print(final)

st.title("Personal Expense tracker")
import pymysql
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Dhashvinth",
    database = "expense_new"
)

mycursor=connection.cursor()

create_table_query = """

CREATE TABLE IF NOT EXISTS final (
    Date date,
    Category VARCHAR(100),
    Payment_Mode VARCHAR(100),
    Description VARCHAR(1000),
    Amount int,
    Cashback int
)
"""

connection.commit()
options = st.selectbox("Queries",["1.Display the entire table",
                                  "2.Display total sum and cashback",
                                  "3.Display the payment mode which gives maximum cashback",
                                  "4.Displaying no of transactions for each payment mode",
                                  "5.Average cashback for each payment mode",
                                  "6.Average amount spent for each category",
                                  "7.Average amount spent for each category by cash",
                                  "8.Amount spend on each month",
                                  "9.Amount spent on each category in April",
                                  "10.Total amount spent except investment - month wise for top 4 month"], placeholder="Select an option", index=None)

if options == "1.Display the entire table":
    mycursor.execute("SELECT * FROM final")
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)

elif options == "2.Display total sum and cashback":
    mycursor.execute("SELECT SUM(Amount) as total_amount, SUM(Cashback) as total_cashback_received FROM final")
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "3.Display the payment mode which gives maximum cashback":
    mycursor.execute("SELECT SUM(Amount) as total_amount, SUM(Cashback) as total_cashback_received, Payment_Mode FROM final GROUP BY Payment_Mode ORDER BY total_cashback_received DESC")                
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "4.Displaying no of transactions for each payment mode":
    mycursor.execute("SELECT count(*) as no_of_transactions, Payment_Mode FROM final GROUP BY Payment_Mode")                
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "5.Average cashback for each payment mode":
    mycursor.execute("SELECT AVG(Cashback) as average_cashback, Payment_Mode FROM final GROUP BY Payment_Mode")                
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "6.Average amount spent for each category":
    mycursor.execute("SELECT Category, AVG(Amount) as average_amount FROM final GROUP BY Category")                
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "7.Average amount spent for each category by cash":
    mycursor.execute("SELECT Category, AVG(Amount) as average_amount FROM final WHERE Payment_Mode = 'Cash' GROUP BY Category")                
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "8.Amount spend on each month":
    mycursor.execute("SELECT monthname(Date) as Month, SUM(Amount) as total_amount_spent FROM final GROUP BY monthname(Date) ORDER BY SUM(Amount) DESC")                
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)
    st.write(data)  

elif options == "9.Amount spent on each category in April":
    mycursor.execute("SELECT Category, SUM(Amount) as total_amount_spent FROM final WHERE monthname(Date) = 'April' GROUP BY Category ORDER BY SUM(Amount) DESC")
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)  
    st.write(data)

elif options == "10.Total amount spent except investment - month wise for top 4 month":
    mycursor.execute("SELECT monthdate(Date), SUM(Amount) as total_amount_spent from final where Category!= 'Investment' GROUP BY monthname(Date) ORDER BY SUM(Amount) DESC")
    columns = [i[0] for i in mycursor.description]
    data = pd.DataFrame(data, columns=columns)  
    st.write(data)


connection.close()
