import csv
import re
from datetime import datetime, timedelta
from io import StringIO
from os import path, sep, listdir
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

np.set_printoptions(precision=2)

date_format = '%Y-%m-%d'

N_A = "null"

NOT_APPL = "N_A"

LOGS = "logs"
LOGS_WATCH = "logs-watch"
DATA = "data"
DATA_WATCH = "data-watch"

PREV_SLEEP_QUE_ID = "key_prev_sleep_que"
PREV_WAKE_QUE_ID = "key_prev_wake_que"

UPLOAD_MGR_SVC = "MicroTUploadManagerService.log.csv"
UPLOAD_MGR_SVC_NOTES = "MicroTUploadManagerServiceNotes.log.csv"
WATCH_PROMPT_ACTIVITY = "Watch-PromptActivity.log.csv"
WEAR_NOTE_SENDER = "WearNoteSender.log.csv"
PROMPT_RESP = "PromptResponses.log.csv"
BURST_SCHEDULE_MGR = "SuperBurstScheduleManager.log.csv"
PHONE_NOTIF_COUNT = "NotificationCounts.csv"
NOTIF_MGR_SVC = "NotificationManager.log.csv"
PHONE_APP_EVENTS = "AppEventCounts.csv"
STEP_COUNTER = "StepCounterService.csv"
ACTIVITIES_DETECTED = "ActivityDetected.csv"
WATCH_ACCEL_SUMMARY = "Watch-AccelSampling.log.csv"
PHONE_ACCEL_SUMMARY = "AccelSampling.log.csv"
WATCH_MISC_LOGGER = "Watch-MiscLogger.log.csv"
WATCH_SENSOR_MGR = "Watch-SensorManagerService.log.csv"
PHONE_SYS_BROADCAST = "SystemBroadcastReceiver.log.csv"
WATCH_POWER_CONN_NOTES = "Watch-PowerConnectionReceiverNotes.log.csv"
PHONE_GPS = "GPS.csv"
WATCH_SYS_BROADCAST_NOTES = "Watch-TimeStudyWearBroadcastReceiverNotes.log.csv"
WATCH_ARBIT_LOG = "Watch-TimeStudyArbitrater.log.csv"
WATCH_SAMPLING_RATE = "Watch-SamplingRate.log.csv"
WATCH_WAKE_SRVC = "Watch-WearableWakefulService.log.csv"
WATCH_COLLECTED_SAVED = "watch_data_collected.txt"
CLUSTER_LOG_FILE = "ClusterMaker.log.csv"

reprompt_col = 0
date_format = '%Y-%m-%d'
quest_resp_time_mean = 0.0
ques_resp_time_med = 0.0
ques_resp_time_without_latency_mean = 0.0
ques_resp_time_without_latency_med = 0.0


