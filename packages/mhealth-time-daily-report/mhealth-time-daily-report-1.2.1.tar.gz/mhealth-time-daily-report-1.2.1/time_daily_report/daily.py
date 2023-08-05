import pandas as pd
from os import listdir, path, sep, makedirs
from datetime import datetime, timedelta
import time
import re
import sys
import warnings

from time_daily_report.utils import delete_folder_tree, delete_file, load_validation_json, check_daylight_saving

from time_daily_report.file_parsers import parse_upload_manager, parse_prompt_responses, \
    parse_step_counter, get_non_microt_notif_count, \
    parse_watch_accel_summary, get_sleep_duration, get_dnd_dur, get_off_dur, \
    get_charging_stats_phone_unlocks, get_folder_sizes, \
    get_phone_loc_data_mins, get_undo_counts, get_unqiue_apps_count, get_watch_notif_alerts, \
    get_watch_sampling_rate_range, get_watch_memory, get_sleep_wake_time_changes, \
    get_retrospective_sleep_wake_times, get_collected_expected_sensor_samples, get_wifi_off_state_version_code, \
    get_daily_location_cluster_numbers, get_uema_validation

warnings.filterwarnings("ignore")

VERSION_NUMBER = "v1.2"

date_format = '%Y-%m-%d'
day_of_week_format = '%a'
prev_day_sleep_time = "NA"
LAST_RECORDED_SLEEP_FILE = "last_recorded_sleep.txt"
watch_data_collected_hr = 0
WATCH_COLLECTED_SAVED = "watch_data_collected.txt"
STABLE_SAMPLING_RATE = 50
DAY_LENGTH = 24 * 60 * 60
EXPECTED_SAMPLES_PER_DAY = STABLE_SAMPLING_RATE * DAY_LENGTH

N_A = "null"
NOT_APPL = "N_A"
NINE_HOUR = 9.0
DAY_LENGTH = 24.0
BUFFER = 1.0
BURST_COMP_COMPLETED = 8

DETECTED_MIMS_FILE = "mims"
DETECTED_SWAN_FILE = "SWaN_"
FINAL_CSV = "_final.csv"
GPS_FILE_NAME = "GPS.csv.zip"
bufferSize = 64 * 1024
LOGS = "logs"
LOGS_WATCH = "logs-watch"
DATA = "data"
DATA_WATCH = "data-watch"
ALL_LOG_FOLDERS = [
    LOGS,
    LOGS_WATCH
]
ALL_DATA_FOLDERS = [
    DATA,
    DATA_WATCH
]
ALL_FOLDERS = ALL_LOG_FOLDERS + ALL_DATA_FOLDERS

FILES_TO_PARSE = ["MicroTUploadManagerServiceNotes.log.csv", "SystemBroadcastReceiver.log.csv",
                  "Watch-TimeStudyArbitrater.log.csv", "Watch-PowerConnectionReceiverNotes.log.csv",
                  "PromptResponses.log.csv", "MicroTUploadManagerService.log.csv", "Watch-PromptActivity.log.csv",
                  "NotificationCounts.csv", "AppEventCounts.csv", "StepCounterService.csv",
                  "Watch-AccelSampling.log.csv", "Watch-MiscLogger.log.csv", "Watch-SensorManagerService.log.csv",
                  "GPS.csv", "Watch-SamplingRate.log.csv", "Watch-WearableWakefulService.log.csv",
                  "ClusterMaker.log.csv", "NotificationManager.log.csv"]
FILES_TO_COMPUTE = ["mims.csv"]

VALIDATION_KEY_VAL = load_validation_json()

