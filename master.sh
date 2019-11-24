input_stock_name="TATAMOTORS"
outputDir="TATA_analysis"
input_start_date="2019,11,3"
input_end_date="2019,11,22"
input_fut_exp_date1="2019,11,28"
input_fut_exp_date2="2019,12,26"

mkdir -p $outputDir
python3 get_stock_eq.py $input_stock_name $outputDir $input_start_date $input_end_date $input_fut_exp_date1 $input_fut_exp_date2
