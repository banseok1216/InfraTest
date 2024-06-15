import psutil
from utils_batch import ensure_log_directory, write_to_log, generate_log_file_name

LOG_DIR = '/home/admin/batch/log/usage'


def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"CPU 사용률: {cpu_usage}%"

def get_disk_usage():
    partitions = psutil.disk_partitions()
    disk_usage = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage.append(f"{partition.mountpoint}: {usage.percent}%")
    return "\n".join(disk_usage)

def get_memory_usage():
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    return f"메모리 사용률: {mem_usage}%"

def job():
    """작업 수행 함수"""
    ensure_log_directory(LOG_DIR)  # LOG_DIR 인자 필요
    cpu_usage = get_cpu_usage()
    disk_usage = get_disk_usage()
    mem_usage = get_memory_usage()

    message = f"{cpu_usage}\n\n디스크 사용률:\n{disk_usage}\n\n{mem_usage}"

    log_file = generate_log_file_name(LOG_DIR, "usage_info")  # LOG_DIR와 prefix 인자 필요
    write_to_log(log_file, message)

if __name__ == "__main__":
    job()
