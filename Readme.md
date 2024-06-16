# 시스템 모니터링과 경보 시스템 설계

## 개요
이 문서는 Kubernetes 클러스터 내에서 DaemonSet을 사용하여 각 노드에서 하드웨어 정보를 수집하고 결과를 RabbitMQ를 통해 모니터링 서버로 전송하여 threshold 기준치를 확인하고 경보 알람을 설정하는 과정을 설명합니다.

## 구성 요소
- Kubernetes 클러스터
- crontab shell script
- 파이썬 script
- DaemonSet을 통해 배포된 파드
- RabbitMQ 메시지 브로커
- 모니터링 서버
- 경보 시스템

## 구현 단계
1. **노드의 정보를 crontab을 이용하여 생성**
   - Crontab을 이용하여 정해진 주기에 따라 정보를 수집하고 이 결과를 지정된 경로에 저장한다.
2. **DaemonSet 파드 구성**
   - Kubernetes YAML 파일을 사용하여 DaemonSet을 정의하고, 각 노드에 정보를 수집하는 파드를 배포합니다.
3. **호스트 노드의 정보 수집**
    - 호스트 노드의 정보가 위치한 경로에 파드의 경로를 read_only로 마운트하고 수집.이때 호스트 노드 생성 시간 기준 10초 delay를 주어 최신 정보를 반영하도록 설계
3. **RabbitMQ 설정**
   - RabbitMQ를 설치하고 설정하여, 호스트 노드가 생성한 정보를 메시지 큐에 전송하고 모니터링 서버로 라우팅합니다.
4. **모니터링 서버 설치 및 설정**
   - 모니터링 서버를 설치하고 RabbitMQ로부터 health check 결과를 구독하여 threshold 기준치를 확인하고 알림을 설정합니다.
5. **경보 시스템 설정**
   - 모니터링 서버는 threshold를 초과하는 경우에 경보 알람을 발생시킵니다.
6. **헬스 체크**
   - 모니터링 서버는 1초마다 모든 워커노드에 대해 ping을 통한 health check를 수행함.

## 시스템 아키텍처 다이어그램
(다이어그램 이미지를 여기에 넣으세요)

## 참고 자료
- [Kubernetes 공식 문서](https://kubernetes.io/docs/)
- [RabbitMQ 공식 문서](https://www.rabbitmq.com/documentation.html)
- [Prometheus 공식 문서](https://prometheus.io/docs/)
- [Grafana 공식 문서](https://grafana.com/docs/)

이 README.md 파일은 Kubernetes 클러스터에서 health check를 수행하고 모니터링 시스템을 구성하는 데 필요한 기본 개념과 단계를 제공합니다.