REPORTS = "reports"
DOMAIN_NAME = "@timestudy_com"
TEMP_FOLDER = "_temporary"
REPORT = "report_"
REPORT_COLUMNS = ["participant_ID", "date", "time_zone_changed", "daylight_saving", "study_mode",
                  "eod_original_prompted_num",
                  "eod_completed_num",
                  "burst_ema_original_prompted_num", "burst_ema_completed_num", "sleep_time_reported_hr",
                  "phone_off_min", "watch_off_dur_shut", "samples_collected_percent", "samples_collected_hr",
                  "uema_prompted_num", "uema_completed_num",
                  "nondata_time_computed_hr", "sleep_time_computed_hr", "watch_charging_min",
                  "watch_charging_num_bouts",
                  "start_date", "end_Date",
                  "day_of_week", "days_into_study", "version_code", "watch_assigned",
                  "is_postponed_burst_mode_day", "current_wake_time", "current_sleep_time",
                  "next_wake_time", "mims_unit_daily_sum", "mims_unit_sample_num", "mims_unit_invalid_sample_num",
                  "wear_time_computed_hr", "nonwear_time_computed_hr",
                  "computed_sleep_time_when_sleeping_hr", "computed_nonwear_time_when_sleeping_hr",
                  "sleep_time_change_num", "wake_time_change_num", "previous_sleep_time", "previous_wake_time",
                  "phone_dnd_mode_min", "watch_dnd_mode_min", "watch_off_min",
                  "sleep_qs_prompted_num", "sleep_qs_reprompt_num",
                  "sleep_qs_started_num", "sleep_qs_completed_num",
                  "sleep_qs_completed_first_prompt_num", "sleep_qs_completed_reprompt_num",
                  "burst_ema_prompted_num", "burst_ema_reprompt_num",
                  "burst_ema_started_num", "burst_ema_completed_first_prompt_num", "burst_ema_completed_reprompt_num",
                  "eod_prompted_num", "eod_reprompt_num", "eod_started_num", "eod_completed_first_prompt_num",
                  "eod_completed_reprompt_num", "set_types_presented", "all_ema_ques_skip_num",
                  "uema_partial_completed_num",
                  "uema_cs_prompted", "uema_cs_completed", "uema_trivia_prompted", "uema_trivia_completed",
                  "uema_undo_num", "uema_validation_perc",
                  "sleep_qs_completion_rate", "sleep_qs_first_prompt_completion_rate",
                  "burst_ema_completion_rate", "burst_ema_first_prompt_completion_rate", "burst_ema_compliance_rate",
                  "burst_ema_9h_compliance_rate", "burst_ema_comp_compliance",
                  "uema_completion_rate", "uema_compliance_rate", "uema_9h_compliance_rate",
                  "all_ema_surv_resp_time_mean", "all_ema_surv_resp_time_med",
                  "sleep_surv_resp_time_mean", "burst_ema_surv_resp_time_mean", "burst_ema_surv_resp_time_med",
                  "eod_surv_resp_time_mean", "eod_surv_resp_time_med", "uema_resp_time_mean", "uema_resp_time_med",
                  "all_ema_response_latency_from_first_prompt_mean", "all_ema_response_latency_from_first_prompt_med",
                  "all_ema_response_latency_from_reprompt_mean", "all_ema_response_latency_from_reprompt_med",
                  "all_ema_single_quest_resp_time_mean", "all_ema_single_quest_resp_time_med",
                  "all_ema_single_ques_resp_time_without_latency_mean",
                  "all_ema_single_ques_resp_time_without_latency_med", "phone_charging_num_bouts", "phone_charging_min",
                  "watch_full_notif_count",
                  "watch_battery_low_notif_count", "watch_service_not_run_notif_count",
                  "watch_update_notif_count", "watch_turn_off_dnd_notif_count", "watch_connect_notf_count",
                  "phone_unlock_num", "location_data_avail_min", "location_clusters_identified",
                  "notifs_received_excluding_TIME_num", "unique_apps_used_num",
                  "daily_step_count", "watch_no_motion_min", "watch_sampling_rate_range",
                  "watch_available_memory_MB", "watch_available_RAM", "phone_wifi_off_min",
                  "phone_logs_size_KB", "phone_data_size_MB",
                  "watch_logs_size_KB", "watch_data_size_MB", "watch_data_files_num", "samples_collected"]

no_of_args = len(sys.argv)
print("No of command line arguments: ", no_of_args)

if no_of_args < 2:
    print("Root path to 'MICROT/Participant_id' folder is required as the first argument. Exiting ...")
    sys.exit(1)

root_path = sys.argv[1]

usernames = []

if no_of_args < 3:
    print("Please provide a date to run daily report. Exiting ...")
    sys.exit(1)

date_to_run = sys.argv[2]

if no_of_args < 4:
    print("Please specify if the decrypted raw should be deleted or not. Exiting ...")
    sys.exit(1)

delete_raw = sys.argv[3]


def clean_log_file(log_content, log_file_name):
    if log_file_name == "Watch-AccelSampling.log.csv":
        if len(log_content) > 0:
            # find log file that is not ended with '\n'. This will cause concatenation of two lines.
            if log_content[-1] != "\n":
                # sometimes the log file is ended with extra letters after \n
                if '\n' in log_content[-5:]:
                    return log_content[:log_content.rfind('\n') + 1]
                else:
                    # add \n if just simply missing \n
                    return log_content + '\n'
    return log_content


def get_prev_day_sleep_time(folder_path):
    # print("Extracting previous day's sleep timestamp")
    file_path = folder_path + sep + LAST_RECORDED_SLEEP_FILE
    if path.exists(file_path):
        with open(file_path) as f:
            line = f.readline()
            return line.rstrip("\n")
    else:
        return "NA"


def get_mims_stats(mims_unit_df_hour):
    df_subset_valid = mims_unit_df_hour[mims_unit_df_hour["MIMS_UNIT"] >= 0]
    df_subset_invalid = mims_unit_df_hour[mims_unit_df_hour["MIMS_UNIT"] < 0]
    mims_unit_df_hour = df_subset_valid["MIMS_UNIT"].sum()
    mims_unit_sample_num_hour = df_subset_valid.shape[0]
    mims_unit_invalid_sample_num = df_subset_invalid.shape[0]
    return mims_unit_df_hour, mims_unit_sample_num_hour, mims_unit_invalid_sample_num