def parse_upload_manager(phone_upload_mgr_service):
    # print("Parsing upload manager notes")
    # file_path = temp_date_path + sep + UPLOAD_MGR_SVC_NOTES
    # print("File path: " + file_path)
    snoozed = N_A
    burst_mode = N_A
    start_date = N_A
    end_date = N_A
    current_sleep_time = N_A
    current_wake_time = N_A
    next_wake_time = N_A
    # if path.exists(file_path):
    if phone_upload_mgr_service is not N_A:
        # print("NOT NAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # print(phone_upload_mgr_service)
        # with open(file_path) as inp:
        #     csvreader = csv.reader(fix_nulls(inp))
        # phone_upload_mgr_service = phone_upload_mgr_service.replace('\0', '')
        csvreader = csv.reader(phone_upload_mgr_service.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            note = row[4]
            if re.match(r"\ABURST mode", note):
                burst_status = note.split("|")[1].strip()
                burst_mode = "BURST" if burst_status == "true" else "TIME"
                # print("Burst status: " + burst_status)
            elif re.match(r"\AStart date", note):
                start_date = note.split("|")[1].strip()
                # print("Start date: " + start_date)
            elif re.match(r"\AEnd date", note):
                end_date = note.split("|")[1].strip()
            elif re.match(r"\ASnooze", note):
                snoozed_status = note.split("|")[1].strip()
                snoozed = "Yes" if snoozed_status == "true" else "No"
            elif re.match(r"\ACurrent sleep time", note):
                current_sleep_time = note.split("|")[1].strip()
            elif re.match(r"\ACurrent wake time", note):
                current_wake_time = note.split("|")[1].strip()
            elif re.match(r"\ANext wake time", note):
                next_wake_time = note.split("|")[1].strip()
    try:
        datetime.strptime(start_date, date_format)
    except ValueError as e:
        print(str(e))
        start_date = N_A
    try:
        datetime.strptime(end_date, date_format)
    except ValueError as e:
        print(str(e))
        end_date = N_A
    return snoozed, burst_mode, start_date, end_date, current_sleep_time, \
           current_wake_time, next_wake_time


def get_sleep_wake_time_changes(phone_upload_mgr_notes_file):
    # print("Getting the number of times sleep and wake times have changed in that day")
    # file_path = temp_date_path + sep + UPLOAD_MGR_SVC_NOTES
    sleep_time_list = []
    wake_time_list = []
    # if path.exists(file_path):
    if phone_upload_mgr_notes_file is not N_A:
        # with open(file_path) as inp:
        #     csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(phone_upload_mgr_notes_file.splitlines(), delimiter=',')
        for row in csvreader:
            note = row[4]
            if re.match(r"\ACurrent sleep time", note):
                current_sleep_time = note.split("|")[1].strip()
                sleep_time_list.append(current_sleep_time)
            elif re.match(r"\ACurrent wake time", note):
                current_wake_time = note.split("|")[1].strip()
                wake_time_list.append(current_wake_time)
        sleep_set = set(sleep_time_list)
        wake_set = set(wake_time_list)
        sleep_time_changes = len(sleep_set) - 1
        wake_time_changes = len(wake_set) - 1
        return sleep_time_changes, wake_time_changes
    else:
        return N_A, N_A


def get_dnd_dur(date, phone_upload_mgr_notes_file, watch_misc_file):
    # print("Get watch and phone dnd duration")
    # phone_file_path = temp_date_path + sep + UPLOAD_MGR_SVC_NOTES
    # watch_file_path = temp_date_path + sep + WATCH_MISC_LOGGER
    phone_log_time_format = "%Y-%m-%d %H:%M:%S.%f"
    watch_log_time_format = "%a %b %d %H:%M:%S %Y"
    phone_dnd_dur, watch_dnd_dur = 0, 0
    midnight_past = date.replace(hour=0, minute=0, second=0,
                                 microsecond=0)
    # print("Midnight past: ", datetime.strftime(midnight_past,
    #                                            "%Y-%m-%d %H:%M:%S.%f %Z"))
    midnight_future = float((midnight_past + timedelta(days=1)).timestamp())
    midnight_past = float(midnight_past.timestamp())
    # print("Day: ", midnight_past.__str__(), "->", midnight_future)
    # print("Day length (s): ", (midnight_future - midnight_past))

    # if path.exists(phone_file_path):
    if phone_upload_mgr_notes_file is not N_A:
        # with open(phone_file_path) as inp:
        dnd_start_time = midnight_past
        dnd_end_time = midnight_future
        dnd_status = False
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(phone_upload_mgr_notes_file.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            note = row[4]
            if re.match(r"\ADND status", note):
                # print("Current aggregated phone dnd time(s):",
                #       phone_dnd_dur)
                dnd_val = int(note.split("|")[1].strip())
                # print("ROW TO PARSE: " + str(row[0]))
                # print("PARSING " + str(row[0][:23]))
                log_time = float(datetime.strptime(row[0][:23],
                                                   phone_log_time_format).timestamp())
                if dnd_val > 1:
                    # print("DND STARTS at: " + str(row[0]))
                    if not dnd_status:
                        dnd_start_time = log_time
                    dnd_status = True
                else:
                    if dnd_status:
                        # print("DND ENDS at: " + str(row[0]))
                        dnd_end_time = log_time
                        phone_dnd_dur += dnd_end_time - dnd_start_time
                        # print("DND DURATION: " + str(phone_dnd_dur))
                    dnd_status = False
        if dnd_status:
            phone_dnd_dur += midnight_future - dnd_start_time
            # print("FINAL DND DURATION: " + str(phone_dnd_dur))
    else:
        # print("File does not exist:", phone_file_path)
        phone_dnd_dur = N_A
    # if path.exists(watch_file_path):
    if watch_misc_file is not N_A:
        # with open(watch_file_path) as inp:
        dnd_start_time = midnight_past
        dnd_end_time = midnight_future
        dnd_status = False
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(watch_misc_file.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            if len(row) >= 3 and row[2] == "DND":
                # print("Current aggregated watch dnd time(s):",
                #       watch_dnd_dur)
                dnd_val = int(row[3].strip())
                # print("WATCH ROW TO PARSE: " + str(row[0]))
                # print("WATCH PARSING " + str(row[0][:19]) + " " + row[0][-4:])
                log_time = float(datetime.strptime(row[0][:19] + " " + row[0][-4:],
                                                   watch_log_time_format).timestamp())
                if dnd_val > 1:
                    if not dnd_status:
                        dnd_start_time = log_time
                    dnd_status = True
                else:
                    if dnd_status:
                        dnd_end_time = log_time
                        watch_dnd_dur += dnd_end_time - dnd_start_time
                    dnd_status = False
        if dnd_status:
            watch_dnd_dur += midnight_future - dnd_start_time
    else:
        # print("File does not exist:", watch_file_path)
        watch_dnd_dur = N_A
    # print("Final phone, watch dnd times (s):", phone_dnd_dur, ",", watch_dnd_dur)
    if phone_dnd_dur != N_A:
        phone_dnd_dur = int(phone_dnd_dur / 60)
    if watch_dnd_dur != N_A:
        watch_dnd_dur = int(watch_dnd_dur / 60)
    return phone_dnd_dur, watch_dnd_dur


def get_off_dur(date, phone_sys_file, watch_arbit_file, watch_power_notes_file):
    # print("Get phone and watch off duration")
    # phone_file_path = temp_date_path + sep + PHONE_SYS_BROADCAST
    # watch_file_path = temp_date_path + sep + WATCH_ARBIT_LOG
    # watch_file_path_2 = temp_date_path + sep + WATCH_POWER_CONN_NOTES
    phone_log_time_format = "%Y-%m-%d %H:%M:%S.%f"
    watch_log_time_format = "%a %b %d %H:%M:%S %Y"
    phone_off_dur, watch_off_dur, watch_off_dur_shut = 0, 0, 0
    watch_decline = False
    PHONE_GAP_ALLOWED_SECS, WATCH_GAP_ALLOWED_SECS = 5 * 60, 40 * 60
    midnight_past = date.replace(hour=0, minute=0, second=0,
                                 microsecond=0)
    # print("Midnight past: ", datetime.strftime(midnight_past,
    #                                            "%Y-%m-%d %H:%M:%S.%f %Z"))
    midnight_future = float((midnight_past + timedelta(days=1)).timestamp())
    midnight_past = float(midnight_past.timestamp())
    # print("Day: ", midnight_past.__str__(), "->", midnight_future)
    # print("Day length (s): ", (midnight_future - midnight_past))
    if phone_sys_file is not N_A:
        # if path.exists(phone_file_path):
        # with open(phone_file_path, encoding='utf-8') as inp:
        phone_off_start = midnight_past
        phone_off_end = midnight_future
        phone_on = False
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(phone_sys_file.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            try:
                note = row[4]
            except:
                continue
            # print("PHONE OFF ROW TO PARSE: " + str(row[0]))
            # print("PHONE OFF PARSING " + str(row[0][:23]))
            try:
                log_time = float(datetime.strptime(row[0][:23],
                                                   phone_log_time_format).timestamp())
            except:
                continue
            if note == "android.intent.action.BOOT_COMPLETED":
                if not phone_on:
                    phone_off_end = log_time
                    # print("PHONE REBOOT TIME: " + str(phone_off_end))
                    phone_off_dur += phone_off_end - phone_off_start
                phone_on = True
            elif note == "android.intent.action.ACTION_SHUTDOWN":
                phone_off_start = log_time
                # print("PHONE OFF TIME: " + str(phone_off_start))
                phone_on = False
        if not phone_on and phone_off_start != midnight_past:
            phone_off_dur += phone_off_end - phone_off_start
    else:
        # print("File does not exist:", phone_file_path)
        phone_off_dur = N_A
    if watch_arbit_file is not N_A:
        # if path.exists(watch_file_path):
        # with open(watch_file_path, encoding='utf-8') as inp:
        watch_last_on = midnight_past
        log_decline_time = midnight_past
        log_incr_time = midnight_future
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(watch_arbit_file.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            # print("ROW is: " + str(row[2]))
            if len(row) >= 2 and "Battery percentage: " in row[2]:
                # print("ROW is: " + str(row))
                # print("WATCH ROW TO PARSE: " + str(row[0]))
                # print("WATCH OFF PARSING " + str(row[0][:19]) + " " + row[0][-4:])
                battery_perc = row[2].split(":")[-1]
                battery_perc = battery_perc.lstrip()
                # print("BATTERY after split: " + str(battery_perc))
                try:
                    battery_perc = float(battery_perc)
                    # print("BATTERY after int: " + str(battery_perc))
                except:
                    continue

                try:
                    log_time = float(datetime.strptime(row[0][:19] + " " + row[0][-4:],
                                                       watch_log_time_format).timestamp())
                except:
                    continue
                # print("WATCH LOG TIME: " + str(log_time) + "," + " WATCH LAST ON: " + str(watch_last_on) + ",
                # FOR ROW: " + str(row[0])) print("WATCH LOG TIME: " + str(log_time))
                if battery_perc <= 10 and watch_decline is False:
                    # print("BATTERY DECLINE STARTED")
                    watch_decline = True
                    log_decline_time = log_time
                    # gap = log_time - watch_last_on
                    # watch_off_dur += gap
                    # watch_last_on = log_time

                if battery_perc > 10 and watch_decline is True:
                    # print("BATTERY IS INCREASING")
                    watch_decline = False
                    log_incr_time = log_time
                    gap = log_incr_time - log_decline_time
                    # print("WATCH BATTERY OFF GAP: " + str(gap))
                    watch_off_dur += gap
                    # print("WATCH TOTAL OFF TIME: " + str(watch_off_dur))
                    # gap = log_time - watch_last_on
                    # watch_off_dur += gap
        if watch_decline is True:
            gap = midnight_future - log_decline_time
            watch_off_dur += gap
    else:
        # print("File does not exist:", watch_file_path)
        watch_off_dur = N_A
    if watch_power_notes_file is not N_A:
        # if path.exists(watch_file_path_2):
        #     with open(watch_file_path_2, encoding='utf-8') as inp:
        watch_last_on = midnight_past
        watch_off_start_2 = midnight_past
        watch_off_end_2 = midnight_future
        watch_on = True
        first_battery_change = True
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(watch_power_notes_file.splitlines(), delimiter=',')
        # print("POWER FILE READING: " + str(watch_file_path_2))
        for row in csvreader:
            # print("ROW::::::::::")
            # print(str(row))
            try:
                note = row[2]
            except:
                continue
            try:
                log_time = float(datetime.strptime(row[0][:19] + " " + row[0][-4:],
                                                   watch_log_time_format).timestamp())
            except:
                continue
            if note == "android.intent.action.ACTION_SHUTDOWN | true":
                if watch_on:
                    # print("WATCH SHUT DOWN AT: " + str(row[0]))
                    watch_off_start_2 = log_time
                    watch_on = False
            elif note == "android.intent.action.BATTERY_CHANGED | true":
                if not watch_on:
                    # print("WATCH RESTARTED AT: " + str(row[0]))
                    watch_off_end_2 = log_time
                    watch_off_dur_shut += watch_off_end_2 - watch_off_start_2
                    # print("WATCH OFF DUR SHUT: " + str(watch_off_dur_shut / 60))
                    watch_on = True
                    first_battery_change = False
                elif watch_on and first_battery_change:
                    # print("FIRST BATTERY CHANGE OF THE DAY: " + str(row[0]))
                    watch_off_end_2 = log_time
                    watch_off_dur_shut += watch_off_end_2 - watch_off_start_2
                    first_battery_change = False
        if not watch_on and watch_off_start_2 != midnight_past:
            watch_off_dur_shut += midnight_future - watch_off_start_2
    else:
        watch_off_dur_shut = N_A

    # print("Final aggregated phone, watch off times (s):",
    #       str(phone_off_dur), ",", str(watch_off_dur), ", ", str(watch_off_dur_shut))
    if phone_off_dur != N_A:
        phone_off_dur = int(phone_off_dur / 60)
    if watch_off_dur != N_A:
        watch_off_dur = int(watch_off_dur / 60)
    if watch_off_dur_shut != N_A:
        watch_off_dur_shut = int(watch_off_dur_shut / 60)
    return phone_off_dur, watch_off_dur, watch_off_dur_shut


def get_charging_stats_phone_unlocks(date, phone_sys_file, watch_power_notes_file):
    # print("Get watch and phone charging and unlocking stats")
    # phone_file_path = temp_date_path + sep + PHONE_SYS_BROADCAST
    # watch_file_path = temp_date_path + sep + WATCH_POWER_CONN_NOTES
    phone_log_time_format = "%Y-%m-%d %H:%M:%S.%f"
    watch_log_time_format = "%a %b %d %H:%M:%S %Y"
    phone_charging_count, phone_charging_dur, watch_charging_count, \
    watch_charging_dur = 0, 0, 0, 0
    phone_unlock_count = 0
    midnight_past = date.replace(hour=0, minute=0, second=0,
                                 microsecond=0)
    # print("Midnight past: ", datetime.strftime(midnight_past,
    #                                            "%Y-%m-%d %H:%M:%S.%f %Z"))
    midnight_future = float((midnight_past + timedelta(days=1)).timestamp())
    midnight_past = float(midnight_past.timestamp())
    # print("Day: ", midnight_past.__str__(), "->", midnight_future)
    # print("Day length (s): ", (midnight_future - midnight_past))
    if phone_sys_file is not N_A:
        # if path.exists(phone_file_path):
        #     with open(phone_file_path) as inp:
        charging_start_time = midnight_past
        charging_end_time = midnight_future
        charging_status = False
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(phone_sys_file.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            try:
                note = row[4]
            except:
                continue
            # print("PHONE OFF ROW TO PARSE: " + str(row[0]))
            # print("PHONE OFF PARSING " + str(row[0][:23]))
            try:
                log_time = float(datetime.strptime(row[0][:23],
                                                   phone_log_time_format).timestamp())
            except:
                continue
            if note == "android.intent.action.ACTION_POWER_CONNECTED":
                # print("CONNECTED at: " + str(row[0]))
                phone_charging_count += 1
                # print("Current aggregated phone charging time(s):",
                #       phone_charging_time)
                if not charging_status:
                    charging_start_time = log_time
                charging_status = True
            elif note == "android.intent.action.ACTION_POWER_DISCONNECTED":
                # print("DISCONNECTED at: " + str(row[0]))
                charging_end_time = log_time
                phone_charging_dur += charging_end_time - charging_start_time
                # print("CHARGING DURATION: " + str(phone_charging_dur))
                charging_start_time = log_time
                charging_status = False
            elif note == "android.intent.action.USER_PRESENT":
                phone_unlock_count += 1
        if charging_status:
            # print("CHARGING START: " + str(charging_start_time) + " CHARGING END: " + str(charging_end_time))
            phone_charging_dur += midnight_future - charging_start_time
            # print("FINAL CHARGING DURATION: " + str(phone_charging_dur))
    else:
        # print("File does not exist:", phone_file_path)
        phone_charging_dur = N_A
        phone_charging_count = N_A
        phone_unlock_count = N_A
    if watch_power_notes_file is not N_A:
        # if path.exists(watch_file_path):
        #     with open(watch_file_path) as inp:
        charging_start_time = midnight_past
        charging_end_time = midnight_future
        charging_status = "false"
        # csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(watch_power_notes_file.splitlines(), delimiter=',')
        for row in csvreader:
            # print("Row: ", row)
            try:
                note = row[2]
            except:
                continue
            if re.match(r"\ACharging", note):
                # print("Current aggregated watch charging time(s):",
                #       watch_charging_time)
                charging_status = note.split("|")[1].strip()
                # print("WATCH CHARGING AT: " + str(row[0]) + " " + str(charging_status))
                charging_val = True if "true" in charging_status else False
                # print("CHARGING VAL: " + str(charging_val))
                # charging_status = bool(charging_status)
                # print("WATCH ROW TO PARSE: " + str(row[0]))
                # print("WATCH PARSING " + str(row[0][:19]) + " " + row[0][-4:])
                log_time = float(datetime.strptime(row[0][:19] + " " + row[0][-4:],
                                                   watch_log_time_format).timestamp())
                if charging_val:
                    watch_charging_count += 1
                    # print("CHARGING STATUS: " + charging_status)
                    if charging_status == "true":
                        # watch_charging_count += 1
                        charging_start_time = log_time
                        # print("CHARGING START TIME: " + str(charging_start_time))
                    charging_status = "true"
                else:
                    charging_end_time = log_time
                    # print("CHARGING END TIME: " + str(charging_end_time))
                    watch_charging_dur += charging_end_time - charging_start_time
                    charging_start_time = log_time
                    charging_status = "false"
        if "true" in charging_status:
            # print("WATCH CHARGING CONTINUED TILL MIDNIGHT")
            watch_charging_dur += midnight_future - charging_start_time
    else:
        # print("File does not exist:", watch_file_path)
        watch_charging_dur = N_A
        watch_charging_count = N_A
    # print("Final aggregated phone, watch charging times (s):", phone_charging_dur, ",", watch_charging_dur)
    if phone_charging_dur != N_A:
        phone_charging_dur = int(phone_charging_dur / 60)
    if watch_charging_dur != N_A:
        watch_charging_dur = int(watch_charging_dur / 60)
    return phone_charging_count, phone_charging_dur, \
           watch_charging_count, watch_charging_dur, \
           phone_unlock_count


def get_phone_loc_data_mins(gps_file):
    # file_path = temp_date_path + sep + PHONE_GPS
    all_data_points_timestamps = set()
    # if gps_reader is not N_A:
    # if path.exists(file_path):
    if gps_file is not N_A:
        # with open(file_path) as inp:
        #     csvreader = csv.reader(fix_nulls(inp))
        csvreader = csv.reader(gps_file.splitlines(), delimiter=',')
        for row in csvreader:
            all_data_points_timestamps.add(row[1])
        return len(all_data_points_timestamps)
    else:
        return N_A


def get_sleep_duration(date, phone_upload_mgr_notes_file):
    # print("Parsing upload manager notes for sleep duration")
    sleep_wake_time_format = "%Y-%m-%d %H:%M:%S"
    log_time_format = "%Y-%m-%d %H:%M:%S.%f"
    # file_path = temp_date_path + sep + UPLOAD_MGR_SVC_NOTES
    # if path.exists(file_path):
    if phone_upload_mgr_notes_file is not N_A:
        # csvreader = csv.reader(phone_upload_mgr_notes_file.splitlines(), delimiter=',')
        df = pd.read_csv(StringIO(phone_upload_mgr_notes_file), header=None, usecols=[i for i in range(5)])
        # print(df.head())
        df = df.drop([1, 2, 3], 1)
        # print("Print head of upload manager notes")
        # print(df.head(6))
        df = df.loc[df[4].str.match(r".*time")]
        tz = df.iloc[0, 0][-3:]
        # tz_end = df.iloc[0, len()]
        # print("TZ TZ TZ TZ TZ TZ: ", str(tz))
        # print("Timezone: ", timezone)
        df[0] = df[0].apply(lambda x: float(datetime.strptime(x[:-4],
                                                              log_time_format).timestamp()))
        # df[4] = df[4].apply(lambda x: x.replace(tz, ""))
        df[4] = df[4].apply(lambda x: x[:-3].strip())
        df_curr_sleep = df.loc[df[4].str.match(r"Current sleep.*")]
        df_curr_wake = df.loc[df[4].str.match(r"Current wake.*")]
        # print(df.head(6))
        df_curr_sleep[4] = df_curr_sleep[4].apply(lambda x: x.split("|")[
            1].strip())
        # print("TEST TEST TEST 1")
        # print(df_curr_sleep.head())
        df_curr_wake[4] = df_curr_wake[4].apply(lambda x: x.split("|")[
            1].strip())
        # print("TEST TEST TEST 2")
        # print(df_curr_wake.head())
        df_curr_sleep[4] = df_curr_sleep[4].apply(lambda x: float(
            datetime.strptime(x[:], sleep_wake_time_format).timestamp()))
        df_curr_wake[4] = df_curr_wake[4].apply(lambda x: float(
            datetime.strptime(x[:], sleep_wake_time_format).timestamp()))
        # print(df_curr_sleep.head(6))
        # print(df_curr_wake.head(6))
        midnight_past = date.replace(hour=0, minute=0, second=0,
                                     microsecond=0)
        # print("Midnight past: ", datetime.strftime(midnight_past, "%Y-%m-%d %H:%M:%S.%f %Z"))
        midnight_future = float((midnight_past + timedelta(days=1)).timestamp())
        midnight_past = float(midnight_past.timestamp())
        # print("Day: ", midnight_past.__str__(), "->", midnight_future)
        # print("Day length (s): ", (midnight_future - midnight_past))
        tot_wake_dur = 0
        current_index = 0
        total_entries = len(df_curr_sleep)
        # print("Sleep wake entries count: ", total_entries)
        awake = True
        data_before_sleep_wake_update = True
        log_time_list = []
        curr_sleep_list = []
        curr_wake_list = []
        awake_start_time = midnight_past
        awake_end_time = midnight_future
        for row in df_curr_sleep.itertuples():
            log_time_list.append(row[1])
            curr_sleep_list.append(row[2])
        for row in df_curr_wake.itertuples():
            curr_wake_list.append(row[2])
        while current_index < total_entries:
            # print(tup)
            log_time = log_time_list[current_index]
            curr_sleep_time = curr_sleep_list[current_index]
            curr_wake_time = curr_wake_list[current_index]
            awake_end_time = min(curr_sleep_time, awake_end_time)
            # print("Time: ", datetime.fromtimestamp(log_time), ":",
            #       datetime.fromtimestamp(curr_sleep_time), ":",
            #       datetime.fromtimestamp(curr_wake_time))
            # print("Before sleep time: ",
            #       datetime.fromtimestamp(awake_start_time), "->",
            #       datetime.fromtimestamp(awake_end_time))
            if log_time > curr_sleep_time:
                # print("Log time > Curr sleep")
                # print("Awake: ", str(awake))
                if awake:
                    awake = False
                    tot_wake_dur += max(awake_end_time - awake_start_time, 0)
            else:
                # print("Log time < Curr sleep")
                if not awake:
                    awake = True
                awake_start_time = max(midnight_past, curr_wake_time)
            awake_end_time = min(curr_sleep_time, midnight_future)
            current_index += 1
            # print("After iteration: ",
            #       datetime.fromtimestamp(awake_start_time), "->",
            #       datetime.fromtimestamp(awake_end_time))
            # print("Total awake duration(s): ", tot_wake_dur)
        if awake:
            tot_wake_dur += awake_end_time - awake_start_time
        #     print("Total wake duration(s) after while loop: ", tot_wake_dur)
        # print("Finally, total awake time(s): ", tot_wake_dur)
        # print("###################################")
        sleep_dur = (24 * 60 * 60 - tot_wake_dur) / (60 * 60)
        return round(sleep_dur, 2)
    else:
        return N_A


def convert_offset_ms(offset):
    # print("Offset is: " + str(offset))
    offset = offset.split('GMT')[1]
    sign = offset[0]
    offset = offset[1:]
    hour, minute = offset.split(":")
    updated_time = sign + str((int(hour) * 3600 + int(minute) * 60) * 1000)
    updated_time = float(updated_time)
    return updated_time


def get_retrospective_sleep_wake_times(prompt_response_file):
    # print("Getting retrospective sleep wake times")
    exclude_status = ['NeverStarted', 'NeverPrompted', 'Started', 'Overwritten']
    exclude_prompt_types = ['EMA_Micro', 'None_Sleep', 'None_Empty', 'Trivia_EMA_Micro',
                            'CS_EMA_Micro', 'CS_EMA', 'null']
    # file_path = temp_date_path + sep + PROMPT_RESP
    prev_sleep_time = 0
    prev_wake_time = 0
    responses = []
    # if path.exists(file_path):
    if prompt_response_file is not N_A:
        # with open(file_path) as resp_csv:
        #     csv_reader = csv.reader(resp_csv, delimiter=",")
        csv_reader = csv.reader(prompt_response_file.splitlines(), delimiter=",")
        for row in csv_reader:
            # print(row[-1])
            # print("UTC OFFSET IS: " + str(utc_offset))
            if row[1] not in exclude_prompt_types and row[10] not in exclude_status:
                # print("Row is: \n" + str(row))
                utc_offset = row[8]
                # print("ORIGINAL OFFSET: " + str(utc_offset))
                try:
                    utc_offset = convert_offset_ms(utc_offset)
                    if row[33] == PREV_SLEEP_QUE_ID:
                        prev_sleep_time = row[35]
                        # print("Prev_sleep_time: " + str(prev_sleep_time))
                        prev_sleep_time = float(prev_sleep_time) + utc_offset
                        prev_sleep_time = datetime.utcfromtimestamp(prev_sleep_time / 1000)
                    if row[37] == PREV_WAKE_QUE_ID:
                        prev_wake_time = row[39]
                        # print("Prev_wake_time: " + str(prev_wake_time))
                        prev_wake_time = float(prev_wake_time) + utc_offset
                        prev_wake_time = datetime.utcfromtimestamp(prev_wake_time / 1000)
                except:
                    continue
        # print("Final sleep and wake time retrospectively: \n" + str(prev_sleep_time) + ", " + str(prev_wake_time))
        # print(responses)
        # getResponseLatency(temp_date_path)
        return prev_sleep_time, prev_wake_time
    else:
        return N_A, N_A


def parse_prompt_responses(is_burst_day, prompt_response_file):
    # print("Parsing prompt responses")
    # file_path = temp_date_path + sep + PROMPT_RESP
    all_resp_time_mean = all_resp_time_med = sleep_resp_time_mean = \
        burst_resp_time_mean = burst_resp_time_med = eod_resp_time_mean = \
        eod_resp_time_med = uema_resp_time_mean = uema_resp_time_med = sleep_prompted = \
        sleep_started = sleep_completed = sleep_first_prompt = sleep_reprompt = \
        sleep_completed_firstPrompt = sleep_completed_reprompt = \
        burst_ema_prompted = burst_ema_original_prompted = burst_ema_started = burst_ema_completed = burst_ema_firstPrompts = \
        burst_ema_reprompts = burst_ema_completed_firstPrompts = burst_ema_completed_reprompts = \
        eod_prompted = eod_original_prompted = eod_started = eod_completed = eod_firstPrompts = \
        eod_reprompts = eod_completed_firstPrompts = eod_completed_reprompts = \
        uema_prompted = uema_completed = uema_partial_completed = response_latency_mean = response_latency_med = \
        general_latency_mean = general_latency_med = set_types_prompted = skip_count = \
        uema_cs_prompted = uema_cs_completed = uema_trivia_prompted = uema_trivia_completed = N_A

    # if path.exists(file_path):
    if prompt_response_file is not N_A:
        # Read the prompt response file up to 32nd column
        resp_file = pd.read_csv(StringIO(prompt_response_file), header=None, usecols=[i for i in range(33)])
        # print("Printing head of the data frame")
        # print(resp_file.head(6))
        # Add overall prompt response time column to the data frame
        resp_file = add_final_response_time(resp_file, prompt_response_file)
        skip_count = get_total_skipped(prompt_response_file)
        # uema_validated_num = get_uema_validation(temp_date_path)
        # print("Resp file has columns: " + str(len(resp_file.columns)))
        # print("Response latency values: " + str(quest_resp_time_mean) + ", " + str(ques_resp_time_med))
        # print("Response times per question without latency are: " + str(ques_resp_time_without_latency_mean) +
        #       ", " + str(ques_resp_time_without_latency_med))
        # Slice out uEMA responses as separate data frame
        u_df = get_micro_ema_dataframe(resp_file)
        # print("u_df has columns: " + str(len(u_df.columns)))
        # Slice out phoneEMA responses as separate data frame
        p_df = get_phone_ema_dataframe(resp_file)
        set_types_prompted = get_set_count_list(p_df)
        # print("p_df has columns: " + str(len(p_df.columns)))
        all_resp_time_mean, all_resp_time_med, sleep_resp_time_mean, \
        burst_resp_time_mean, burst_resp_time_med, eod_resp_time_mean, \
        eod_resp_time_med = get_phone_response_times(p_df, is_burst_day)
        uema_resp_time_mean, uema_resp_time_med = get_watch_response_times(u_df, is_burst_day)

        response_latency_mean, response_latency_med, general_latency_mean, \
        general_latency_med = get_response_latency_values(p_df)

        sleep_prompted, sleep_started, sleep_completed, sleep_first_prompt, \
        sleep_reprompt, sleep_completed_firstPrompt, sleep_completed_reprompt, \
        burst_ema_prompted, burst_ema_original_prompted, burst_ema_started, \
        burst_ema_completed, burst_ema_firstPrompts, \
        burst_ema_reprompts, burst_ema_completed_firstPrompts, burst_ema_completed_reprompts, \
        eod_prompted, eod_original_prompted, eod_started, eod_completed, \
        eod_firstPrompts, eod_reprompts, eod_completed_firstPrompts, \
        eod_completed_reprompts = get_phone_prompt_counts(
            resp_file, is_burst_day)
        uema_prompted, uema_completed, uema_partial_completed, uema_cs_prompted, uema_cs_completed, \
        uema_trivia_prompted, uema_trivia_completed = get_watch_prompt_counts(u_df, is_burst_day)
    else:
        print("File not found")
    return all_resp_time_mean, all_resp_time_med, sleep_resp_time_mean, \
           burst_resp_time_mean, burst_resp_time_med, eod_resp_time_mean, \
           eod_resp_time_med, uema_resp_time_mean, uema_resp_time_med, \
           response_latency_mean, response_latency_med, general_latency_mean, \
           general_latency_med, \
           quest_resp_time_mean, ques_resp_time_med, \
           ques_resp_time_without_latency_mean, ques_resp_time_without_latency_med, \
           sleep_prompted, sleep_started, sleep_completed, sleep_first_prompt, \
           sleep_reprompt, sleep_completed_firstPrompt, sleep_completed_reprompt, \
           burst_ema_prompted, burst_ema_original_prompted, burst_ema_started, burst_ema_completed, \
           burst_ema_firstPrompts, burst_ema_reprompts, burst_ema_completed_firstPrompts, \
           burst_ema_completed_reprompts, eod_prompted, eod_original_prompted, eod_started, eod_completed, eod_firstPrompts, \
           eod_reprompts, eod_completed_firstPrompts, eod_completed_reprompts, \
           set_types_prompted, skip_count, uema_prompted, uema_completed, uema_partial_completed, \
           uema_cs_prompted, uema_cs_completed, uema_trivia_prompted, uema_trivia_completed


def get_non_microt_notif_count(notif_count_file):
    # print("Parsing notif counts")
    # file_path = temp_date_path + sep + PHONE_NOTIF_COUNT
    non_microt_notif_count = N_A
    # print(file_path)
    # if path.exists(file_path):
    if notif_count_file is not N_A:
        try:
            notif_df = pd.read_csv(StringIO(notif_count_file), header=None, usecols=[0, 1, 2, 3, 4])
        except:
            return N_A
        # print("Print head of the notification counts")
        # print(notif_df.head(6))
        non_microt_df = notif_df.loc[notif_df[4] != "mhealth.neu.edu.microT"]
        non_microt_notif_count = non_microt_df.shape[0]
    return non_microt_notif_count


def get_unqiue_apps_count(app_count_file):
    # print("Parsing app events")
    # file_path = temp_date_path + sep + PHONE_APP_EVENTS
    unique_apps_count = "null"
    # print(file_path)
    # if path.exists(file_path):
    if app_count_file is not N_A:
        try:
            apps_df = pd.read_csv(StringIO(app_count_file), header=None)
        except:
            return N_A
        # print("Print head of the app events")
        # print(apps_df.head(6))
        apps_fg_df = apps_df.loc[apps_df[5] == "MOVE_TO_FOREGROUND"]
        unique_apps_count = len(apps_fg_df[3].unique())
        return unique_apps_count
    else:
        return N_A


def parse_step_counter(step_count_file):
    # print("Parsing step counts")
    # file_path = temp_date_path + sep + STEP_COUNTER
    # print(file_path)
    daily_steps = "null"
    # if path.exists(file_path):
    if step_count_file is not N_A:
        # print("Steps file exists")
        try:
            step_file = pd.read_csv(StringIO(step_count_file), header=None)
        except:
            return N_A
        # print("Print head of the step counts")
        # print(step_file.head(6))
        daily_steps = step_file[1].sum()
        return daily_steps
    else:
        return N_A


def parse_watch_accel_summary(watch_sampling_file, no_motion_threshold=90):
    # print("parsing Watch Accel Summary")
    # file_path = temp_date_path + sep + WATCH_ACCEL_SUMMARY
    watch_motion_summary = N_A
    # if path.exists(file_path):
    if watch_sampling_file is not N_A:
        try:
            watch_summ_file = pd.read_csv(StringIO(watch_sampling_file), header=None, usecols=[0, 1, 2, 3, 4, 5, 6])
        except:
            return N_A
        watch_summ_file.dropna(inplace=True)
        watch_summ_file.reset_index(drop=True, inplace=True)
        watch_summ_file[0].replace('', np.nan, inplace=True)
        watch_summ_file[1].replace('', np.nan, inplace=True)
        watch_summ_file[2].replace('', np.nan, inplace=True)
        watch_summ_file[3].replace('', np.nan, inplace=True)
        watch_summ_file[4].replace('', np.nan, inplace=True)
        watch_summ_file[5].replace('', np.nan, inplace=True)
        watch_summ_file[6].replace('', np.nan, inplace=True)
        # watch_motion_summary = watch_summ_file[4].sum() + watch_summ_file[5].sum() + \
        #                        np.nansum(list(watch_summ_file[6]))
        cols = [4, 5, 6]
        watch_summ_file[cols] = watch_summ_file[cols].apply(pd.to_numeric, errors='coerce', axis=1)
        # watch_summ_file.to_csv(temp_date_path + sep + "Test.csv", index=False)
        watch_motion_summation = watch_summ_file[4] + watch_summ_file[5] + watch_summ_file[6]
        tm_list = []
        for i in range(watch_summ_file.shape[0]):
            # print("DECODING: " + str(watch_summ_file[2][i]))
            try:
                t = datetime.fromtimestamp(float(watch_summ_file[2][i]) / 1000)
            except:
                continue
            date_time_str = str(t.day) + ' ' + str(t.hour) + ':' + str(t.minute)
            date_time_obj = datetime.strptime(date_time_str, '%d %H:%M')
            tm_list.append(date_time_obj)
        try:
            watch_summ_file[7] = watch_motion_summation
            watch_summ_file[8] = tm_list
            df = watch_summ_file[[7, 8]].groupby([8]).mean()
            watch_motion_summary = sum(df[7] < no_motion_threshold)
            return watch_motion_summary
        except:
            return N_A
    else:
        return N_A


def read_responses_by_line(prompt_response_file):
    # print("reading responses by line")
    responses = []
    # file_path = temp_date_path + sep + PROMPT_RESP
    # with open(file_path) as resp_csv:
    #     csv_reader = csv.reader(resp_csv, delimiter=",")
    csv_reader = csv.reader(prompt_response_file.splitlines(), delimiter=",")
    for row in csv_reader:
        # print(row[-1])
        responses.append(row[-1])
    # print(responses)
    # getResponseLatency(temp_date_path)
    return responses


# Read the responses by line here and then generate: 1) a response latency
# column, a list of all the item response times for daily mean and median
# computations. May need separate functions
def get_quest_response_latency(prompt_response_file):
    # print("Calculating response latency and question-based response times")
    global quest_resp_time_mean
    global ques_resp_time_med
    global ques_resp_time_without_latency_mean
    global ques_resp_time_without_latency_med
    responses = []
    response_times = []
    response_times_without_latency = []
    general_latency = []
    response_latency = []
    status = ["NeverPrompted", "Overwritten"]
    prompt_type_exclude = ["EMA_micro", "Trivia_EMA_Micro", "CS_EMA_Micro", None, "null", ""]
    # file_path = temp_date_path + sep + PROMPT_RESP
    # with open(file_path) as resp_csv:
    #     csv_reader = csv.reader(resp_csv, delimiter=",")
    csv_reader = csv.reader(prompt_response_file.splitlines(), delimiter=",")
    for row in csv_reader:
        responses.append(row)
    for i in responses:
        qsRow = i
        # print("for row: ")
        # print(qsRow)
        diff_time = ""
        # try:
        #     print("It has the 36th item: " + str(qsRow[36]))
        # except:
        #     continue
        # print("Status is: " + qsRow[10])
        if qsRow[10] not in status and qsRow[1] not in prompt_type_exclude and len(qsRow) >= 37:
            promptCol = get_reprompt_number(qsRow)
            nQues = int(qsRow[31])
            nStart = 33
            # print("reprompted at: " + str(promptCol))
            # print("Prompt time is: " + qsRow[promptCol] + " First item response time: " + qsRow[36])
            # Get latency with respect to when the first question was answered
            # Check if the first question was even answered or not
            if "-1" not in qsRow[36]:
                # check against the reprompt time vs first prompt time
                # if it was answered in a reprompt, then compute diff_time from reprompt time only
                diff_time = (float(qsRow[36]) - float(qsRow[promptCol])) / 1000
                # First, check if there is any reprompt
                if promptCol != 9:
                    # Check if this item was already answered in the first prompt
                    if diff_time < 0:
                        # If so, then compute from the first prompt itself
                        diff_time = (float(qsRow[36]) - float(qsRow[9])) / 1000
                # also get a response time to the item from the first prompt time as well nevertheless
                gen_diff_time = (float(qsRow[36]) - float(qsRow[9])) / 1000
                # print("FOR THE FIRST ITEM: " + "Diff time is: " + str(diff_time) + ", gen_diff_time: " + str(
                #     gen_diff_time))
            else:
                # print("Not completed")
                diff_time = None
                gen_diff_time = None
                # print("Diff time is: " + str(diff_time) + ", gen_diff_time: " + str(gen_diff_time))
            # Now compute individual item response times
            # print("Now computing individual item response times")
            for j in range(0, nQues):
                # print("Getting item response times, starting: " + str(nStart))
                if "-1" not in qsRow[nStart + 3]:
                    # Check with the reprompt vs first prompt for partially completed prompts
                    if j == 0:
                        # Then check there was a reprompt or not
                        # print("For the first item")
                        quesTime = (float(qsRow[nStart + 3]) - float(qsRow[promptCol])) / 1000
                        # print("item response before reprompt check: " + str(quesTime))
                        if promptCol != 9:
                            # print("There was a reprompt")
                            # Check if this question was already answered before the reprompt
                            if quesTime < 0:
                                # print("Checking if the item was already answered before")
                                quesTime = (float(qsRow[nStart + 3]) - float(qsRow[9])) / 1000
                            # print("item response time: " + str(quesTime))
                    else:
                        quesTime = (float(qsRow[nStart + 3]) - float(qsRow[nStart - 1])) / 1000
                        ques_to_ques_time = (float(qsRow[nStart + 3]) - float(qsRow[nStart - 1])) / 1000
                        # print("Not the first item")
                        if promptCol != 9:
                            # print("There was a reprompt")
                            quesTime = (float(qsRow[nStart + 3]) - float(qsRow[nStart - 1])) / 1000
                            # Also collect individual item response times excluding the response time to the first
                            # prompt. This will prevent skewing of response times because of the first item response
                            # latencies
                            ques_to_ques_time = quesTime
                            fromReprompt = (float(qsRow[nStart + 3]) - float(qsRow[promptCol])) / 1000
                            # print("Diff from previous item: " + str(quesTime) + " diff from reprompt: " + str(
                            #     fromReprompt))
                            if quesTime > fromReprompt >= 0:
                                # print("Item answered after the reprompt")
                                quesTime = fromReprompt
                                ques_to_ques_time = quesTime
                        response_times_without_latency.append(ques_to_ques_time)
                    # print("item response time: " + str(quesTime))
                    response_times.append(quesTime)
                    # response_times_without_latency.append(ques_to_ques_time)
                    nStart = nStart + 4
                # else:
                #     print("Question not answered, exiting")
        else:
            # print("Not prompted")
            diff_time = None
            gen_diff_time = None
        response_latency.append(diff_time)
        general_latency.append(gen_diff_time)
    # print("response times for each item are: ")
    # print(response_times)
    quest_resp_time_mean = np.mean(response_times)
    ques_resp_time_med = np.median(response_times)
    ques_resp_time_without_latency_mean = np.mean(response_times_without_latency)
    ques_resp_time_without_latency_med = np.median(response_times_without_latency)
    if np.isnan(quest_resp_time_mean):
        quest_resp_time_mean = N_A
    else:
        quest_resp_time_mean = round(quest_resp_time_mean, 2)
    if np.isnan(ques_resp_time_med):
        ques_resp_time_med = N_A
    else:
        ques_resp_time_med = round(ques_resp_time_med, 2)
    if np.isnan(ques_resp_time_without_latency_mean):
        ques_resp_time_without_latency_mean = N_A
    else:
        ques_resp_time_without_latency_mean = round(ques_resp_time_without_latency_mean, 2)
    if np.isnan(ques_resp_time_without_latency_med):
        ques_resp_time_without_latency_med = N_A
    else:
        ques_resp_time_without_latency_med = round(ques_resp_time_without_latency_med, 2)
    # print("Mean item response time: " + str(quest_resp_time_mean) +
    #       ", Median item response time: " + str(ques_resp_time_med))
    # print(responseLatency)
    return response_latency, general_latency


def get_reprompt_number(qs_row):
    # print("Checking the reprompt number)")
    # prompt_col = 9
    if qs_row[13] != "-1":
        prompt_col = 13
    elif qs_row[19] != "-1":
        prompt_col = 19
    elif qs_row[22] != "-1":
        prompt_col = 22
    elif qs_row[25] != "-1":
        prompt_col = 25
    else:
        prompt_col = 9
    return prompt_col


def get_response_latency_values(df):
    # print("computing mean and median latencies")
    end = len(df.columns)
    response_latency_mean = round(df[end - 2].mean(), 2)
    if np.isnan(response_latency_mean) and df.shape[0] != 0:
        response_latency_mean = N_A
    response_latency_med = round(df[end - 2].median(), 2)
    if np.isnan(response_latency_med) and df.shape[0] != 0:
        response_latency_med = N_A
    general_latency_mean = round(df[end - 1].mean(), 2)
    if np.isnan(general_latency_mean) and df.shape[0] != 0:
        general_latency_mean = N_A
    general_latency_med = round(df[end - 1].median(), 2)
    if np.isnan(general_latency_med) and df.shape[0] != 0:
        general_latency_med = N_A
    return response_latency_mean, response_latency_med, \
           general_latency_mean, general_latency_med


def add_final_response_time(df, prompt_response_file):
    # print("Adding final response time")
    end = len(df.columns)
    # print("Ending is: " + str(end))
    df[end] = read_responses_by_line(prompt_response_file)
    df[end] = df[end].replace('-1', 'N/A')
    df[end] = pd.to_numeric(df[end], errors='coerce')
    # print("Updated end is: ", str(len(df.columns)))
    # print(df.head(6))
    # Select the right column to subtract from
    for i, row in df.iterrows():
        if row[13] != -1:
            # print("Reprompted at column 13: " + str(row[13]))
            try:
                df.loc[i, end + 1] = (df.loc[i, end] - df.loc[i, 13]) / 1000
            except TypeError:
                continue
            # row[end+1] = (row[end] - row[13])/1000
            # print("The diff is: " + str(row[end+1]))
        elif row[16] != -1:
            # print("Reprompted at column 16: " + str(row[16]))
            try:
                df.loc[i, end + 1] = (df.loc[i, end] - df.loc[i, 16]) / 1000
            except TypeError:
                continue
            # row[end + 1] = (row[end] - row[16])/1000
            # print("The diff is: " + str(row[end + 1]))
        elif row[19] != -1:
            # print("Reprompted at column 19: " + str(row[19]))
            try:
                df.loc[i, end + 1] = (df.loc[i, end] - df.loc[i, 19]) / 1000
            except TypeError:
                continue
            # row[end + 1] = (row[end] - row[19])/1000
            # print("The diff is: " + str(row[end + 1]))
        elif row[22] != -1:
            # print("Reprompted at column 22: " + str(row[22]))
            try:
                df.loc[i, end + 1] = (df.loc[i, end] - df.loc[i, 22]) / 1000
            except TypeError:
                continue
            # row[end + 1] = (row[end] - row[22])/1000
            # print("The diff is: " + str(row[end + 1]))
        elif row[25] != -1:
            # print("Reprompted at column 25: " + str(row[25]))
            try:
                df.loc[i, end + 1] = (df.loc[i, end] - df.loc[i, 25]) / 1000
            except TypeError:
                continue
            # row[end + 1] = (row[end] - row[25])/1000
            # print("The diff is: " + str(row[end + 1]))
        else:
            # print("No reprompts needed")
            try:
                df.loc[i, end + 1] = (df.loc[i, end] - df.loc[i, 9]) / 1000
            except TypeError:
                continue
            # row[end + 1] = (row[end] - row[9])/1000
            # print("The diff is: " + str(row[end + 1]))
        if df.loc[i, end + 1] is None:
            df.loc[i, end + 1] = N_A
    # print("End after column selection: ", str(len(df.columns)))
    # print(df.head(6))
    df[end + 2], df[end + 3] = get_quest_response_latency(prompt_response_file)
    # end = len(df.columns)
    # print("Updated after adding response latency: " + str(len(df.columns)))
    return df


def get_micro_ema_dataframe(resp_df):
    # print("Subsetting microEMA dataframe")
    # Filter rows where the column number [1] contains "Micro_EMA"
    u_df = resp_df[resp_df[1].str.contains('Micro', na=False)]
    # print("Printing the head of microEMA responses")
    # print(u_df.head(6))
    # print("No. of rows: " + str(u_df.shape[0]))
    return u_df


def get_phone_ema_dataframe(resp_df):
    # print("Subsetting phoneEMA dataframe")
    # Filter out all the uEMA rows
    p_df = resp_df[~resp_df[1].str.contains('Micro', na=False)]
    # get_set_count_list(p_df)
    # print("Printing the head of phoneEMA responses")
    # print(p_df.head(6))
    return p_df


def get_phone_response_times(df, is_burst_day):
    # print("Computing response for all phone EMA times")
    end = len(df.columns)
    # print("When getting phone response times, " + str(end))
    col = end - 3
    all_resp_time_mean = df[col].mean()
    all_resp_time_mean = round(all_resp_time_mean, 2)
    # print("ALL RESP TIME IS: " + str(all_resp_time_mean))
    if np.isnan(all_resp_time_mean):
        all_resp_time_mean = N_A
    all_resp_time_med = df[col].median()
    all_resp_time_med = round(all_resp_time_med, 2)
    if np.isnan(all_resp_time_med):
        all_resp_time_med = N_A
    sleep_df = df[df[1].str.contains('WakeSleepTime', na=False)]
    sleep_resp_time_mean = sleep_df[col].mean()
    sleep_resp_time_mean = round(sleep_resp_time_mean, 2)
    if np.isnan(sleep_resp_time_mean) and sleep_df.shape[0] != 0:
        sleep_resp_time_mean = N_A
    sleep_resp_time_med = sleep_df[col].median()
    # print("Rows in WakeSleepTime: ", str(sleep_df.shape[0]))
    burst_df = df[df[2].str.contains('BURST', na=False) & df[1].str.contains('EMA', na=False)]
    # print("Rows in BURST: ", str(burst_df.shape[0]))
    burst_resp_time_mean = burst_df[col].mean()
    burst_resp_time_mean = round(burst_resp_time_mean, 2)
    if np.isnan(burst_resp_time_mean) and burst_df.shape[0] != 0:
        burst_resp_time_mean = N_A
    burst_resp_time_med = burst_df[col].median()
    burst_resp_time_med = round(burst_resp_time_med, 2)
    if np.isnan(burst_resp_time_med) and burst_df.shape[0] != 0:
        burst_resp_time_med = N_A
    eod_df = df[df[1].str.contains('Daily', na=False)]
    # print("Rows in EOD: ", str(eod_df.shape[0]))
    eod_resp_time_mean = eod_df[col].mean()
    eod_resp_time_mean = round(eod_resp_time_mean, 2)
    if np.isnan(eod_resp_time_mean) and eod_df.shape[0] != 0:
        eod_resp_time_mean = N_A
    eod_resp_time_med = eod_df[col].median()
    eod_resp_time_med = round(eod_resp_time_med, 2)
    if np.isnan(eod_resp_time_med) and eod_df.shape[0] != 0:
        eod_resp_time_med = N_A
    if is_burst_day == "TIME":
        burst_resp_time_med = burst_resp_time_mean = NOT_APPL
    if is_burst_day == "BURST":
        sleep_resp_time_mean = NOT_APPL
    return all_resp_time_mean, all_resp_time_med, sleep_resp_time_mean, \
           burst_resp_time_mean, burst_resp_time_med, eod_resp_time_mean, \
           eod_resp_time_med


def get_watch_response_times(df, is_burst_day):
    # print("Computing MicroEMA response times")
    end = len(df.columns)
    col = end - 3
    uema_resp_time_mean = df[col].mean()
    uema_resp_time_mean = round(uema_resp_time_mean, 2)
    if np.isnan(uema_resp_time_mean) and df.shape[0] != 0:
        uema_resp_time_mean = N_A
    uema_resp_time_med = df[col].median()
    uema_resp_time_med = round(uema_resp_time_med, 2)
    if np.isnan(uema_resp_time_med) and df.shape[0] != 0:
        uema_resp_time_med = N_A
    if is_burst_day == "BURST":
        uema_resp_time_med = uema_resp_time_mean = NOT_APPL
    return uema_resp_time_mean, uema_resp_time_med


def get_phone_prompt_counts(df, is_burst_day):
    # print("Computing phone EMA prompt counts")
    status = ['Started', 'Completed', 'PartiallyCompleted']
    promptedStatus = ['Started', 'Completed', 'NeverStarted', 'PartiallyCompleted']
    sleep_df = df[df[1].str.contains(r'WakeSleepTime', na=False)]
    # sleep_started_df = sleep_df[sleep_df[10].str.contains('Started') | sleep_df[10].str.contains('Completed')]
    sleep_started_df = sleep_df[sleep_df[10].isin(status)]
    sleep_started = sleep_started_df.shape[0]
    sleep_completed_df = sleep_df[sleep_df[10].isin(['Completed'])]
    sleep_completed = sleep_completed_df.shape[0]
    sleep_first_prompts, sleep_reprompts = check_if_reprompt(sleep_df)
    sleep_completed_firstPrompts, sleep_completed_reprompts = \
        check_if_reprompt(sleep_completed_df)
    # compute total prompted by including all the prompts (with reprompts)
    sleep_prompted = sleep_df.shape[0] + sleep_reprompts
    if is_burst_day == "BURST":
        sleep_prompted = sleep_first_prompts = sleep_completed = sleep_started = sleep_reprompts \
            = sleep_completed_firstPrompts \
            = sleep_completed_reprompts = NOT_APPL

    burst_ema_df = df[df[1].isin(['EMA']) & ~df[10].isin(['NeverPrompted'])]
    # burst_ema_prompted = burst_ema_df.shape[0]
    burst_ema_started_df = burst_ema_df[burst_ema_df[10].isin(status)]
    burst_ema_started = burst_ema_started_df.shape[0]
    burst_ema_completed_df = burst_ema_df[burst_ema_df[10].isin(['Completed'])]
    burst_ema_completed = burst_ema_completed_df.shape[0]

    # print("Number of burst EMA started: ", str(burst_ema_started))
    # print("Number of burst EMA prompted: ", str(burst_ema_prompted))
    # print("Number of burst EMA completed: ", str(burst_ema_completed))

    burst_ema_firstPrompts, burst_ema_reprompts = check_if_reprompt(burst_ema_df)
    burst_ema_completed_firstPrompt, burst_ema_completed_reprompts = check_if_reprompt(burst_ema_completed_df)

    burst_ema_prompted = burst_ema_df.shape[0] + burst_ema_reprompts
    burst_ema_original_prompted = burst_ema_df.shape[0]

    if is_burst_day == "TIME":
        burst_ema_prompted = burst_ema_original_prompted = burst_ema_reprompts = burst_ema_started \
            = burst_ema_completed = burst_ema_completed_firstPrompt = burst_ema_completed_reprompts = NOT_APPL

    eod_df = df[df[1].isin(['Daily'])]
    # eod_df_prompted = eod_df.shape[0]
    eod_df_started = eod_df[eod_df[10].isin(status)]
    eod_df_completed = eod_df[eod_df[10].isin(['Completed'])]
    eod_started = eod_df_started.shape[0]
    eod_completed = eod_df_completed.shape[0]
    eod_firstPrompts, eod_reprompts = check_if_reprompt(eod_df)
    eod_completed_firstPrompts, eod_completed_reprompts = check_if_reprompt(eod_df_completed)
    eod_df_prompted = eod_df.shape[0] + eod_reprompts
    eod_original_prompted = eod_df.shape[0]

    return sleep_prompted, sleep_started, sleep_completed, \
           sleep_first_prompts, sleep_reprompts, sleep_completed_firstPrompts, sleep_completed_reprompts, \
           burst_ema_prompted, burst_ema_original_prompted, burst_ema_started, burst_ema_completed, \
           burst_ema_firstPrompts, burst_ema_reprompts, burst_ema_completed_firstPrompt, burst_ema_completed_reprompts, \
           eod_df_prompted, eod_original_prompted, eod_started, eod_completed, \
           eod_firstPrompts, eod_reprompts, eod_completed_firstPrompts, eod_completed_reprompts


def get_watch_prompt_counts(df, is_burst_day):
    # print("Computing watch prompt counts")
    uema_prompted = df.shape[0]
    # print("Number of microEMA prompts: ", uema_prompted)
    uema_completed_df = df[df[10].isin(['Completed', 'CompletedThenDismissed'])]
    uema_completed = uema_completed_df.shape[0]
    uema_partially_completed_df = df[df[10].isin(['PartiallyCompleted'])]
    uema_partial_completed = uema_partially_completed_df.shape[0]
    uema_cs = df[df[1].isin(['CS_EMA_Micro'])]
    uema_cs_prompted = uema_cs.shape[0]
    uema_cs_completed_df = uema_cs[uema_cs[10].isin(['Completed', 'CompletedThenDismissed'])]
    uema_cs_completed = uema_cs_completed_df.shape[0]
    uema_trivia = df[df[1].isin(['Trivia_EMA_Micro'])]
    uema_trivia_prompted = uema_trivia.shape[0]
    uema_trivia_completed_df = uema_trivia[uema_trivia[10].isin(['Completed', 'CompletedThenDismissed'])]
    uema_trivia_completed = uema_trivia_completed_df.shape[0]
    # print("Number of uEMA completed: ", uema_completed)
    if is_burst_day == "BURST":
        uema_prompted = uema_completed = NOT_APPL
    return uema_prompted, uema_completed, uema_partial_completed, uema_cs_prompted, \
           uema_cs_completed, uema_trivia_prompted, uema_trivia_completed


def check_if_reprompt(df):
    # print("Checking if a prompt is reprompt or not")
    end = len(df.columns)
    df.loc[:, end] = ((df[13] == -1) & (df[16] == -1) & (df[19] == -1) & (df[22] == -1) & (df[25] == -1)).astype(int)
    firstPrompts = len(df[df[end] == 1])
    rePrompts = len(df[df[end] == 0])
    # print("Printing with reprompt column")
    # print(df[end].head(6))
    # print("First prompts: " + str(firstPrompts) + " and Reprompts: " + str(rePrompts))
    return firstPrompts, rePrompts


def get_time_zone(hour_folder_name):
    hour_str_clean = hour_folder_name.split("_")[0]
    time_zone_str = hour_str_clean.split("-")[1]
    return time_zone_str


def get_folder_sizes(user_path, date):
    # print("Getting folder sizes")
    all_folders_sizes = {LOGS: 0.0, LOGS_WATCH: 0.0, DATA: 0.0,
                         DATA_WATCH: 0.0}
    time_zone_list = []
    for folder in all_folders_sizes.keys():
        folder_size = 0
        folder_path = user_path + sep + folder + sep + date
        # print("Checking folder:", folder_path)
        if path.exists(folder_path) and not folder.endswith(".zip"):
            for sub_folder in listdir(folder_path):
                sub_folder_path = folder_path + sep + sub_folder
                folder_size += path.getsize(sub_folder_path)
                time_zone_list.append(get_time_zone(sub_folder))
            all_folders_sizes[folder] = folder_size
        else:
            all_folders_sizes[folder] = N_A

    if all_folders_sizes[LOGS] != N_A:
        all_folders_sizes[LOGS] = '%.2f' % (all_folders_sizes[LOGS] / 1024)
    if all_folders_sizes[DATA] != N_A:
        all_folders_sizes[DATA] = '%.2f' % (all_folders_sizes[DATA] / (1024 * 1024))
    if all_folders_sizes[LOGS_WATCH] != N_A:
        all_folders_sizes[LOGS_WATCH] = '%.2f' % (all_folders_sizes[LOGS_WATCH] / 1024)
    if all_folders_sizes[DATA_WATCH] != N_A:
        all_folders_sizes[DATA_WATCH] = '%.2f' % (
                all_folders_sizes[DATA_WATCH] / (1024 * 1024))

    time_zone_changed = False
    if len(set(time_zone_list)) > 1:
        time_zone_changed = True

    return all_folders_sizes[LOGS], all_folders_sizes[DATA], \
           all_folders_sizes[LOGS_WATCH], all_folders_sizes[DATA_WATCH], time_zone_changed


def get_undo_counts(is_burst_day, watch_prompt_activity_file):
    # print("Getting undo counts for microEMA")
    # file_path = temp_date_path + sep + WATCH_PROMPT_ACTIVITY
    # print(watch_prompt_activity_file)
    undo_str = "Undo selected"
    undo_counter = 0
    # if path.exists(file_path):
    if watch_prompt_activity_file is not N_A:
        # with open(file_path) as undo_csv:
        # csv_reader = csv.reader(fix_nulls(undo_csv), delimiter=",")
        csv_reader = csv.reader(watch_prompt_activity_file.splitlines(), delimiter=",")
        for row in csv_reader:
            # print(row)
            if undo_str in row[2]:
                undo_counter += 1
        if is_burst_day == "BURST":
            undo_counter = NOT_APPL
        return undo_counter
    else:
        return N_A


def get_set_count_list(df):
    # print("Get set counts for each phone prompt")
    # df = df[30].replace(np.nan, 'None', regex = True)
    # First filter out all the never started and never prompted prompts.
    status = ["NeverPrompted", "NeverStarted"]
    df = df.loc[~df[10].isin(status)]
    df[30].fillna("None", inplace=True)
    # print("print head before counting sets")
    # print(df.head(6))
    set_list = df.groupby([30]).size()
    set_names = df.groupby([30]).groups.keys()
    # print("set names are: " + str(len(set_names)))
    # print(set_names)
    # print("The set prompts are: " + str(len(set_list)))
    # print(set_list)
    set_count_list = ""
    k = 0
    for i in set_names:
        set_count_list = set_count_list + " | " + str(i) + " : " + str(set_list[k])
        k = k + 1
        # print(set_count_list)
    # set_count_list = "Set_1: " + str(set_list[0]) + " | Set 2: " + str(set_list[1]) + " | Set_3: " + str(set_list[2])
    # print(set_count_list)
    return set_count_list


def get_total_skipped(prompt_response_file):
    # print("Getting number of skipped items")
    # file_path = temp_date_path + sep + PROMPT_RESP
    skip_count = 0
    # if path.exists(file_path):
    if prompt_response_file is not N_A:
        # with open(file_path) as resp_csv:
        #     csv_reader = csv.reader(resp_csv, delimiter=",")
        csv_reader = csv.reader(prompt_response_file.splitlines(), delimiter=",")
        for row in csv_reader:
            # split the row by ","
            len_row = len(row)
            # print("Row length is: " + str(len_row))
            for i in range(0, len_row):
                if row[i] == "_NOT_ANS_" and row[i + 1] != "-1":
                    skip_count = skip_count + 1
                    # print("Skip count is: " + str(skip_count))
        # print("Final skip count of the day: " + str(skip_count))
        return skip_count
    else:
        return N_A


def get_uema_validation(val_key_file, prompt_response_file):
    # print("Getting number of skipped items")
    # file_path = temp_date_path + sep + PROMPT_RESP
    uema_responses = []
    total_val_prompted = 0
    total_val_correct = 0
    skip_count = 0
    # if path.exists(file_path):
    if prompt_response_file is not N_A:
        # with open(file_path) as resp_csv:
        #     csv_reader = csv.reader(resp_csv, delimiter=",")
        csv_reader = csv.reader(prompt_response_file.splitlines(), delimiter=",")
        for row in csv_reader:
            len_row = len(row)
            if "Micro" in row[1] and row[10] == "Completed":
                # print("The ID is: " + str(row[33]))
                if "Val_" in row[33]:
                    uema_responses.append(row)
    total_val_prompted = len(uema_responses)
    # print("uEMA filtered rows are: ")
    # print(uema_responses)
    if total_val_prompted != 0:
        # with open('validation_key_ans.json', 'r') as openfile:
        #     valid_key_ans_dict = json.load(openfile)

        for i in uema_responses:
            # print(str(i[34]))
            if i[34] in val_key_file:
                # print('found it with answer: ' + str(i[35]) + ' answer in list: ' + str(valid_key_ans_dict[i[34]]))
                valid_ans = val_key_file[i[34]]
                if isinstance(valid_ans, str):
                    if i[35] == valid_ans:
                        # print('correct answer')
                        total_val_correct = total_val_correct + 1
                else:
                    for ans in valid_ans:
                        if i[35] == ans:
                            total_val_correct = total_val_correct + 1
            else:
                return N_A
        val_perc_correct = total_val_correct / total_val_prompted
        # print("Perc val correct: " + str(val_perc_correct))
        return round(val_perc_correct, 2)
    else:
        # print("Perc val correct: " + N_A)
        return N_A


def get_watch_notif_alerts(notif_mgr_file):
    # print("Reading notification manager for watch notifications")
    # file_path = temp_date_path + sep + NOTIF_MGR_SVC
    watch_full_notif_count = 0
    watch_battery_low_notif_count = 0
    watch_service_not_run_notif_count = 0
    watch_update_notif_count = 0
    watch_turn_off_dnd_notif_count = 0
    watch_connect_notf_count = 0
    # if path.exists(file_path):
    if notif_mgr_file is not N_A:
        # with open(file_path) as inp:
        #     csv_reader = csv.reader(fix_nulls(inp), delimiter=",")
        csv_reader = csv.reader(notif_mgr_file.splitlines(), delimiter=",")
        for row in csv_reader:
            try:
                note = row[4]
            except:
                continue
            # print("WATCH NOTE BEFORE: " + note)
            if "showing notification" in note:
                # print("WATCH NOTIF NOTE: " + note)
                note_message = note.replace("showing notification", "")
                # print("WATCH NOTE MESSAGE: " + note_message)
                if note_message == "Battery full. Please wear the watch.":
                    watch_full_notif_count += 1
                elif note_message == "Battery low. Please charge the watch.":
                    watch_battery_low_notif_count += 1
                elif note_message == "All services not running. Please launch TIME app on watch.":
                    watch_service_not_run_notif_count += 1
                elif note_message == "Please turn off Do not Disturb mode on watch.":
                    watch_turn_off_dnd_notif_count += 1
                elif note_message == "Watch not in connection!":
                    watch_connect_notf_count += 1
            elif "Showing update watch notif, last 5 mins." in note:
                watch_update_notif_count += 1
        return watch_full_notif_count, watch_battery_low_notif_count, watch_service_not_run_notif_count, \
               watch_update_notif_count, watch_turn_off_dnd_notif_count, watch_connect_notf_count
    else:
        return N_A, N_A, N_A, N_A, N_A, N_A


def get_watch_sampling_rate_range(sampling_rate_file):
    # print("Getting watch accel sampling rate range for the day")
    # file_path = temp_date_path + sep + WATCH_SAMPLING_RATE
    # if path.exists(file_path):
    if sampling_rate_file is not N_A:
        try:
            rate_file = pd.read_csv(StringIO(sampling_rate_file), header=None, delimiter=",")
        except:
            return N_A
        min_rate = round(np.min(rate_file.iloc[:, 3]), 2)
        max_rate = round(np.max(rate_file.iloc[:, 3]), 2)
        min_max_rate = str(min_rate) + " - " + str(max_rate)
        return min_max_rate
    else:
        return N_A


def get_watch_memory(watch_wake_file):
    # print("Getting watch memory by the end of the day")
    # file_path = temp_date_path + sep + WATCH_WAKE_SRVC
    storage_val = N_A
    ram_val = N_A
    # if path.exists(file_path):
    if watch_wake_file is not N_A:
        # with open(file_path) as inp:
        #     csv_reader = csv.reader(inp, delimiter=",")
        csv_reader = csv.reader(watch_wake_file.splitlines(), delimiter=",")
        for row in csv_reader:
            try:
                note = row[2]
                # print("NOTE1: " + str(note))
            except:
                continue
            # print("MEMORY NOTE: " + str(row))
            if "Watch available storage" in note:
                storage_val = note.replace("Watch available storage: ", "")
                # print("STORAGE_VAL: " + str(storage_val))
                storage_val = storage_val.split("MB")[0]
                note2 = row[3]
                # print("NOTE: " + str(note2))
                if "free RAM" in note2:
                    # ram_val = note.split(",")[1]
                    ram_val = note2.replace("free RAM: ", "")
                    ram_val = ram_val.split("MB")[0]
                    # print("AVAILABLE RAM:" + str(ram_val))
                # print("STORAGE_VAL_2: " + str(storage_val))
    # print("FINAL WATCH MEMORY: " + str(storage_val))
    return storage_val, ram_val


def get_collected_expected_sensor_samples(date, watch_sensor_file):
    # print("Getting sensor sample counts")
    # file_path = temp_date_path + sep + WATCH_SENSOR_MGR
    samples_collected_total = 0
    midnight_past = date.replace(hour=0, minute=0, second=0,
                                 microsecond=0)
    # print("Midnight past: ", datetime.strftime(midnight_past,
    #                                            "%Y-%m-%d %H:%M:%S.%f %Z"))
    midnight_future = float((midnight_past + timedelta(days=1)).timestamp())
    midnight_past = float(midnight_past.timestamp())
    # if path.exists(file_path):
    if watch_sensor_file is not N_A:
        # with open(file_path) as inp:
        #     csv_reader = csv.reader(fix_nulls(inp), delimiter=",")
        csv_reader = csv.reader(watch_sensor_file.splitlines(), delimiter=",")
        for row in csv_reader:
            # print("length is: " + str(len(row)))
            if len(row) == 4:
                # print("ROW is: " + str(row))
                note_collected = row[2]
                note_expected = row[3]
                log_time = row[0]
                # Remove time zone
                if bool(re.search('[A-Z]{3}-[0-9]{2}:[0-9]{2}', log_time)):
                    log_time = re.sub('[A-Z]{3}-[0-9]{2}:[0-9]{2}', '', log_time)
                elif bool(re.search('[A-Z]{3}\+[0-9]{2}:[0-9]{2}', log_time)):
                    log_time = re.sub('[A-Z]{3}\+[0-9]{2}:[0-9]{2}', '', log_time)
                elif bool(re.search('[A-Z]{4}', log_time)):
                    log_time = re.sub('[A-Z]{4}', '', log_time)
                elif bool(re.search('[A-Z]{3}', log_time)):
                    log_time = re.sub('[A-Z]{3}', '', log_time)
                # print('log time without time zone ' + str(log_time))
                try:
                    log_time_stamp = datetime.strptime(log_time, '%a %b %d %H:%M:%S  %Y')
                except:
                    continue
                # print("log time stamp is: " + str(log_time_stamp))
                log_time_stamp = float(log_time_stamp.timestamp())
                # print("log time stamp in float: " + str(log_time_stamp))
                if "Collected total" in note_collected and "expected total" in note_expected:
                    # print("NOTE collected: " + str(note_collected) + ", Expected: " + str(note_expected))
                    if log_time_stamp < midnight_future:
                        # print("Sample log found before midnight")
                        collected = note_collected.split(":")[1]
                        # expected = note_expected.split(":")[1]
                        samples_collected_total = float(collected.replace(" ", ""))
    return samples_collected_total


def get_wifi_off_state_version_code(phone_upload_mgr_file):
    # print("Getting wifi status on the phone")
    # file_path = temp_date_path + sep + UPLOAD_MGR_SVC
    wifi_off_min = 0
    version_code = N_A
    # if path.exists(file_path):
    if phone_upload_mgr_file is not N_A:
        # with open(file_path) as inp:
        #     csv_reader = csv.reader(fix_nulls(inp), delimiter=",")
        csv_reader = csv.reader(phone_upload_mgr_file.splitlines(), delimiter=",")
        for row in csv_reader:
            try:
                note = row[4]
            except:
                continue
            if 'Wifi state' in note:
                # print("NOTE: " + note)
                wifi_state = note.split(":")[1]
                wifi_state = wifi_state.replace(" ", "")
                # print("Final state: " + str(wifi_state))
                if wifi_state == 'false':
                    wifi_off_min += 1
            elif re.match(r"Current App version code", note):
                version_code = row[4][-4:]
        return wifi_off_min, version_code
    else:
        return N_A, N_A


def get_daily_location_cluster_numbers(cluster_file):
    # print("Counting unique clusters for the day")
    look_up_text = 'Observed cluster with id'
    # file_path = temp_date_path + sep + CLUSTER_LOG_FILE
    num_of_clusters = 0
    cluster_list = []
    # if path.exists(file_path):
    if cluster_file is not N_A:
        # with open(file_path) as inp:
        #     csv_reader = csv.reader(fix_nulls(inp), delimiter=",")
        csv_reader = csv.reader(cluster_file.splitlines(), delimiter=",")
        for row in csv_reader:
            try:
                note = row[4]
            except:
                continue
            if look_up_text in note:
                cluster_id = note.split(':')[1]
                cluster_id = cluster_id.split('.')[0]
                cluster_list.append(cluster_id)
        num_of_clusters = len(set(cluster_list))
    else:
        num_of_clusters = N_A
    return num_of_clusters
