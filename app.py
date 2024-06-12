from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import pika
import json

app = Flask(__name__)


def send_to_rabbitmq(hardware_info, software_info):
    # RabbitMQ 서비스에 연결
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq.rabbitmq', 5672, credentials=pika.PlainCredentials('admin', 'admin')))
    channel = connection.channel()

    # 큐(Queue) 선언
    channel.queue_declare(queue='hardware_software_info_queue')

    channel.basic_publish(exchange='', routing_key='hardware_software_info_queue',
                          body=json.dumps({"hardware_info": hardware_info, "software_info": software_info}))

    # 연결 종료
    connection.close()


def job():
    try:
        with open('/data/hardware_info.txt', 'r') as hardware_file:
            hardware_info = hardware_file.read()
        with open('/data/software_info.txt', 'r') as software_file:
            software_info = software_file.read()
        send_to_rabbitmq(hardware_info, software_info)
    except Exception as e:
        print(f"데이터 읽기 실패: {str(e)}")

schedule = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
schedule.add_job(job, 'interval', seconds=3)
schedule.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
