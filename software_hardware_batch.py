import subprocess
from utils_batch import ensure_log_directory, write_to_log, generate_log_file_name

SOFTWARE_LOG_DIR = '/home/admin/batch/log/software'
HARDWARE_LOG_DIR = '/home/admin/batch/log/hardware'

def run_command(command):
    """명령어를 실행하고 결과를 반환하는 함수"""
    try:
        output = subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.STDOUT
        )
        return output.strip()
    except Exception as e:
        return str(e)

def collect_hardware_info():
    """하드웨어 정보를 수집하는 함수"""
    command = "lshw"
    output = run_command(command)
    log_file = generate_log_file_name(HARDWARE_LOG_DIR, "hardware_info")
    write_to_log(log_file, output)

def collect_software_info():
    """소프트웨어 정보를 수집하는 함수"""
    command = "lsmod"
    output = run_command(command)
    log_file = generate_log_file_name(SOFTWARE_LOG_DIR, "software_info")
    write_to_log(log_file, output)

def job():
    """작업 수행 함수"""
    ensure_log_directory(SOFTWARE_LOG_DIR)
    ensure_log_directory(HARDWARE_LOG_DIR)
    collect_hardware_info()
    collect_software_info()

if __name__ == "__main__":
    job()
