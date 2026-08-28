# sisa-eltdx

eltdx × SIDA 适配层。用 eltdx 的 7709 端口直连通达信，替代 SIDA 的 TQ HTTP 网关，零依赖 TQ 后端。

## 架构

```
eltdx (7709) → sida_adapter.py → SIDA Vendor 接口
  ├── EltdxQuoteVendor   (实时行情)
  ├── EltdxKlineVendor   (日K/分钟K)
  └── EltdxMoreInfoVendor (换手率/量比/PB/市值等)
```

## 使用

1. 构建镜像：`docker build -t shit6/sida-eltdx .`
2. 替换 SIDA 主镜像：在 `docker-compose.yml` 中将 `panwatch` 改为 `shit6/sida-eltdx`
3. 数据源设置为 `eltdx`

## 自动构建

上游 [electkismet/eltdx](https://github.com/electkismet/eltdx) 有新 release 时，GitHub Actions 自动构建 `shit6/sida-eltdx` 镜像。

## SIDA 适配说明

- `docker_resources/registry.py`：在 SIDA `VENDOR_CLASSES_BY_TYPE` 中注入 eltdx 三个 vendor
- `docker_resources/start_eltdx.sh`：运行时解压 wheel + 设置 PYTHONPATH
- 无需修改 SIDA 源代码
