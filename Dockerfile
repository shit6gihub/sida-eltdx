FROM shit6/panwatch:latest

# 安装 eltdx（用 7709 端口直连通达信，替代 TQ HTTP 网关）
# 从 GitHub Releases 下载最新 wheel
ARG ELTDX_VERSION=3.0.7
ARG ELTDX_WHEEL_URL=https://github.com/electkismet/eltdx/releases/download/v${ELTDX_VERSION}/eltdx-${ELTDX_VERSION}-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# 复制 SIDA 适配代码
COPY docker_resources/start_eltdx.sh /usr/local/bin/start_eltdx.sh
RUN chmod +x /usr/local/bin/start_eltdx.sh

# 下载并安装 eltdx wheel
RUN set -eux; \
    curl -fSL --connect-timeout 30 --max-time 120 \
      -o /tmp/eltdx.whl "${ELTDX_WHEEL_URL}" && \
    pip install --no-cache-dir /tmp/eltdx.whl && \
    rm -f /tmp/eltdx.whl

# 替换 SIDA registry.py，注入 eltdx vendor
COPY docker_resources/registry.py /app/packages/marketdata/src/marketdata/registry.py

# 设置环境变量
ENV PYTHONPATH=/app/packages/marketdata/src/marketdata:/app/packages/marketdata/eltdx_src
ENV ELTDX_ENABLED=1

# 用 start_eltdx.sh 覆盖入口点
ENTRYPOINT ["/usr/local/bin/start_eltdx.sh"]
CMD ["python", "server.py"]
