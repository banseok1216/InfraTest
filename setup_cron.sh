PYTHON_SYSTEM_INFO_SCRIPT="/home/admin/batch/software_hardware_batch.py"
PYTHON_SYSTEM_USAGE_SCRIPT="/home/admin/batch/usage_batch.py"

# PYTHON_SYSTEM_INFO_SCRIPT에 대한 crontab 등록
(crontab -l | grep -v "$PYTHON_SYSTEM_INFO_SCRIPT" ; \
 echo "* * * * * python3 $PYTHON_SYSTEM_INFO_SCRIPT >> /home/admin/log/output.log 2>> /home/admin/log/error.log") | crontab -

# PYTHON_SYSTEM_USAGE_SCRIPT에 대한 crontab 등록
(crontab -l | grep -v "$PYTHON_SYSTEM_USAGE_SCRIPT" ; \
 echo "* * * * * python3 $PYTHON_SYSTEM_USAGE_SCRIPT >> /home/admin/log/output.log 2>> /home/admin/log/error.log") | crontab -
