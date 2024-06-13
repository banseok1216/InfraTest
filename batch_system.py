from datetime import datetime
import psutil

# 데이터를 수집하는 함수
def collect_system_info():
    # CPU 정보 수집
    cpu_percent = psutil.cpu_percent()

    # 메모리 정보 수집
    mem = psutil.virtual_memory()
    mem_total = mem.total
    mem_used = mem.used
    mem_percent = mem.percent

    # 디스크 정보 수집
    disk = psutil.disk_usage('/')
    disk_total = disk.total
    disk_used = disk.used
    disk_percent = disk.percent

    return {
        'cpu_percent': cpu_percent,
        'mem_total': mem_total,
        'mem_used': mem_used,
        'mem_percent': mem_percent,
        'disk_total': disk_total,
        'disk_used': disk_used,
        'disk_percent': disk_percent
    }

# 데이터를 텍스트 파일에 저장하는 함수
def save_data_to_txt(data, file_path):
    with open(file_path, 'a') as file:
        file.write("시간: {}\n".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))  # 현재 시간을 문자열로 변환하여 추가
        file.write("CPU 사용율: {}%\n".format(data['cpu_percent']))
        file.write("전체 메모리: {:.2f} GB\n".format(data['mem_total'] / (1024 ** 3)))
        file.write("사용 중인 메모리: {:.2f} GB\n".format(data['mem_used'] / (1024 ** 3)))
        file.write("메모리 사용율: {}%\n".format(data['mem_percent']))
        file.write("전체 디스크 공간: {:.2f} GB\n".format(data['disk_total'] / (1024 ** 3)))
        file.write("사용 중인 디스크 공간: {:.2f} GB\n".format(data['disk_used'] / (1024 ** 3)))
        file.write("디스크 사용율: {}%\n".format(data['disk_percent']))
        file.write("\n")

def main():
    # 시스템 정보 수집
    system_info = collect_system_info()

    # 로그 파일 이름 설정
    log_file_name = '/root/system_info_log_{}.txt'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    # 데이터 파일에 저장
    save_data_to_txt(system_info, log_file_name)

    print("데이터가 {}에 추가되었습니다.".format(log_file_name))

if __name__ == "__main__":
    main()
