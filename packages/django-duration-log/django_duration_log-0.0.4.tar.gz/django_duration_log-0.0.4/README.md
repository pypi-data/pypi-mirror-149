## Django Duration Log

### 注册到 `installed_apps` 中

```python
INSTALLED_APPS = [
    "corsheaders",
    "django_duration_log",
    ···
]
```

### 添加 `middleware`

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_duration_log.middlewares.DjangoDurationLogMiddleware",
    ···
]
```

### 配置环境变量

```python
INFLUXDB_ACCESS_TOKEN = os.getenv("INFLUXDB_ACCESS_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
```
