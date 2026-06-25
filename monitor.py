import asyncio
import httpx
import time
import logging
import sys
import json
import os

# 全面改用标准结构化 JSON 日志，原生适配 Grafana Loki / ELK 收集系统
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "metrics": %(message)s}',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class APIHealthProber:
    def __init__(self, name: str, target_url: str, expected_status: int = 200, timeout_seconds: int = 5):
        self.name = name
        self.target_url = target_url
        self.expected_status = expected_status
        self.timeout = timeout_seconds

    async def probe_endpoint(self) -> dict:
        """
        利用 Asyncio + HTTPX 异步连接池，支持毫秒级非阻塞并发探测
        """
        start_time = time.perf_counter()
        status = "DOWN"
        latency_ms = 0.0
        error_msg = None

        async with httpx.AsyncClient(timeout=self.timeout, http2=True) as client:
            try:
                response = await client.get(self.target_url, follow_redirects=True)
                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                
                # 动态断言校验
                if response.status_code == self.expected_status:
                    status = "UP"
                else:
                    error_msg = f"HTTP_STATUS_MISMATCH_{response.status_code}"
            except httpx.TimeoutException:
                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                error_msg = "NETWORK_TIMEOUT_LIMIT_EXCEEDED"
            except httpx.RequestError as exc:
                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                error_msg = f"NETWORK_EXCEPTION_{type(exc).__name__.upper()}"

        return {
            "name": self.name,
            "url": self.target_url,
            "status": status,
            "latency_ms": latency_ms,
            "error_payload": error_msg
        }

async def runtime_scheduler():
    config_path = "config.json"
    
    # 防御性编程：检查配置文件是否存在
    if not os.path.exists(config_path):
        logging.error('"Missing vital config.json file. Runtime aborted."')
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    timeout = config["settings"]["global_timeout_seconds"]
    endpoints = config["endpoints"]
    
    # 动态组装异步任务切片
    prober_tasks = [
        APIHealthProber(ep["name"], ep["url"], ep["expected_status"], timeout).probe_endpoint() 
        for ep in endpoints
    ]
    
    # 瞬间并行发射
    results = await asyncio.gather(*prober_tasks)
    
    for result in results:
        # 严格序列化为单行标准 JSON，防止分布式日志收集时发生格式碎裂
        log_payload = (
            f'{{"target": "{result["name"]}", "url": "{result["url"]}", "status": "{result["status"]}", '
            f'"latency_ms": {result["latency_ms"]}, "error": '
            f'{"null" if result["error_payload"] is None else f"\\"{result["error_payload"]}\\""}}}'
        )
        logging.info(log_payload)

if __name__ == "__main__":
    asyncio.run(runtime_scheduler())
