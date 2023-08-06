import pandas as pd
def data_handler(df, t, ampt, evt):
    '''return values:
    list(time), list(ampt), list(evt)
    '''
    keys = list(df.keys())
    keys.remove(t)
    keys.remove(ampt)
    keys.remove(evt)
    df.drop(labels=keys, axis=1, inplace=True)
    time = list(df[t])
    amptitude = list(df[ampt])
    event = list(df[evt])
    return time, amptitude, event

def event_init():
    '''return values:
    ts_start, ts_end, bool_is_event, bool_is_correction
    '''
    return pd.Timestamp(0.0), pd.Timestamp(0.0), False, False

def correction_time_init():
    '''return values:
    float_max_correction_time, ts_correction_start, ts_correction_end
    '''
    return 0.0, pd.Timestamp(0.0), pd.Timestamp(0.0)

def ts_duration(ts_start, ts_end):
    return (ts_end - ts_start).total_seconds()

def update_dict(dict_out, dt_event_time, ts_start, ts_end, bool_is_correction):
    dict_out['event_time'].append(dt_event_time)
    dict_out['start_time'].append(ts_start)
    dict_out['end_time'].append(ts_end)
    dict_out['duration'].append(ts_duration(ts_start,ts_end))
    dict_out['is_correction'].append(bool_is_correction)

def bool_in_correction(ampt, cor_thd, offset):
    if(abs(ampt - cor_thd) <= offset):
        return True
    else:
        return False

def bool_is_rule(ampt, rule, thd):
    if(rule == '>'):
        return ampt > thd
    if(rule == '>='):
        return ampt >= thd
    if(rule == '<='):
        return ampt <= thd
    if(rule == '<'):
        return ampt < thd