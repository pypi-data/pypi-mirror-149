from .utils import *
def cameo_threshold(raw_data,rule='>=',time='time', amptitude='modified_Lmax', event='is_event',threshold=86.0, correction_threshold=94.0, correction_offset=0.3, correction_interval=5.0):
    '''arguments:
        required:
            raw_data: 至少包含時間戳記,音量,事件標記三欄的raw_data DataFrame
        optional:
            rule: 需求與閾值的關係
                '>' : 需求大於閾值則標記
                '>=': 需求大於等於閾值則標記
                '<=': 需求小於等於閾值則標記
                '<' : 需求小於閾值則標記
            time: 含有時間戳記的欄位標題 預設為 'time'
            amptitude: 含有音量的欄位標題 預設為 'modified_Lmax'
            event: 含有事件標記的欄位標題 預設為 'is_event' 
            threshold: 事件閾值 預設為86.0
            correction_threshold: 校正事件的閾值 預設為94.0
            correction_offset: 校正事件的允許誤差值 預設為0.3
            correction_interval: 校正事件的最低時長 預設為5.0
    return value:
        處理完的dataframe
        event_time | start_time | end_time | duration | is_correction
    '''
    dict_out = {'event_time':[],
                'start_time':[],
                'end_time':[],
                'duration':[],
                'is_correction':[]}
    df_in = pd.DataFrame(raw_data)
    lst_time, lst_amptitude, lst_event = data_handler(df_in, time, amptitude, event)
    ts_start, ts_end, bool_is_event, bool_is_correction = event_init()
    float_max_correction_time, ts_correction_start, ts_correction_end = correction_time_init()

    for i in range(len(lst_time)):
        if(bool_is_rule(lst_amptitude[i], rule, threshold)):
            if(ts_start==pd.Timestamp(0.0)):
                ts_start = lst_time[i]
                modified_Lmax_start = lst_amptitude[i]

            if not(ts_correction_start!=0.0 and bool_in_correction(lst_amptitude[i], correction_threshold, correction_offset)):
                ts_correction_start = lst_time[i]

            ts_correction_end = lst_time[i]
            float_correction_time = ts_duration(ts_correction_start, ts_correction_end)
            if(float_correction_time > float_max_correction_time):
                float_max_correction_time = float_correction_time

            if(lst_event[i]):
                bool_is_event = True
                dt_event_time = lst_time[i]

            ts_end = lst_time[i]
            modified_Lmax_end = lst_amptitude[i]
        else:
            if(bool_is_event):
                bool_is_correction = (float_max_correction_time > correction_interval)
                update_dict(dict_out, dt_event_time, ts_start, ts_end, bool_is_correction)
            
            ts_start, ts_end, bool_is_event, bool_is_correction = event_init()
            float_max_correction_time, ts_correction_start, ts_correction_end = correction_time_init()
    return pd.DataFrame(dict_out)