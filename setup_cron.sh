PYTHON_SYSTEM_INFO_SCRIPT="/root/batch/batch.py"
PYTHON_SYSTEM_USAGE_SCRIPT="/root/batch/usage.py"

# PYTHON_SYSTEM_INFO_SCRIPT에 대한 crontab 등록
(crontab -l | grep -v "$PYTHON_SYSTEM_INFO_SCRIPT" ; \
 echo "* * * * * python3 $PYTHON_SYSTEM_INFO_SCRIPT >> /root/output.log 2>> /root/error.log") | crontab -

# PYTHON_SYSTEM_USAGE_SCRIPT에 대한 crontab 등록
(crontab -l | grep -v "$PYTHON_SYSTEM_USAGE_SCRIPT" ; \
 echo "* * * * * python3 $PYTHON_SYSTEM_USAGE_SCRIPT >> /root/output.log 2>> /root/error.log") | crontab -
