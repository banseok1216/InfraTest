import os
import glob
import time
from datetime import datetime, timedelta, timezone
import sys

import pika
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
KST = timezone(timedelta(hours=9))
scheduler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')

HARDWARE_INFO_PATH = '/host-data/hardware/hardware_info_log_*'
SOFTWARE_INFO_PATH = '/host-data/software/software_info_log_*'
RESOURCE_USAGE_INFO_PATH = '/host-data/usage/usage_info_log_*'


def read_file(file_path):
    """Read content from a file."""
    try:
        files = glob.glob(file_path)
        recent_file = max(files, key=os.path.getmtime)
        print(recent_file)
        with open(recent_file, 'r') as file:
            return file.read()
    except Exception as e:
        current_time = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{current_time} - 읽기 실패 {file_path}: {str(e)}",file=sys.stderr, flush=True)
        return None


def system_job():
    """하드웨어 정보와 소프트웨어 정보를 RabbitMQ로 전송"""
    hardware_info = read_file(HARDWARE_INFO_PATH)
    if hardware_info:
        send_to_rabbitmq("hardware_info_queue", hardware_info)

    software_info = read_file(SOFTWARE_INFO_PATH)
    if software_info:
        send_to_rabbitmq("software_info_queue", software_info)


def resource_usage_job():
    """리소스 사용 정보를 RabbitMQ로 전송"""
    resource_usage_info = read_file(RESOURCE_USAGE_INFO_PATH)
    if resource_usage_info:
        send_to_rabbitmq("system_usage_info_queue", resource_usage_info)


def send_to_rabbitmq(queue, data):
    """Send data to RabbitMQ with retry logic."""
    max_retries = 3
    current_time = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')
    for attempt in range(max_retries):
        try:
            # connection = pika.BlockingConnection(
            #     pika.ConnectionParameters('rabbitmq.rabbitmq', 5672,
            #                               credentials=pika.PlainCredentials('admin', 'admin'))
            # )
            # channel = connection.channel()
            # channel.queue_declare(queue=queue)
            # channel.basic_publish(exchange='direct', routing_key=queue, body=json.dumps(data))
            # connection.close()
            print(f"{current_time} - 메시지 전송 성공 {attempt + 1}",file=sys.stdout,flush=True)
            break
        except Exception as e:
            print(f"{current_time} - 메시지 전송 시도 {attempt + 1} 실패: {str(e)}",file=sys.stderr,flush=True)
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"{current_time} - 메시지 전송 시도 3번 실패: {str(e)}",file=sys.stderr,flush=True)


scheduler.add_job(resource_usage_job, 'cron', minute='*', second='5', id='resource_usage_job')
scheduler.add_job(system_job, 'cron', minute='*', second='5', id='system_job')

# Start the scheduler
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
