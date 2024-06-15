import time
from datetime import datetime

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import json
import pika
from system_info import resource_usage_job

app = Flask(__name__)

scheduler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')

def send_to_rabbitmq(queue, data):
    """Send data to RabbitMQ with retry logic."""
    max_retries = 3
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for attempt in range(max_retries):
        try:
            # connection = pika.BlockingConnection(
            #     pika.ConnectionParameters('rabbitmq.rabbitmq', 5672, credentials=pika.PlainCredentials('admin', 'admin'))
            # )
            # channel = connection.channel()
            # channel.queue_declare(queue=queue)
            # channel.basic_publish(exchange='direct', routing_key=queue, body=json.dumps(data))
            # connection.close()
            print(f"{current_time} - 메시지 전송 성공 {attempt + 1}")
            break
        except Exception as e:
            print(f"{current_time} - 메시지 전송 시도 {attempt + 1} 실패: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"{current_time} - 메시지 전송 시도 3번 실패: {str(e)}")

scheduler.add_job(resource_usage_job, 'cron', minute='*', second='1', id='batch_job')

# Start the scheduler
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
