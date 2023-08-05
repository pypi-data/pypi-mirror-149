import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from strym import strymread

from .file_iterator import FileIteratorCanGps
from .cache import init_cache
from .cyverse_io_irods import IRODSPut
from ..global_variables.global_variables import local_long_folder


def read_metadata_from_event_analysis_name(filename: str):
    '''
    :param filename: name of the file onto which extract metadata
    :return: Dict object with those fields:
    {
        filename: <>,
        name: <>,
        created_on: <>,
        minimum_speed: <>, 
        previous_treshold_speed: <>, 
        following_treshold_speed: <>, 
    }
    '''
    splitted_filename = filename.split('&')
    return {
        'filename': filename,
        'name': splitted_filename[1],
        'created_on': splitted_filename[2].split('=')[1],
        'minimum_speed': splitted_filename[3].split('=')[1],
        'previous_treshold_speed': splitted_filename[4].split('=')[1],
        'following_treshold_speed': splitted_filename[5].split('=')[1]
    }


def read_strym_can_data(canfile, verbose: bool = False):
    """
    Parses CAN data with Strymread
    :param canfile: string, csv file
    :return: strymreads of can and gps files, dictionnary of the meta-datas associated
    """

    # read canfile
    s = strymread(csvfile=canfile)
    if verbose:
        print(f'reading of {canfile} was succesful? {s.success}')

    # metadata from filename
    date_time = canfile.split('/')[-1][0:19]
    vin = canfile.split('/')[-1][20:37]

    return s, {'date_time': date_time, 'vin': vin}


def read_can_data_for_car_crossing_detection(can):
    """
    :param can: strymread object
    :param gps: strymmap object
    :return: speed, lead_distance, cruise_control time series
    """
    try:
        speed_ts = can.speed()
        lead_distance_ts = can.lead_distance()
        cruise_control_state_ts = can.acc_state()
        return speed_ts, lead_distance_ts, cruise_control_state_ts
    except Exception as err:
        print(f"Error while trying to read the time series.\nFailed on: {err}")
        raise Exception(err)


def find_ts_state_at_given_time(ts, ts_time, event_time):
    """
    Finds the value of a time series at a given point in time. Uses the closest time point to the event
    :param ts: Time Series messages list to search within
    :param ts_time: Time Series time list
    :param event_time: Time at which we want the value
    :return:
    """
    min_index = np.argmin([np.abs(time - event_time) for time in ts_time])
    return ts[min_index]


def find_crossing(speed, lead_distance, cruise_control_state, speed_treshold = 20, prev_treshold = 10, next_treshold = 5, verbose: bool = False):
    """
    finds the time where car crossing events happens, from ts associated to 1 specific acquisition
    this functions find the acceptable intervals where the constraints on speed and cruise control are valid,
    then finds the places where crossings happens, filtering them by the acceptable times (this allows to handle
    different sampling frequencies over the different time series)
    :param speed: Time Series of the speed
    :param lead_distance: Time Series of the Speed
    :param cruise_control_state: Time Series of the Controller state (=6 if activated)
    :param speed_treshold: minimum speed to consider a dangerous time crossing event, in km/h
    :param prev_treshold: minimum lead distance before the crossing to consider the event as a car crossing
    :param next_treshold: maximum lead distance after the crossing to consider the car crossing as dangerous
    :param verbose: Set to true to get more logs
    :return: array<time>, of event_times of car crossing events
    """
    event_times = []
    controller_states = []
    speeds = []
    unacceptable_crossings = []

    lead_distance_list = lead_distance['Message']
    lead_time_list = lead_distance['Time']
    len_lead = len(lead_time_list)

    speed_list = speed['Message']
    speed_time_list = speed['Time']
    len_speed = len(speed_time_list)

    cc_state_list = cruise_control_state['Message']
    cc_state_time_list = cruise_control_state['Time']

    # Acceptable times for cruise control state and speed:
    # composed of time interval objects {"beg": time_begining, "end": time_ending}
    acceptable_range_speed = []
    currently_valid = False
    current_interval = {"beg": None, "end": None}
    for i in range(len_speed):
        if speed_list[i] >= speed_treshold and not currently_valid:
            currently_valid = True
            current_interval['beg'] = speed_time_list[i]
        elif speed_list[i] < speed_treshold and currently_valid:
            currently_valid = False
            current_interval['end'] = speed_time_list[i]
            acceptable_range_speed.append(current_interval)
            current_interval = {"beg": None, "end": None}

    # case if the speed is still acceptable at the end of the file:
    if current_interval['beg'] and not current_interval['end']:
        current_interval['end'] = speed_time_list[-1]
        acceptable_range_speed.append(current_interval)

    for i in range(1, len_lead):
        is_lead_distance_acceptable = (lead_distance_list[i - 1] >= prev_treshold) and (lead_distance_list[i] <= next_treshold)
        if is_lead_distance_acceptable:
            # if at this time a car crossing occurs, we check that the conditions to store this event are valid
            time_event = lead_time_list[i]
            unacceptable_crossings.append(time_event)
            for interval in acceptable_range_speed:
                if interval['beg'] <= time_event <= interval['end']:
                    event_times.append(time_event)
                    controller_states.append(find_ts_state_at_given_time(cc_state_list, cc_state_time_list, time_event))
                    speeds.append(find_ts_state_at_given_time(speed_list, speed_time_list, time_event))

    if verbose:
        print(f'acceptable range for speed > {speed_treshold} m/s: {acceptable_range_speed}')
        print(f'number of crossings detected: {len(unacceptable_crossings)}')
        print(f'number of valid crossings detected: {len(event_times)}')
        print(f'event times of valid crossings: {event_times}')

    return event_times, controller_states, speeds

