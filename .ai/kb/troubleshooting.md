# 常见问题排查

> 常见问题、调试流程、已知坑位。

## [+] sentence-transformers 安装失败

常见原因：numpy 版本不兼容旧版 PyTorch。现象为 `ModuleNotFoundError` 或 `AttributeError: module 'torch' has no attribute 'float8_e8m0fnu'`。解决方案：降级 numpy 到 1.x 和 transformers 到 4.x：
```
pip install "numpy<2" "transformers<5"
```
若 huggingface.co 不可达，设置环境变量 `HF_ENDPOINT=https://hf-mirror.com` 使用国内镜像下载模型。
