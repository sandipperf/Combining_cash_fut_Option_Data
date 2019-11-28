from datetime import date

import time
import pandas as pd
import sys
from nsepy import get_history
import numpy as np


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
final_result_file = f'{outputDir}/Result_{input_stock_name}.csv'

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
fields_fut_exp1 = input_fut_exp_date1.split(",")
input_fut_exp1_year=int(fields_fut_exp1[0])
input_fut_exp1_month=int(fields_fut_exp1[1])
input_fut_exp1_day=int(fields_fut_exp1[2])

fields_fut_exp2 = input_fut_exp_date2.split(",")
input_fut_exp2_year=int(fields_fut_exp2[0])
input_fut_exp2_month=int(fields_fut_exp2[1])
input_fut_exp2_day=int(fields_fut_exp2[2])

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

    eq_data = pd.read_csv(equity_result_FileName, encoding='ISO-8859\xe2\x80\x931')
    fut_current_month = pd.read_csv(fut_result_FileName1, encoding='ISO-8859\xe2\x80\x931')
    fut_next_month = pd.read_csv(fut_result_FileName2, encoding='ISO-8859\xe2\x80\x931')

    result_fut_merge_df = pd.merge(fut_current_month, fut_next_month, on='Date', how='left')

    result_fut_merge_df['cumulation_oi'] = result_fut_merge_df['Open Interest_x'] + result_fut_merge_df['Open Interest_y']

    result_fut_merge_df['cumulation_change_oi'] = result_fut_merge_df['Change in OI_x'] + result_fut_merge_df['Change in OI_y']
    result_fut_merge_df['cumulation_contract'] = result_fut_merge_df['Number of Contracts_x'] + result_fut_merge_df['Number of Contracts_y']
    result_fut_merge_df['Change_in_OI_DivBy_Contract'] = round(result_fut_merge_df['cumulation_oi'] / result_fut_merge_df['cumulation_contract'], 2)



    final_result_df = pd.DataFrame();
    final_result_df['date_eq'] = eq_data['Date'];
    final_result_df['Cash_LTP'] = eq_data['Last'];
    final_result_df['VWAP'] = eq_data['VWAP'];
    final_result_df['Cash_Volume_Divby_Trade'] = round(eq_data['Volume'] / eq_data['Trades'], 2);
    final_result_df['%Deliverble'] = round(eq_data['%Deliverble'] * 100, 2);
    final_result_df['Cummulative_OI'] = result_fut_merge_df['cumulation_oi']
    final_result_df['Cummulative_Change_in_OI'] = result_fut_merge_df['cumulation_change_oi'];

    final_result_df['Change_in_OI_DivBy_Contract'] = result_fut_merge_df['Change_in_OI_DivBy_Contract'];
    final_result_df['Open'] = eq_data['Open'];
    final_result_df['High'] = eq_data['High'];
    final_result_df['Low'] = eq_data['Low'];
    final_result_df['YClose'] = eq_data['Prev Close'];
    final_result_df['%Change'] = round(((final_result_df['Cash_LTP'] - final_result_df['YClose'])/final_result_df['YClose'])*100, 2);


    #Print result to csv file
    final_result_df.to_csv(final_result_file, index=False)







#get_equity_data_from_nse();
#time.sleep(320);
#get_futures__currentmonthdetails_from_nse();
#time.sleep(320);
#get_futures__nextmonthdetails_from_nse();
read_cash_dat();
