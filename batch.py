import subprocess
import schedule
import time
from datetime import datetime

def collect_hardware_info(file_path):
    command = "lshw"
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        with open(file_path, 'w') as output_file:
            output_file.write("시간: {}\n".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))  # 현재 시간을 문자열로 변환하여 추가
            output_file.write(output)
        print("하드웨어 정보 수집 완료")
        return output
    except subprocess.CalledProcessError as e:
        print("하드웨어 정보 수집 중 에러 발생:", e)
    except Exception as e:
        print("예외 발생:", e)

def collect_software_info(file_path):
    command = "lsmod"
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        with open(file_path, 'w') as output_file:
            output_file.write("시간: {}\n".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))  # 현재 시간을 문자열로 변환하여 추가
            output_file.write(output)
        print("소프트웨어 정보 수집 완료")
        return output
    except subprocess.CalledProcessError as e:
        print("소프트웨어 정보 수집 중 에러 발생:", e)
    except Exception as e:
        print("예외 발생:", e)

def job():
    file_path_hw = '/root/hardware_info_log_{}.txt'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    collect_hardware_info(file_path_hw)
    file_path_sw = '/root/software_info_log_{}.txt'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    collect_software_info(file_path_sw)


if __name__ == "__main__":
    schedule.every().second.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)