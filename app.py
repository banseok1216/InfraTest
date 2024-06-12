from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import pika
import json
import os

app = Flask(__name__)

schedule = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
def send_to_rabbitmq(key, info):
    try:
        # RabbitMQ 서비스에 연결
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq.rabbitmq', 5672, credentials=pika.PlainCredentials('admin', 'admin')))
        channel = connection.channel()

        channel.queue_declare(queue='monitoring')

        channel.basic_publish(exchange='direct', routing_key=key, body=json.dumps(info))

        connection.close()
    except Exception as e:
        print(f"RabbitMQ 연결 실패: {str(e)}")


def resource_job():
    try:
        with open('/data/hardware_info.txt', 'r') as hardware_file:
            hardware_info = hardware_file.read()
        send_to_rabbitmq("hardware_info_queue", hardware_info)
        with open('/data/software_info.txt', 'r') as software_file:
            software_info = software_file.read()
        send_to_rabbitmq("software_info_queue", software_info)
    except Exception as e:
        print(f"데이터 읽기 실패: {str(e)}")


def system_info_job():
    try:
        files = os.listdir('/data/system')
        # 가장 최근 파일 선택
        latest_file = max(files, key=os.path.getctime)
        # 파일 경로
        file_path = os.path.join('/data/system', latest_file)
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            system_info_text = file.read()
        if parse_system_info(system_info_text):
            schedule.modify_job('system_info_job', trigger=IntervalTrigger(minutes=10))
        else:
            schedule.modify_job('system_info_job', trigger=IntervalTrigger(minutes=5))
    except Exception as e:
        print(f"시스템 정보 읽기 및 처리 실패: {str(e)}")

def parse_system_info(system_info_text):
    lines = system_info_text.split('\n')
    for line in lines:
        if line.startswith('CPU 사용율:'):
            if float(line.split(': ')[1].strip('%')) > 80:
                return False
        elif line.startswith('메모리 사용율:'):
            if float(line.split(': ')[1].strip('%')) > 80:
                return False
        elif line.startswith('디스크 사용율:'):
            if float(line.split(': ')[1].strip('%')) > 80:
                return False
    return True

schedule.add_job(system_info_job, IntervalTrigger(minutes=10), id='system_info_job')
schedule.add_job(resource_job, IntervalTrigger(minutes=30), id='resource_job')
schedule.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
