
input_stock_name="INFY"
outputDir="INFY_Final"
input_start_date="2019,11,3"
input_end_date="2019,11,26"
input_fut_exp_date1="2019,11,28"
input_fut_exp_date2="2019,12,26"

mkdir -p $outputDir
python3 analyse_stock_eq.py $input_stock_name $outputDir $input_start_date $input_end_date $input_fut_exp_date1 $input_fut_exp_date2
