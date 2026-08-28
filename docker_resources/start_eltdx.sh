#!/bin/sh
# eltdx SIDA adapter startup script
# 运行时解压 eltdx wheel 到可写目录，设置 PYTHONPATH，然后启动 SIDA

ELTDX_WHEEL="/assets/eltdx-${ELTDX_VERSION:-3.0.7}-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
ELTDX_INSTALL="/tmp/eltdx_install"

# 确保 /assets 目录存在（挂载卷或内置 wheel）
if [ ! -f "${ELTDX_WHEEL}" ]; then
    echo "[eltdx] ⚠️ Wheel not found at ${ELTDX_WHEEL}, skipping eltdx"
    exec "$@"
fi

# 解压 wheel 到可写位置
if [ ! -f "${ELTDX_INSTALL}/eltdx/__init__.py" ]; then
    mkdir -p "${ELTDX_INSTALL}"
    python3 -c "
import zipfile, os
target = '${ELTDX_INSTALL}'
with zipfile.ZipFile('${ELTDX_WHEEL}') as z:
    for name in z.namelist():
        if name.startswith('eltdx/') and name != 'eltdx/':
            dest = os.path.join(target, name)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(name) as src, open(dest, 'wb') as dst:
                dst.write(src.read())
print('[eltdx] Wheel extracted to', target)
"
fi

# 设置 PYTHONPATH
export PYTHONPATH="${ELTDX_INSTALL}:${PYTHONPATH}"
echo "[eltdx] PYTHONPATH=${PYTHONPATH}"

# 执行原始入口点
exec "$@"
