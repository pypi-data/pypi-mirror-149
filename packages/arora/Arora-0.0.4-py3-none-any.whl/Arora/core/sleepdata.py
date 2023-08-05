import csv
from datetime import datetime, timedelta
from dateutil import parser
import numpy as np
import pandas as pd
from pytz import timezone


withings_signal_names = {
    'withings_sleep_state': 'raw_sleep-monitor_sleep-state',
    'withings_sleep_hr': 'raw_sleep-monitor_hr',
    'withings_watch_state': 'raw_tracker_sleep-state',
    'withings_watch_hr': 'raw_tracker_hr',
    'withings_sleep_movement_max': 'raw_sleep-monitor_maximum_movement',
    'withings_sleep_movement_pim': 'raw_sleep-monitor_movement_pim',
}


def get_e4_info(filename):
    with open(filename, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        i = 0
        for row in csv_reader:
            if i == 0:
                n = len(row)
                start_time = ['']*n
                for j in range(len(start_time)):
                    start_time[j] = datetime.utcfromtimestamp(float(row[j])).isoformat(
                        sep=' ',
                        timespec='milliseconds'
                    )
            elif i == 1:
                n = len(row)
                freq = [0.0]*n
                for j in range(len(freq)):
                    freq[j] = float(row[j])
            else:
                break
            i += 1
        return start_time, freq


def e4_to_dataframe(signal_name, path):
    """

    Args:
        signal_name:
        path:

    Returns:

    """
    file = path + signal_name + '.csv'
    start, freq = get_e4_info(file)
    period = 1000000/(freq[0]) # In microseconds

    signal_df = pd.read_csv(file, skiprows=2, header=None)

    daterange = pd.date_range(
            start = start[0],
            periods = len(signal_df),
            freq = str(int(period))+'U'
            )

    df = pd.DataFrame(daterange, columns=['time'])
    df = pd.concat([df, signal_df], axis=1)
    df['datetime'] = pd.to_datetime(df['time'])
    df = df.set_index('datetime')
    df.drop(['time'], axis=1, inplace=True)

    return df


def withings_csv_to_dataframe(signal, path):

    signalname = withings_signal_names[signal]
    file = path + signalname + '.csv'
    with open(file, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        i=0
        for row in csv_reader:
            row = np.array(row)
            if i==0:
                signal_np = np.array([row])
            else:
                starttime = parser.parse(row[0])
                vals = np.fromstring(row[2][1:-1], sep=',')
                durations = np.fromstring(row[1][1:-1], sep=',')
                for j in range(len(vals)):
                    val = vals[j]
                    duration = durations[j]
                    starttime = starttime+timedelta(seconds=int(duration))
                    starttime = starttime.astimezone(timezone('GMT')) # GMT for Iceland
                    signal_np = np.append(signal_np,[[starttime, duration, val]], axis=0)
            i = i+1

        df = pd.DataFrame(data=signal_np[1:,1::], index=signal_np[1:,0], columns=signal_np[0,1:]).sort_index()

        return df