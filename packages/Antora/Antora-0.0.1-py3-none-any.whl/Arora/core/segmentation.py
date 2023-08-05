"""
THIS IS A WIP file and is subject to change, will probably be turned into a directory later on
when more features have been implemented
"""
import datetime
from typing import List

import pandas as pd
from pandas import DataFrame


# TODO: comment
# TODO: pretty up the code through typing conventions
# TODO: UnitTests


def get_sample_segment(onset: int, signals: List[int or float], freq: float, duration=30, time_unit="sec"):
    """
    TODO: Allow the user to decide if he only wants to get the signals or also the Dataframe
    :param onset: start of recording in seconds (int)
    :param signals: list of EEG signals (float)
    :param freq: sample frequency of the EEG signals (int)
    :param duration: end of recording in seconds (int)
    :param time_unit: the unit of time for the duration (str)
    :return: a list of EEG signals and pandas DataFrame including the beginning and end index of the sample
    """
    if time_unit == "min":
        duration *= 60
    elif time_unit == "hours":
        duration *= 3600

    signal_list = []
    index_dataframe = pd.DataFrame()

    # find the beginning index by transferring time into index using the sampling frequency
    beg_index = int(onset * freq)

    # find the end index by figuring out the
    end_index = int((onset + duration) * freq)

    # end index might be out of scope of the list in which case we'll return as much as we can
    if end_index > len(signals):
        # TODO: warning/error handling over here
        print("Warning: Duration is beyond the scope of your list, data might not be reliable")

        signal_list = signals[beg_index:]
        end_index = len(signals)
    else:
        signal_list = signals[beg_index: end_index + 1]

    index_dataframe['beg_index'] = [beg_index]
    index_dataframe['end_index'] = [end_index]

    return signal_list, index_dataframe


def epochize(data: pd.DataFrame, channel_names: List[str], epoch_len: int,
             sampling_freq: int or float, start_timestamp: datetime) -> pd.DataFrame:
    """
    Args:
        data: EDF file turned into an array -> pd.DataFrame
        channel_names: The names of the channels to be used -> list[str]
        epoch_len: How long the epoch should be - will be changed to duration later on -> integer
        sampling_freq: The sampling frequency of the data -> float or integer
        start_timestamp: ??? - Will be removed later on

    Returns: A dataframe with the epochs - will be changed later on to a tuple with the epoch,
            start and duration
    """
    # WIP, will need to change the return, and some things in the function so that it will fit
    # previous work
    # Acknowledgement: Katrín Hera, M.Sc. student

    # Find the length of the signal
    l = len(data)
    # Find the number of data points
    number = int(epoch_len * sampling_freq)
    # initialize the epoch list
    epochs = []
    # add the epochs to the list
    for x in range(0, l, int(epoch_len * sampling_freq)):
        epochs.append(data[x:x + number])
    # initialize a list of timestamps at the beginning of each epoch
    timestamps_epoch_start = []
    for i in range(int(len(data) / (epoch_len * sampling_freq))):
        # make start timestamps for all the subsequent epochs and add to list
        next_timestamp = start_timestamp + datetime.timedelta(seconds=epoch_len * i)
        timestamps_epoch_start.append(next_timestamp)
    # make dataframe with timestamps and epoch
    df: DataFrame = pd.DataFrame()
    df['Epoch start'] = timestamps_epoch_start
    df[channel_names] = epochs  # temporarilly commented out for debugging

    # df['eh_test'] = pd.to_datetime(df['start times'])
    # df = df.set_index('Epoch start')
    return df
