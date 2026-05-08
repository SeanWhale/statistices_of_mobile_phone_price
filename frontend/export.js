// frontend/export.js

async function exportWithTimeout() {
    // 1. 设置 5 秒超时控制器
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    try {
        console.log("正在请求数据（带超时监测）...");

        // 2. 发起请求，并将 signal 传给 fetch
        const response = await fetch("http://127.0.0.1:4010/api/export", {
            signal: controller.signal
        });

        if (response.status === 400) {
            alert("错误：当前没有可导出的数据！");
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        alert("数据获取成功！");
    } catch (error) {
        // 3. 捕获超时或异常情况
        if (error.name === 'AbortError') {
            console.error("请求超时：服务器响应太慢了！");
            alert("系统繁忙：后端响应超时，请检查网络或稍后再试。"); // 展现层逻辑闭环
        } else {
            console.error("请求失败：", error);
            alert("网络异常，请联系管理员。");
        }
    } finally {
        clearTimeout(timeoutId);
    }
}

if (typeof window !== "undefined") {
    window.exportWithTimeout = exportWithTimeout;
}
