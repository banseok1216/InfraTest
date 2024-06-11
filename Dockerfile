# 사용할 기본 이미지를 지정합니다.
FROM python:3.8-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# Flask 및 pika 패키지를 직접 설치합니다.
RUN pip install Flask pika

# 호스트의 현재 디렉토리에 있는 모든 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY . /app

# 컨테이너 내에서 실행될 명령을 지정합니다.
CMD ["python", "app.py"]