def get_sleep_wear_nonwear_stats(folder_path, date_string, wake_time, sleep_time, user_path):
    SWAN_FILE = DETECTED_SWAN_FILE + date_string + FINAL_CSV
    # print("Reading SWAN_FILE: " + SWAN_FILE)
    file_name = folder_path + sep + SWAN_FILE
    # print("Reading file name: " + file_name)
    if path.exists(file_name):
        # read file as a pd
        swan_file = pd.read_csv(file_name, header=0)
        # change to date time format
        # swan_file['HEADER_TIME_STAMP'] = pd.to_datetime(swan_file['HEADER_TIME_STAMP'])
        swan_file['START_TIME'] = pd.to_datetime(swan_file['START_TIME'])
        global prev_day_sleep_time
        wake_time = wake_time[0:19]
        sleep_time = sleep_time[0:19]
        midnight_past = date_string + " 00:00:00"
        midnight_past = datetime.strptime(midnight_past, "%Y-%m-%d %H:%M:%S")
        midnight_future = datetime.strptime(date_string, "%Y-%m-%d")
        midnight_future += timedelta(days=1)
        wear_dur = len(swan_file[swan_file['PREDICTION'] == 'Wear']) * (30 / 3600)
        sleep_dur = len(swan_file[swan_file['PREDICTION'] == 'Sleep']) * (30 / 3600)
        nonwear_dur = len(swan_file[swan_file['PREDICTION'] == 'Nonwear']) * (30 / 3600)
        # print("WEAR, SLEEP, NONWEAR: " + str(wear_dur) + "," + str(sleep_dur) + "," + str(nonwear_dur))
        # print("MIDNIGHT PAST: " + str(midnight_past) + " MIDNIGHT FUTURE: " + str(midnight_future))
        try:
            wake_time = datetime.strptime(wake_time, "%Y-%m-%d %H:%M:%S")
        except:
            return round(wear_dur, 2), round(sleep_dur, 2), round(nonwear_dur, 2), N_A, N_A
        try:
            sleep_time = datetime.strptime(sleep_time, "%Y-%m-%d %H:%M:%S")
        except:
            return round(wear_dur, 2), round(sleep_dur, 2), round(nonwear_dur, 2), N_A, N_A
        # Also get previous day's sleep time
        prev_day_sleep_time = get_prev_day_sleep_time(user_path)
        # print("EXTRACTED previois day sleep: " + str(prev_day_sleep_time))
        if prev_day_sleep_time == "NA":
            prev_day_sleep_time = midnight_past
        else:
            prev_day_sleep_time = datetime.strptime(prev_day_sleep_time, "%Y-%m-%d %H:%M:%S")
        # print("Previous day's sleep time: " + str(prev_day_sleep_time))
        # print("Current sleep time: " + str(sleep_time))
        # Get before wake time stamp
        before_wake_time = max(midnight_past, prev_day_sleep_time)
        # print("BEFORE WAKE TIME IS: " + str(before_wake_time))
        # print("WAKE TIME IS: " + str(wake_time))
        if before_wake_time <= wake_time:
            before_wake_subset = swan_file[(before_wake_time <= swan_file['START_TIME']) &
                                           (swan_file['START_TIME'] <= wake_time)]
            sleep_time_computed_during_sleep = len(before_wake_subset[before_wake_subset['PREDICTION'] == "Sleep"]) * \
                                               (30 / 3600)
            nonwear_time_computed_during_sleep = len(
                before_wake_subset[before_wake_subset['PREDICTION'] == "Nonwear"]) * \
                                                 (30 / 3600)
        else:
            sleep_time_computed_during_sleep = 0
            nonwear_time_computed_during_sleep = 0
        if sleep_time <= midnight_future:
            after_sleep_subset = swan_file[(sleep_time <= swan_file['START_TIME']) &
                                           (swan_file['START_TIME'] <= midnight_future)]
            sleep_time_computed_during_sleep = sleep_time_computed_during_sleep + \
                                               len(after_sleep_subset[after_sleep_subset['PREDICTION'] == 'Sleep']) * \
                                               (30 / 3600)
            nonwear_time_computed_during_sleep = nonwear_time_computed_during_sleep + \
                                                 len(after_sleep_subset[
                                                         after_sleep_subset['PREDICTION'] == 'Nonwear']) * \
                                                 (30 / 3600)
        # print("Computed nonwear time during sleep: " + str(nonwear_time_computed_during_sleep))
        # print("Computed sleep time during sleep: " + str(sleep_time_computed_during_sleep))
        # write the prev_day_sleep_time to a file
        prev_day_sleep_time = sleep_time
        # print("Final previous day's sleep time: " + str(prev_day_sleep_time))
        # print(prev_day_sleep_time, file=open(user_path + sep + LAST_RECORDED_SLEEP_FILE, 'w'))
        return round(wear_dur, 2), round(sleep_dur, 2), round(nonwear_dur, 2), \
               round(sleep_time_computed_during_sleep, 2), round(nonwear_time_computed_during_sleep, 2)
    else:
        return N_A, N_A, N_A, N_A, N_A


