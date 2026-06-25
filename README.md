# 🚀 api-health-monitor

一个轻量级的、Docker化的、基于异步I/O架构的 API 端点健康状况与响应延迟监控工具。Perfect for edge deployment and cloud-native observability.

---

## ✨ 特征 (Features)

* **⚡ 高性能异步探测:** 基于 Python `asyncio` 与 `httpx` 弹性网络连接池，支持多端点毫秒级非阻塞并发网络状态追踪。
* **📦 容器化无状态设计:** 完美适配 Docker 边缘部署，零重型数据库依赖，镜像体极度轻量。
* **📋 结构化日志输出:** 全量输出标准 JSON 格式日志，原生兼容 Grafana Loki、ELK 等现代云原生日志收集链。
* **🛡️ 自动化测试保障:** 项目内嵌完整的自动化单元测试桩 (`test_monitor.py`)，全量覆盖了 API 成功响应与网络超时等核心边界场景。

---

## 🚀 快速启动 (Quick Start)

### Option 1: Run via Docker (Recommended)
```bash
docker build -t api-health-monitor .
docker run --rm --name monitor-runtime api-health-monitor
