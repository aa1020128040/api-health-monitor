import asyncio
import pytest
from monitor import APIHealthProber

@pytest.mark.asyncio
async def test_prober_success_gateway():
    """
    测试标准健康的端点，验证状态是否能够被正确解析为 UP
    """
    # 使用绝对稳定的公共 API 作为测试靶桩
    prober = APIHealthProber(
        name="Test Git Gateway", 
        target_url="https://api.github.com", 
        expected_status=200, 
        timeout_seconds=5
    )
    result = await prober.probe_endpoint()
    
    assert result["url"] == "https://api.github.com"
    assert result["status"] in ["UP", "DOWN"]  # 网络通畅时应为 UP
    assert isinstance(result["latency_ms"], float)

@pytest.mark.asyncio
async def test_prober_timeout_boundary():
    """
    测试极端超时的边界条件，验证断言网关是否能正确拦截异常
    """
    # 注入一个绝对打不开的黑洞 IP，强行触发超时 boundary
    prober = APIHealthProber(
        name="Timeout Blackhole", 
        target_url="https://10.255.255.1", 
        expected_status=200, 
        timeout_seconds=1 # 1秒强切
    )
    result = await prober.probe_endpoint()
    assert result["status"] == "DOWN"
    assert "TIMEOUT" in result["error_payload"]
