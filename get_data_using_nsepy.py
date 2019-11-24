from datetime import date
import pandas as pd
import sys
import time
from nsepy import get_history


#input definitions
input_stock_name = sys.argv[1]
outputDir = sys.argv[2]
input_start_date = sys.argv[3]
input_end_date = sys.argv[4]
input_fut_exp_date1 = sys.argv[5]
input_fut_exp_date2 = sys.argv[6]

#Defining output files as per inputs
equity_result_FileName = f'{outputDir}/cash_market_details_{input_stock_name}.csv'
fut_result_FileName1 = f'{outputDir}/fut_market_details_currentmonth_{input_stock_name}.csv'
fut_result_FileName2 = f'{outputDir}/fut_market_details_nextmonth_{input_stock_name}.csv'

#preparing inputs from given input
fields_start_eq = input_start_date.split(",")
input_eq_start_year=int(fields_start_eq[0])
input_eq_start_month=int(fields_start_eq[1])
input_eq_start_day=int(fields_start_eq[2])

fields_end_eq = input_end_date.split(",")
input_eq_end_year=int(fields_end_eq[0])
input_eq_end_month=int(fields_end_eq[1])
input_eq_end_day=int(fields_end_eq[2])

#input_fut_exp_date1
fileds_fut_exp1 = input_fut_exp_date1.split(",")
input_fut_exp1_year=int(fileds_fut_exp1[0])
input_fut_exp1_month=int(fileds_fut_exp1[1])
input_fut_exp1_day=int(fileds_fut_exp1[2])

fileds_fut_exp2 = input_fut_exp_date2.split(",")
input_fut_exp2_year=int(fileds_fut_exp2[0])
input_fut_exp2_month=int(fileds_fut_exp2[1])
input_fut_exp2_day=int(fileds_fut_exp2[2])
#print(input_start_date,input_end_date,input_fut_exp_date1,input_fut_exp_date2)

#getting Equity details from nse and write to a file
def get_equity_data_from_nse():
    eq_details = get_history(symbol=input_stock_name,
                   start=date(input_eq_start_year,input_eq_start_month,input_eq_start_day),
                   end=date(input_eq_end_year,input_eq_end_month,input_eq_end_day))

    #print(sbin.columns)
    eq_query_result = open(equity_result_FileName, "w")
    eq_query_result.write(str(eq_details.to_csv()))
    eq_query_result.close()

# getting Future details for current month from nse and write to two files
def get_futures__currentmonthdetails_from_nse():
    stock_fut_currentmonth_details = get_history(symbol=input_stock_name,
                            start=date(input_eq_start_year, input_eq_start_month, input_eq_start_day),
                            end=date(input_eq_end_year, input_eq_end_month, input_eq_end_day),
                            index=False,
                            futures=True,
                            expiry_date=date(input_fut_exp1_year, input_fut_exp1_month, input_fut_exp1_day))
    fut_query_result1 = open(fut_result_FileName1, "w");
    fut_query_result1.write(str(stock_fut_currentmonth_details.to_csv()));
    fut_query_result1.close();

# getting Future details for current month from nse and write to two files
def get_futures__nextmonthdetails_from_nse():
    stock_fut_nextmonth_details = get_history(symbol=input_stock_name,
                            start=date(input_eq_start_year, input_eq_start_month, input_eq_start_day),
                            end=date(input_eq_end_year, input_eq_end_month, input_eq_end_day),
                            index=False,
                            futures=True,
                            expiry_date=date(input_fut_exp2_year, input_fut_exp2_month, input_fut_exp2_day))
    fut_query_result2 = open(fut_result_FileName2, "w");
    fut_query_result2.write(str(stock_fut_nextmonth_details.to_csv()));
    fut_query_result2.close();

def read_cash_dat():
    cash_d = pd.read_csv(equity_result_FileName)
    #cash_d['YClose'] = (pd.to_numeric(cash_d['Prev Close']))
    #print(cash_d['YClose'])
    #print(cash_d.head());
    for col in cash_d.columns:
        print(col)
        exit();



get_equity_data_from_nse();
time.sleep(320);
get_futures__currentmonthdetails_from_nse();
time.sleep(320);
get_futures__nextmonthdetails_from_nse();
