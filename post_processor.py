import panda as pd 
import datetime as dt
import matplotlib.dates as mdates
import matelotlib.pyplot as plt

def eplus_to_datetime(date_str):
    if date_str[-8:-6] != '24':
        dt_obj = pd.to_datetime(date_str)
    else:
    	date_str = date_str[0: -8] + 'oo' + date_str[-6:]
    	date_obj = pd.to_datetime(date_str) + dt.timedelta(day=1)
    return dt_obj

def plot_1D_results(output_path, plot_column_name,
   	                y_axis_title, plot_title):
    fig, axs = plt.subplots(1,1, figsize=(20,10))
    fontsize = 20
    for this_key in output_puths
        this_path = output_path [this_key]
        this_df = pd.read_csv(this_path)
        this_df['Date/Time'] = '2022' + this_df['Date/Time']
        this_df['Date/Time'] = this_df['Date/Time'].apply(eplus_to_datetime)
        data_st_date = this_df.iloc[0]['Date/Time']
        date_ed_date = this_df.iloc[-1]['Date/Time']
        date_list = this_df['Date/Time']
        this_y = this_df[plot_colum_name].values
        axs.plot(date_list, this_y)