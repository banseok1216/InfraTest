from flask import Flask, request, jsonify, json
import pika

app = Flask(__name__)


def send_to_rabbitmq(hardware_info, software_info):
    # RabbitMQ 서비스에 연결
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq.rabbitmq', 5672, credentials=pika.PlainCredentials('admin', 'admin')))
    channel = connection.channel()

    # 큐(Queue) 선언
    channel.queue_declare(queue='hardware_software_info_queue')

    channel.basic_publish(exchange='', routing_key='hardware_software_info_queue',
                          body=json.dumps({"hardware_info": hardware_info, "software_info": software_info}))

    # 연결 종료
    connection.close()
@app.route('/hardware_software_info', methods=['POST'])
def receive_hardware_software_info():
    try:
        data = request.get_json()
        hardware_info = data.get('hardware_info')
        software_info = data.get('software_info')
        if hardware_info and software_info:
            # RabbitMQ로 데이터 전송
            send_to_rabbitmq(hardware_info, software_info)
            # 성공 응답 반환
            return jsonify({"message": "success"}), 200
    except Exception as e:
        # 예외가 발생한 경우 오류 응답 반환
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
