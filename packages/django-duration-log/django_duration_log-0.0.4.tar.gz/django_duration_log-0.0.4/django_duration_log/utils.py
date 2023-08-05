from django.conf import settings
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS


def get_ip(request):
    if request.META.get("HTTP_X_REAL_IP"):
        return request.META.get("HTTP_X_REAL_IP")
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META.get("HTTP_X_FORWARDED_FOR").replace(" ", "").split(",")[0]
    return request.META.get("REMOTE_ADDR")


class GlobalLogExtraFuncMixin:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class SaveLogHandler:
    def __init__(self):
        self.token = settings.INFLUXDB_ACCESS_TOKEN
        self.org = settings.INFLUXDB_ORG
        self.bucket = settings.INFLUXDB_BUCKET
        self.url = settings.INFLUXDB_URL

    def save_log(self, detail):
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
            write_api = client.write_api(write_options=ASYNCHRONOUS)
            data = "duration,{tags} {fields}".format(
                tags=",".join([f"{key}={val}" for key, val in detail["tags"].items()]),
                fields=",".join(
                    [f"{key}={val}" for key, val in detail["fields"].items()]
                ),
            )
            write_api.write(self.bucket, self.org, data)