def plot_events_over_lead(name, lead, times, event_times):
    """
    :param lead: Time series of the lead_distance
    :param times: Time series of the times (for the lead_distance)
    :param event_times: Times of the events to plot (list of times)
    :return: Plots the lead_distance time series, with the events as overlaying ticks.
    """
    def fake(time):
        if time in event_times:
            return 252
        else:
            return 0
    event_times_fake = [fake(time) for time in times]

    # plot the figure
    fig, ax = plt.subplots()
    l = ax.plot(times, lead, 'b.')
    e = ax.plot(times, event_times_fake, 'r-')
    plt.title(name)
    plt.ion()
    plt.show()


def csv_file_namer(name, speed_t, prev_t, next_t):
    return f'{name}&create_on={str(datetime.now()).replace(" ", "_")}&s={speed_t}&p={prev_t}&n={next_t}.csv'


def find_all_events_car_crossing_one_file(canfile, prev_treshold, next_treshold, speed_treshold, verbose: bool = False, plot: bool = False, plot_name: str = '', gpsfile: str = None):
    """
    From a CAN and a GPS file as well as analysis parameters, finds the useful information (all of the events tiles,
    as well as metadata about the acquisition and at event times)
    :param canfile: local path to the CSV of the CAN acquisition
    :param prev_treshold: previous speed treshold for car crossing
    :param next_treshold: next speed threshold for car crossing
    :param speed_treshold: minimum speed to consider a car crossing
    :param verbose: set to True to have more extensive logs
    :param plot: set to True to plot the lead distance as well as the event times
    :param plot_name: name to give to the plot
    :param gpsfile: local path to the GPS of the CAN acquisition. Set to None to ignore.
    NOTE: GPS file will not be used here. Indeed, strymmap only works within notebook
    
    :return: array of:
        - the event times
        - cc states and speeds at time of the events
        - metadata about the acquisition
    (all of those arrays reference the same event for the same indice)
    """

    ignore_gps_file = gpsfile is None
    if not ignore_gps_file:
        raise NotImplementedError(f'Issue while trying to analyze the events in a file.\
            Strymmmap is not configured for python scripts so analyzing gps files here is not possible.')

    s, metadata = read_strym_can_data(canfile, verbose=verbose)
    speed, lead_dist, cc_state = read_can_data_for_car_crossing_detection(s)
    event_times, event_cc_states, event_speeds = find_crossing(speed, lead_dist, cc_state,
                                                           prev_treshold=prev_treshold,
                                                           next_treshold=next_treshold,
                                                           speed_treshold=speed_treshold,
                                                           verbose=verbose)

    if plot:
        strymread.plt_ts(lead_dist)
        plot_events_over_lead(plot_name, lead_dist['Message'], lead_dist['Time'], event_times)

    return event_times, event_cc_states, event_speeds, metadata


