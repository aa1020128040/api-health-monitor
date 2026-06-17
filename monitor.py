import requests
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "https://api.github.com"
CHECK_INTERVAL = 60

def send_alert(message):
    """模拟发送报警邮件/通知"""
    logging.info(f"--- 报警已触发: {message} ---")

def check_api():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            logging.info(f"API 运行正常! 状态码: {response.status_code}")
        else:
            msg = f"API 异常! 状态码: {response.status_code}"
            logging.warning(msg)
            send_alert(msg)
    except Exception as e:
        msg = f"连接失败: {e}"
        logging.error(msg)
        send_alert(msg)

if __name__ == "__main__":
    logging.info("监控服务启动...")
    while True:
        check_api()
        time.sleep(CHECK_INTERVAL)