def main(root_path, date_to_run, delete_raw):
    script_start_time_dt = datetime.now()
    script_start_time = time.time()
    watch_assigned = False
    user_path = root_path
    root_path_components = user_path.split(sep)
    user_name = root_path_components[len(root_path_components) - 1]
    print("Currently generating for user: ", user_name)
    reports_path = user_path + sep + REPORTS + sep + date_to_run
    if not path.exists(reports_path):
        makedirs(reports_path)
    report_file_path = reports_path + sep + REPORT + date_to_run + '.csv'
    dates_to_check = [date_to_run]
    report_df = pd.DataFrame(columns=REPORT_COLUMNS)

    report_df.set_index("date", inplace=True, drop=False)

    for current_date in dates_to_check:
        print("For date: " + str(current_date))
        watch_data_collected = 0
        # >>> MIMS <<<: 1) Day level summary of MIMS Unit; 2) valid sample num
        mims_unit_sum_day = N_A
        mims_unit_sample_num_day = 0
        mims_unit_invalid_sample_num_day = 0
        p_id_list = []
        date_list = []
        hour_list = []
        mims_unit_sum_hour_list = []
        mims_unit_sample_num_hour_list = []
        date = current_date
        available = False
        # Initialize file objects
        phone_sys_file = watch_arbit_file = watch_power_notes_file = phone_upload_mgr_notes_file = \
            prompt_response_file = phone_upload_mgr_file = watch_prompt_activity_file = \
            notif_count_file = app_count_file = step_count_file = watch_misc_file = \
            watch_sampling_file = watch_sensor_file = gps_file = sampling_rate_file = \
            watch_wake_file = notif_mgr_file = cluster_file = N_A

        for folder in ALL_FOLDERS:
            # print("Processing %s files" % folder)
            data_folder_path = user_path + sep + folder + sep + date
            # print(data_folder_path)
            if path.exists(data_folder_path):
                # print(data_folder_path)
                available = True
                for hour_folder in sorted(listdir(data_folder_path)):
                    hour_folder_path = data_folder_path + sep + hour_folder
                    if re.match(r"\d{2}-[A-Z]{3}(\+[0-9_]{5}|$)", hour_folder) or \
                            re.match(r"\d{2}-[A-Z]{3}-\d{4}(\+[0-9_]{5}|$)", hour_folder) or \
                            re.match(r'\d{2}-[A-Z]{4}(\+[0-9_]{5}|$)', hour_folder) or \
                            re.match(r'\d{2}-[A-Z]{3}(-|\+)\d{2}:\d{2}', hour_folder) or \
                            re.match(r'\d{2}-[A-Z]{3}_\d+', hour_folder) or \
                            hour_folder == "DailyClusteringRelated":
                        # print("Proceeding for: " + hour_folder)
                        for hour_file in listdir(hour_folder_path):
                            if hour_file.endswith(".baf") and folder == DATA_WATCH:
                                watch_data_collected += 1
                                # print("Found::: " + folder + str(watch_data_collected))
                            if hour_file in FILES_TO_PARSE:
                                with open(hour_folder_path + sep + hour_file, encoding='utf-8') as file:
                                    # print("For the file: " + str(hour_file) + " and date " + date + " and hour " +
                                    # hour_folder)
                                    try:
                                        content = file.read()
                                    except:
                                        print("Corrupted file found: " + str(hour_folder_path))
                                        continue
                                    content_cleaned = content
                                    if hour_file == "MicroTUploadManagerServiceNotes.log.csv":
                                        phone_upload_mgr_notes_file = phone_upload_mgr_notes_file + content_cleaned
                                        phone_upload_mgr_notes_file = phone_upload_mgr_notes_file.replace(N_A, '')
                                        phone_upload_mgr_notes_file = phone_upload_mgr_notes_file.replace('\0', '')
                                    elif hour_file == "SystemBroadcastReceiver.log.csv":
                                        phone_sys_file = phone_sys_file + content_cleaned
                                        phone_sys_file = phone_sys_file.replace(N_A, '')
                                        phone_sys_file = phone_sys_file.replace('\0', '')
                                    elif hour_file == "Watch-TimeStudyArbitrater.log.csv":
                                        watch_arbit_file = watch_arbit_file + content_cleaned
                                        watch_arbit_file = watch_arbit_file.replace(N_A, '')
                                        watch_arbit_file = watch_arbit_file.replace('\0', '')
                                    elif hour_file == "Watch-PowerConnectionReceiverNotes.log.csv":
                                        watch_power_notes_file = watch_power_notes_file + content_cleaned
                                        watch_power_notes_file = watch_power_notes_file.replace(N_A, '')
                                        watch_power_notes_file = watch_power_notes_file.replace('\0', '')
                                    elif hour_file == "PromptResponses.log.csv":
                                        prompt_response_file = prompt_response_file + content_cleaned
                                        prompt_response_file = prompt_response_file.replace(N_A, '')
                                        prompt_response_file = prompt_response_file.replace('\0', '')
                                    elif hour_file == "MicroTUploadManagerService.log.csv":
                                        phone_upload_mgr_file = phone_upload_mgr_file + content_cleaned
                                        phone_upload_mgr_file = phone_upload_mgr_file.replace(N_A, '')
                                        phone_upload_mgr_file = phone_upload_mgr_file.replace('\0', '')
                                    elif hour_file == "Watch-PromptActivity.log.csv":
                                        watch_prompt_activity_file = watch_prompt_activity_file + content_cleaned
                                        watch_prompt_activity_file = watch_prompt_activity_file.replace(N_A, '')
                                        watch_prompt_activity_file = watch_prompt_activity_file.replace('\0', '')
                                    elif hour_file == "NotificationCounts.csv":
                                        notif_count_file = notif_count_file + content_cleaned
                                        notif_count_file = notif_count_file.replace(N_A, '')
                                        notif_count_file = notif_count_file.replace('\0', '')
                                    elif hour_file == "AppEventCounts.csv":
                                        app_count_file = app_count_file + content_cleaned
                                        app_count_file = app_count_file.replace(N_A, '')
                                        app_count_file = app_count_file.replace('\0', '')
                                    elif hour_file == "StepCounterService.csv":
                                        step_count_file = step_count_file + content_cleaned
                                        step_count_file = step_count_file.replace(N_A, '')
                                        step_count_file = step_count_file.replace('\0', '')
                                    elif hour_file == "Watch-AccelSampling.log.csv":
                                        content_cleaned = clean_log_file(content_cleaned, hour_file)
                                        watch_sampling_file = watch_sampling_file + content_cleaned
                                        watch_sampling_file = watch_sampling_file.replace(N_A, '')
                                        watch_sampling_file = watch_sampling_file.replace('\0', '')
                                    elif hour_file == "Watch-MiscLogger.log.csv":
                                        watch_misc_file = watch_misc_file + content_cleaned
                                        watch_misc_file = watch_misc_file.replace(N_A, '')
                                        watch_misc_file = watch_misc_file.replace('\0', '')
                                    elif hour_file == "Watch-SensorManagerService.log.csv":
                                        watch_sensor_file = watch_sensor_file + content_cleaned
                                        watch_sensor_file = watch_sensor_file.replace(N_A, '')
                                        watch_sensor_file = watch_sensor_file.replace('\0', '')
                                    elif hour_file == "GPS.csv":
                                        gps_file = gps_file + content
                                        gps_file = gps_file.replace(N_A, '')
                                        gps_file = gps_file.replace('\0', '')
                                    elif hour_file == "Watch-SamplingRate.log.csv":
                                        sampling_rate_file = sampling_rate_file + content_cleaned
                                        sampling_rate_file = sampling_rate_file.replace(N_A, '')
                                        sampling_rate_file = sampling_rate_file.replace('\0', '')
                                    elif hour_file == "Watch-WearableWakefulService.log.csv":
                                        watch_wake_file = watch_wake_file + content_cleaned
                                        watch_wake_file = watch_wake_file.replace(N_A, '')
                                        watch_wake_file = watch_wake_file.replace('\0', '')
                                    elif hour_file == "ClusterMaker.log.csv":
                                        cluster_file = cluster_file + content_cleaned
                                        cluster_file = cluster_file.replace(N_A, '')
                                        cluster_file = cluster_file.replace('\0', '')
                                    elif hour_file == "NotificationManager.log.csv":
                                        notif_mgr_file = notif_mgr_file + content_cleaned
                                        notif_mgr_file = notif_mgr_file.replace(N_A, '')
                                        notif_mgr_file = notif_mgr_file.replace('\0', '')
                            elif hour_file in FILES_TO_COMPUTE:
                                if hour_file == "mims.csv":
                                    # print("** {}".format(hour_folder_path))
                                    mims_unit_df_hour = pd.read_csv(hour_folder_path + sep + hour_file)
                                    mims_unit_sum_hour, mims_unit_sample_num_hour, mims_unit_invalid_sample_num_hour = get_mims_stats(
                                        mims_unit_df_hour)
                                    if mims_unit_sum_day == N_A:
                                        mims_unit_sum_day = 0
                                    mims_unit_sum_day += mims_unit_sum_hour
                                    mims_unit_sample_num_day += mims_unit_sample_num_hour
                                    mims_unit_invalid_sample_num_day += mims_unit_invalid_sample_num_hour
                                    p_id_list.append(user_name)
                                    date_list.append(date_to_run)
                                    hour_list.append(hour_folder)
                                    mims_unit_sum_hour_list.append(mims_unit_sum_hour)
                                    mims_unit_sample_num_hour_list.append(mims_unit_sample_num_hour)
        print("*** check mims")
        if mims_unit_sum_day != N_A:
            df_mims_unit_hour = pd.DataFrame(
                {"p_id": p_id_list, "date": date_list, "hour": hour_list, "mims_unit_sum_hour": mims_unit_sum_hour_list,
                 "mims_unit_sample_num_hour": mims_unit_sample_num_hour_list})
            df_mims_unit_hour.to_csv(reports_path + sep + "mims_sum_hour_{}.csv".format(date_to_run), index=False)

        if available:
            avail_date = date
            # print("processing for date: " + avail_date)
            data_date_path = user_path + sep + DATA_WATCH + sep + avail_date
            day_of_week = datetime.strftime(datetime.strptime(avail_date, date_format),
                                            day_of_week_format)
            snoozed, burst_mode, start_date, end_date, current_sleep_time, current_wake_time, next_wake_time = \
                parse_upload_manager(phone_upload_mgr_notes_file)
            daylight_saving = check_daylight_saving(avail_date, current_wake_time)
            all_EMA_resp_time_mean, all_EMA_resp_time_med, sleep_resp_time_mean, \
            burst_resp_time_mean, burst_resp_time_med, eod_resp_time_mean, \
            eod_resp_time_med, uema_resp_time_mean, uema_resp_time_med, \
            response_latency_mean, response_latency_med, general_latency_mean, general_latency_med, \
            quest_resp_time_mean, quest_resp_time_med, \
            quest_resp_time_without_latency_mean, quest_resp_time_without_latency_med, \
            sleep_prompted, sleep_started, sleep_completed, sleep_first_prompt, \
            sleep_reprompt, sleep_completed_firstPrompt, sleep_completed_reprompt, \
            burst_ema_prompted, burst_ema_original_prompted, burst_ema_started, \
            burst_ema_completed, burst_ema_firstPrompts, burst_ema_reprompts, \
            burst_ema_completed_firstPrompt, burst_ema_completed_reprompt, eod_prompted, eod_original_prompted, eod_started, \
            eod_completed, eod_firstPrompts, eod_reprompts, eod_completed_firstPrompt, \
            eod_completed_reprompt, set_types_prompted, skip_count, \
            uema_prompted, uema_completed, uema_partial_completed, \
            uema_cs_prompted, uema_cs_completed, uema_trivia_prompted, uema_trivia_completed \
                = parse_prompt_responses(burst_mode, prompt_response_file)
            uema_undo_counts = get_undo_counts(burst_mode, watch_prompt_activity_file)
            non_microt_notif_count = get_non_microt_notif_count(notif_count_file)
            unique_app_count = get_unqiue_apps_count(app_count_file)
            daily_step_count = parse_step_counter(step_count_file)
            watch_accel_summary = parse_watch_accel_summary(watch_sampling_file)
            uema_validated_num = get_uema_validation(VALIDATION_KEY_VAL, prompt_response_file)
            days_in_study = N_A
            if start_date != N_A:
                days_in_study = (datetime.strptime(avail_date, date_format)
                                 - datetime.strptime(start_date, date_format)).days
            try:
                sleep_duration = get_sleep_duration(datetime.strptime(avail_date, date_format),
                                                    phone_upload_mgr_notes_file)
            except Exception as e:
                print("Exception occurred while parsing sleep time: ", str(e))
                sleep_duration = N_A
            dnd_phone_dur, dnd_watch_dur = get_dnd_dur(datetime.strptime(avail_date, date_format),
                                                       phone_upload_mgr_notes_file, watch_misc_file)
            off_phone_dur, off_watch_dur, watch_off_dur_shut = get_off_dur(datetime.strptime(avail_date, date_format),
                                                                           phone_sys_file,
                                                                           watch_arbit_file, watch_power_notes_file)
            charging_phone_count, charging_phone_dur, charging_watch_count, \
            charging_watch_dur, phone_unlocks = get_charging_stats_phone_unlocks(datetime.strptime(avail_date,
                                                                                                   date_format),
                                                                                 phone_sys_file,
                                                                                 watch_power_notes_file)
            phone_logs_size, phone_data_size, watch_logs_size, watch_data_size, time_zone_changed = \
                get_folder_sizes(user_path, avail_date)

            # Check if the watch is assigned by the researchers
            if not watch_assigned:
                if watch_logs_size is not "null" or watch_data_size is not "null":
                    watch_assigned = True

            loc_data_mins = get_phone_loc_data_mins(gps_file)
            watch_data_collected_hr = watch_data_collected
            sleep_time_change_num, wake_time_change_num = get_sleep_wake_time_changes(phone_upload_mgr_notes_file)
            prev_sleep_time, prev_wake_time = get_retrospective_sleep_wake_times(prompt_response_file)

            try:
                if burst_mode == "TIME":
                    sleep_qs_completion = sleep_completed / (sleep_prompted - sleep_reprompt)
                    sleep_qs_completion = round(sleep_qs_completion, 2)
                else:
                    sleep_qs_completion = NOT_APPL
            except:
                sleep_qs_completion = 0

            try:
                if burst_mode == "TIME":
                    sleep_qs_first_prompt_completion = sleep_completed_firstPrompt / (sleep_prompted - sleep_reprompt)
                    sleep_qs_first_prompt_completion = round(sleep_qs_first_prompt_completion, 2)
                else:
                    sleep_qs_first_prompt_completion = NOT_APPL
            except:
                sleep_qs_first_prompt_completion = 0

            try:
                if burst_mode == "BURST":
                    burst_ema_completion = burst_ema_completed / (burst_ema_prompted - burst_ema_reprompts)
                    burst_ema_completion = round(burst_ema_completion, 2)
                else:
                    burst_ema_completion = NOT_APPL
            except:
                burst_ema_completion = 0

            try:
                burst_ema_comp_compliance = burst_ema_completed / BURST_COMP_COMPLETED
                burst_ema_comp_compliance = round(burst_ema_comp_compliance, 2)
                if burst_ema_comp_compliance >= 1.0:
                    burst_ema_comp_compliance = 1.0
                if burst_mode == "TIME":
                    burst_ema_comp_compliance = NOT_APPL
            except:
                burst_ema_comp_compliance = N_A

            try:
                if burst_mode == "BURST":
                    burst_ema_compliance = burst_ema_completed / (DAY_LENGTH - BUFFER - sleep_duration)
                    burst_ema_compliance = round(burst_ema_compliance, 2)
                    if burst_ema_compliance < 0:
                        burst_ema_compliance = N_A
                else:
                    burst_ema_compliance = NOT_APPL
            except:
                burst_ema_compliance = N_A

            try:
                if burst_mode == "BURST":
                    burst_ema_9h_compliance = burst_ema_completed / (DAY_LENGTH - BUFFER - NINE_HOUR)
                    burst_ema_9h_compliance = round(burst_ema_9h_compliance, 2)
                else:
                    burst_ema_9h_compliance = NOT_APPL
            except:
                burst_ema_9h_compliance = N_A

            try:
                if burst_mode == "BURST":
                    burst_ema_first_prompt_completion = burst_ema_completed_firstPrompt / (
                            burst_ema_prompted - burst_ema_reprompts)
                    burst_ema_first_prompt_completion = round(burst_ema_first_prompt_completion, 2)
                else:
                    burst_ema_first_prompt_completion = NOT_APPL
            except:
                burst_ema_first_prompt_completion = 0

            try:
                if burst_mode == "TIME" and watch_assigned:
                    uema_completion = uema_completed / uema_prompted
                    uema_completion = round(uema_completion, 2)
                else:
                    uema_completion = NOT_APPL
            except:
                uema_completion = 0

            try:
                if burst_mode == "TIME" and watch_assigned:
                    uema_compliance = uema_completed / (4 * (DAY_LENGTH - (BUFFER / 2) - sleep_duration))
                    uema_compliance = round(uema_compliance, 2)
                    if uema_compliance < 0:
                        uema_compliance = N_A
                else:
                    uema_compliance = NOT_APPL
            except:
                uema_compliance = 0

            try:
                if burst_mode == "TIME" and watch_assigned:
                    uema_9h_compliance = uema_completed / (4 * (DAY_LENGTH - BUFFER - NINE_HOUR))
                    uema_9h_compliance = round(uema_9h_compliance, 2)
                else:
                    uema_9h_compliance = NOT_APPL
            except:
                uema_9h_compliance = 0

            watch_full_notif_count, watch_battery_low_notif_count, watch_service_not_run_notif_count, \
            watch_update_notif_count, watch_turn_off_dnd_notif_count, \
            watch_connect_notf_count = get_watch_notif_alerts(notif_mgr_file)
            phone_wifi_off_min, version_code = get_wifi_off_state_version_code(phone_upload_mgr_file)

            watch_sampling_rate_range = get_watch_sampling_rate_range(sampling_rate_file)

            watch_available_memory, watch_available_RAM = get_watch_memory(watch_wake_file)
            # print("WATCH MEMORY = " + str(watch_available_memory))

            computed_wear_time, computed_sleep_time, computed_nonwear_time, \
            computed_sleep_time_when_sleeping, computed_nonwear_time_when_sleeping, \
                = get_sleep_wear_nonwear_stats(data_date_path, avail_date, current_wake_time,
                                               current_sleep_time, user_path)

            location_clusters_identified = N_A

            samples_collected = get_collected_expected_sensor_samples(datetime.strptime(avail_date, date_format),
                                                                      watch_sensor_file)
            samples_collected_percent = samples_collected / EXPECTED_SAMPLES_PER_DAY
            samples_collected_hr = samples_collected / (STABLE_SAMPLING_RATE * 60 * 60)

            nondata_time_computed_hr = computed_nonwear_time

            num_loc_clusters = get_daily_location_cluster_numbers(cluster_file)
            # delete_folder_tree(temp_date_path)

            if computed_nonwear_time is not N_A and samples_collected_hr is not N_A:
                # print("########: WATCH OFF VAL: " + str(computed_nonwear_time) + ", " + str(watch_off_dur_shut))
                nondata_time_computed_hr = computed_nonwear_time + (DAY_LENGTH - samples_collected_hr)

            # print("Column names size:", len(REPORT_COLUMNS))
            data_row = [user_name, avail_date, time_zone_changed, daylight_saving,
                        burst_mode, eod_original_prompted,
                        eod_completed, burst_ema_original_prompted,
                        burst_ema_completed, sleep_duration, off_phone_dur, watch_off_dur_shut,
                        samples_collected_percent,
                        samples_collected_hr, uema_prompted, uema_completed, nondata_time_computed_hr,
                        computed_sleep_time,
                        charging_watch_dur, charging_watch_count, start_date, end_date, day_of_week,
                        days_in_study, version_code, watch_assigned,
                        snoozed, current_wake_time, current_sleep_time, next_wake_time,
                        mims_unit_sum_day, mims_unit_sample_num_day, mims_unit_invalid_sample_num_day,
                        computed_wear_time, computed_nonwear_time,
                        computed_sleep_time_when_sleeping, computed_nonwear_time_when_sleeping,
                        sleep_time_change_num, wake_time_change_num, prev_sleep_time, prev_wake_time,
                        dnd_phone_dur, dnd_watch_dur, off_watch_dur,
                        sleep_prompted, sleep_reprompt, sleep_started,
                        sleep_completed, sleep_completed_firstPrompt, sleep_completed_reprompt,
                        burst_ema_prompted, burst_ema_reprompts, burst_ema_started,
                        burst_ema_completed_firstPrompt, burst_ema_completed_reprompt,
                        eod_prompted, eod_reprompts, eod_started,
                        eod_completed_firstPrompt, eod_completed_reprompt, set_types_prompted, skip_count,
                        uema_partial_completed, uema_cs_prompted, uema_cs_completed,
                        uema_trivia_prompted, uema_trivia_completed, uema_undo_counts, uema_validated_num,
                        sleep_qs_completion, sleep_qs_first_prompt_completion,
                        burst_ema_completion, burst_ema_first_prompt_completion, burst_ema_compliance,
                        burst_ema_9h_compliance, burst_ema_comp_compliance,
                        uema_completion, uema_compliance, uema_9h_compliance,
                        all_EMA_resp_time_mean,
                        all_EMA_resp_time_med, sleep_resp_time_mean,
                        burst_resp_time_mean, burst_resp_time_med,
                        eod_resp_time_mean, eod_resp_time_med,
                        uema_resp_time_mean, uema_resp_time_med,
                        general_latency_mean, general_latency_med,
                        response_latency_mean, response_latency_med,
                        quest_resp_time_mean, quest_resp_time_med,
                        quest_resp_time_without_latency_mean, quest_resp_time_without_latency_med,
                        charging_phone_count, charging_phone_dur,
                        watch_full_notif_count, watch_battery_low_notif_count,
                        watch_service_not_run_notif_count, watch_update_notif_count, watch_turn_off_dnd_notif_count,
                        watch_connect_notf_count, phone_unlocks, loc_data_mins, num_loc_clusters,
                        non_microt_notif_count, unique_app_count,
                        daily_step_count, watch_accel_summary, watch_sampling_rate_range,
                        watch_available_memory, watch_available_RAM, phone_wifi_off_min,
                        phone_logs_size, phone_data_size, watch_logs_size,
                        watch_data_size, watch_data_collected_hr, samples_collected]
            report_df.loc[avail_date] = data_row

    report_df.sort_index(inplace=True)

    with open(report_file_path, "w", newline='') as report_file:
        report_df.to_csv(report_file, index=False)
    print("Report generation completed for: " + user_name)

    # delete_folder_tree(temp_folder_path)
    delete_file(user_path + sep + LAST_RECORDED_SLEEP_FILE)
    # Reset watch_assigned to False before computing for the next user
    watch_assigned = False
    if delete_raw == 'TRUE':
        log_folder = root_path + sep + 'logs' + sep + date_to_run
        data_folder = root_path + sep + 'data' + sep + date_to_run
        logs_watch_folder = root_path + sep + 'logs-watch' + sep + date_to_run
        delete_folder_tree(log_folder)
        delete_folder_tree(data_folder)
        delete_folder_tree(logs_watch_folder)
    script_end_time_dt = datetime.now()
    script_end_time = time.time()
    print("Actual start time: " + str(script_start_time_dt.strftime("%m/%d/%Y, %H:%M:%S")))
    print("Actual end time: " + str(script_end_time_dt.strftime("%m/%d/%Y, %H:%M:%S")))
    print("Execution time for daily report = " + str(script_end_time - script_start_time) + " secs")


if __name__ == "__main__":
    main(root_path, date_to_run, delete_raw)
