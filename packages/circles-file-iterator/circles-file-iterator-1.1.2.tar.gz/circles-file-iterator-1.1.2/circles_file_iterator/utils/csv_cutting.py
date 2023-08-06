import numpy as np
import pandas as pd

def find_ts_time_close(ts_time, event_time):
    """
    Finds the available time point of a time series closest to a given point in time
    :param ts_time: Time Series time list
    :param event_time: Time at which we want the value
    :return: the time point available for the time series
    """
    min_index = np.argmin([np.abs(time - event_time) for time in ts_time])
    return ts_time[min_index]

def perform_cut(local_address, previous_cut_time, next_cut_time, event_time):
    """
    cuts a CAN/GPS time series before and after the event
    :param local_address: local address of the file to cut
    :param previous_cut_time: float, seconds before the event to keep
    :param next_cut_time: float, seconds after the event to keep
    :param event_time: float
    :return: Path of the cutted file
    """
    df_can = pd.read_csv(local_address)
    filename = local_address.split('/')[-1]
    folders = local_address.split('/')[:-1]
    foldername = ''
    for folder in folders:
        foldername += folder
    new_filename = 'cutted__' + filename

    time_beginning_cut = find_ts_time_close(df_can['Time'], event_time - previous_cut_time)
    time_ending_cut = find_ts_time_close(df_can['Time'], event_time + next_cut_time)
    cutted_df = df_can.loc[(df_can['Time'] >= time_beginning_cut) & (df_can['Time'] <= time_ending_cut)]
    cutted_df.to_csv(path_or_buf=f'results/{new_filename}')
    new_path = foldername + '/' + new_filename
    return new_path