import os
import datetime

HARDWARE_INFO_PATH = '/data/hardware/hardware_info_*.txt'
SOFTWARE_INFO_PATH = '/data/software/software_info_*.txt'
RESOURCE_USAGE_INFO_PATH = '/data/usage/software_info_*.txt'

from app import send_to_rabbitmq
import glob


def read_file(file_path):
    """Read content from a file."""
    try:
        files = glob.glob(file_path)
        recent_file = max(files, key=os.path.getmtime)
        print(recent_file)
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"읽기 실패 {file_path}: {str(e)}")
        return None


def system_job():
    """하드웨어 정보와 cpu 정브를 토대로 rabbitmq로 전송"""
    hardware_info = read_file(HARDWARE_INFO_PATH)
    if hardware_info:
        send_to_rabbitmq("hardware_info_queue", hardware_info)

    software_info = read_file(SOFTWARE_INFO_PATH)
    if software_info:
        send_to_rabbitmq("software_info_queue", software_info)


def resource_usage_job():
    """하드웨어 정보와 cpu 정브를 토대로 rabbitmq로 전송"""
    resource_usage_info = read_file(RESOURCE_USAGE_INFO_PATH)
    if resource_usage_info:
        send_to_rabbitmq("system_usage_info_queue", resource_usage_info)



