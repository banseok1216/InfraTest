from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import pika
import json
import os
import time

app = Flask(__name__)

scheduler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')

# 경로 상수 정의
HARDWARE_INFO_PATH = '/data/hardware_info.txt'
SOFTWARE_INFO_PATH = '/data/software_info.txt'
PROC_STAT_PATH = '/proc/stat'
MEMINFO_PATH = '/proc/meminfo'


def send_to_rabbitmq(queue, data):
    """Send data to RabbitMQ."""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq.rabbitmq', 5672, credentials=pika.PlainCredentials('admin', 'admin'))
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='direct', routing_key=queue, body=json.dumps(data))
        connection.close()
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {str(e)}")


def read_resource_file(file_path):
    """Read content from a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read file {file_path}: {str(e)}")
        return None


def resource_job():
    """Read hardware and software info and send to RabbitMQ."""
    hardware_info = read_resource_file(HARDWARE_INFO_PATH)
    if hardware_info:
        send_to_rabbitmq("hardware_info_queue", hardware_info)

    software_info = read_resource_file(SOFTWARE_INFO_PATH)
    if software_info:
        send_to_rabbitmq("software_info_queue", software_info)


def calculate_memory_usage():
    """Calculate memory usage percentage."""
    with open(MEMINFO_PATH, 'r') as f:
        meminfo = f.readlines()
    mem_total = int(meminfo[0].split()[1])
    mem_available = int(meminfo[2].split()[1])
    memory_usage = ((mem_total - mem_available) / mem_total) * 100
    return memory_usage


def calculate_disk_usage():
    """Calculate disk usage percentage."""
    statvfs = os.statvfs('/')
    disk_total = statvfs.f_frsize * statvfs.f_blocks
    disk_free = statvfs.f_frsize * statvfs.f_bfree
    disk_used = disk_total - disk_free
    disk_usage = (disk_used / disk_total) * 100
    return disk_usage


def read_cpu_stat():
    """Read CPU statistics from /proc/stat."""
    with open(PROC_STAT_PATH, 'r') as f:
        lines = f.readlines()
    line = lines[0]
    parts = line.split()
    total = sum(int(part) for part in parts[1:])
    idle = int(parts[4])
    return total, idle


previous_total, previous_idle = read_cpu_stat()


def calculate_cpu_usage():
    """Calculate CPU usage percentage."""
    global previous_total, previous_idle
    current_total, current_idle = read_cpu_stat()
    total_diff = current_total - previous_total
    idle_diff = current_idle - previous_idle
    usage = (total_diff - idle_diff) / total_diff * 100
    previous_total, previous_idle = current_total, current_idle
    return usage


def system_info_job():
    """Collect and send system info."""
    try:
        cpu_usage = calculate_cpu_usage()
        memory_usage = calculate_memory_usage()
        disk_usage = calculate_disk_usage()
        send_to_rabbitmq("system_info", {cpu_usage, memory_usage, disk_usage})

    except Exception as e:
        print(f"Failed to collect or process system info: {str(e)}")


scheduler.add_job(system_info_job, IntervalTrigger(minutes=5), id='system_info_job')
scheduler.add_job(resource_job, IntervalTrigger(hours=1), id='resource_job')

# Start the scheduler
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
