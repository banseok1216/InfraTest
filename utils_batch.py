
import os
from datetime import datetime
import sys


def ensure_log_directory(LOG_DIR):
    """로그 디렉토리가 없으면 생성하는 함수"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def write_to_log(log_file, message):
    """로그 파일에 메시지를 씁니다."""
    try:
        with open(log_file, 'a') as file:
            file.write(f"시간: {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}\n")
            file.write(message + "\n\n")
        print(f"{os.path.basename(log_file)} 파일에 정보를 기록했습니다.", file=sys.stdout)
    except Exception as e:
        error_message = f"{os.path.basename(log_file)} 파일 생성 중 예외 발생: {e}"
        print(error_message, file=sys.stderr)


def generate_log_file_name(log_dir, prefix):
    """로그 파일 이름을 생성하는 함수"""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"{log_dir}/{prefix}_log_{timestamp}.txt"