async def find_all_events_car_crossing(file_exploration_name: str, db_analysis_name:str, speed_threshold: float, previous_distance_threshold: float, next_distance_threshold: float, exploration_filters_vin: str = None, exploration_filters_date: str = None, verbose: bool = False):
    """
    Launches the creation of the exploration and event analysis CSV file
    For the moment, only the Car Crossing event is found.
    More can be added, as leading vehicle strong deceleration for instance.
    :param file_exploration_name: <str>, path on CyVerse to the file exploration you wish to use
    :param db_analysis_name: <str>, small description of the full analysis. Must be in 1 word (automated information are added)
    :param speed_threshold: <float>, minimum speed, in m/s
    :param previous_distance_threshold: <float>, minimum distance before the crossing
    :param next_distance_threshold: <float>, maximum distance after the crossing
        note: the crossing is detected as a discontinuity in lead_distance time series
    :param exploration_filters_vin: <str> VIN of the vehicle. Set to None if you don't want to filter on this criteria
    :param exploration_filters_date: <str> Date to keep. string formatted as YYYY-MM-DD. Keep only the runs from this day. Set to None if you don't want to filter on this criteria    
    :param verbose: <bool>, set to True to have extensive logs (for development purposes)
    :return: return local address of the analysis (CSV file)
    """
    # Exploration of the file share
    if verbose:
        print('opening the file handler')    

    file_iterator = FileIteratorCanGps(ignore_gps_file=True)
    local_exploration = await file_iterator.get_specific_user_exploration(file_exploration_name, clear_long_cache=True)
    file_iterator.filter(date=exploration_filters_date, vin=exploration_filters_vin)

    # Naming of the output
    full_analysis_csv_filename = 'analysis&' + csv_file_namer(db_analysis_name, speed_threshold, previous_distance_threshold, next_distance_threshold)

    # Analysis of the events
    output_data = {'remote_addresses': [], 'event_time': [], 'event_speeds': [], 'event_cc_state': [], 'event_type': [], 'date_time': [], 'vin': []}
    if verbose:
        print('Starting the analysis of the events in the explored files')

    for index in range(file_iterator.index, file_iterator.max_index):
        if verbose:
            print('\nINDEX is ', index, ' out of ', file_iterator.max_index)

        try:
            # download files
            current_can_file, remote_can_file = await file_iterator.next()
            if verbose:
                print('starting analysis of the file: ', current_can_file)

            try:
                # event analysis for car crossing
                event_times, event_cc_states, event_speeds, metadata = find_all_events_car_crossing_one_file(
                    current_can_file,
                    prev_treshold=previous_distance_threshold,
                    next_treshold=next_distance_threshold,
                    speed_treshold=speed_threshold,
                    verbose=verbose)

                # add the metadata to the events
                event_type = 'car_crossing'
                number_of_events = len(event_times)
                if number_of_events > 0:
                    output_data['event_time'].extend(event_times)
                    output_data['event_speeds'].extend(event_speeds)
                    output_data['event_cc_state'].extend(event_cc_states)
                    output_data['remote_addresses'].extend([remote_can_file] * number_of_events)
                    output_data['event_type'].extend([event_type] * number_of_events)
                    output_data['date_time'].extend([metadata['date_time']] * number_of_events)
                    output_data['vin'].extend([metadata['vin']] * number_of_events)

                
                ########################################################################
                #                                                                      #
                # Place your code here if you wish to add more event detections types  #
                #                                                                      #
                ########################################################################


            # NOTE: we catch those exception without raising, as often some of the files are bugged
            # and 1 or 2 files out of a lot have problems preventing them to be red.
            except Exception as err:
                print(f'there was an issue trying to scan {current_can_file}. \nFailed on: {err}')
        except Exception as err:
            print(f'there was an issue trying to download file at index {index}. \nFailed on: {err}')


    # CSV logging
    if verbose:
        print(f'starting to write the data to the CSV')
    try:
        df = pd.DataFrame(data=output_data)
        local_analysis_address = os.path.join(local_long_folder, full_analysis_csv_filename)
        df.to_csv(path_or_buf=local_analysis_address)

        if verbose:
            print(f'analysis was written down in: {full_analysis_csv_filename}')
    
    except Exception as e:
        error_msg = f'Error trying to write the CSV file. \nFailed on : {e}'
        if verbose:
            print(df)
            print(error_msg)
        return Exception('error_msg')

    # clean caches
    init_cache()

    # return local address
    return local_analysis_address