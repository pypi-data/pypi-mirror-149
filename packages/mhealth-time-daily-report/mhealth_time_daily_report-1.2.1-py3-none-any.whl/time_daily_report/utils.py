import shutil
from os import path
import os
import json
import importlib.resources
import pkgutil
import pytz
from datetime import timedelta, datetime

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
time_offset_dict = {
    "CDT": "America/Indiana/Knox",
    "CST": "America/Indiana/Knox",
    "MDT": "America/Denver",
    "MST": "America/Denver",
    "PDT": "US/Pacific",
    "PST": "US/Pacific",
    "EDT": "US/Eastern",
    "EST": "US/Eastern",
    "AKDT": "US/Alaska",
    "AKST": "US/Alaska",
    "HDT": "US/Aleutian",
    "HST": "US/Aleutian",
    "AST": "America/Aruba"
}


def delete_folder_tree(folder_path):
    if path.exists(folder_path):
        print("Recursively deleting dir tree @: " + folder_path)
        try:
            shutil.rmtree(folder_path)
        except:
            print("Error while deleting temp folder")
    else:
        print("No directory exists @: " + folder_path)


def delete_file(file_path):
    if path.exists(file_path):
        print("Removing file: " + str(file_path))
        try:
            os.remove(file_path)
        except:
            print("Error deleting the file: " + file_path)
    else:
        print("No such file exists: " + file_path)


def load_validation_json():
    # with open('validation_key_ans.json', 'r') as openfile:
    #     valid_key_ans_dict = json.load(openfile)
    #     return valid_key_ans_dict
    json_data = pkgutil.get_data('time_daily_report', 'validation_key_ans.json')
    return json.loads(json_data)
    # with importlib.resources.path('time_daily_report', 'validation_key_ans.json') as openfile:
    #     valid_key_ans_dict = json.load(openfile)
    #     return valid_key_ans_dict


# whether a given time occurs during DST for a specific timezone
def is_dst(dt, timezone):
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


def map_tzStr_to_pytz(time_offset_dict, time_zone_str):
    if time_zone_str in time_offset_dict:
        time_zone_name = time_offset_dict[time_zone_str]
    else:
        time_zone_name = "null"
    return time_zone_name


def check_daylight_saving(avail_date, current_wake_time):
    if current_wake_time == "null":
        return "null"

    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    time_offset_dict = {
        "CDT": "America/Indiana/Knox",
        "CST": "America/Indiana/Knox",
        "MDT": "America/Denver",
        "MST": "America/Denver",
        "PDT": "US/Pacific",
        "PST": "US/Pacific",
        "EDT": "US/Eastern",
        "EST": "US/Eastern",
        "AKDT": "US/Alaska",
        "AKST": "US/Alaska",
        "HDT": "US/Aleutian",
        "HST": "US/Aleutian",
        "AST": "America/Aruba"
    }

    time_zone_str = current_wake_time.split(" ")[-1]
    time_zone_pytz = map_tzStr_to_pytz(time_offset_dict, time_zone_str)
    if time_zone_pytz == "null":
        return "null"
    #
    avail_date_components = avail_date.split("-")
    date_dt = datetime(int(avail_date_components[0]), int(avail_date_components[1]), int(avail_date_components[2])) + timedelta(days=1)
    # is_dst(datetime(2022, 3, 13) + timedelta(days=1), timezone="US/Eastern")
    # is_dst(datetime(2022, 3, 13) + timedelta(days=1), timezone="America/Aruba")
    daylight_saving = is_dst(date_dt, timezone=time_zone_pytz)
    return daylight_saving
