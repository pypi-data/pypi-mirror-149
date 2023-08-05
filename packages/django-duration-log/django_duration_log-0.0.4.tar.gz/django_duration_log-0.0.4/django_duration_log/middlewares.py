import logging
import sys
import traceback
from timeit import default_timer as timer

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.module_loading import import_string

from django_duration_log.utils import SaveLogHandler, get_ip

logger = logging.getLogger("django")


class DjangoDurationLogMiddleware(MiddlewareMixin):
    """全局日志中间件"""

    req_start_time_key = "_influxdb_log_req_start_time"
    is_enabled = getattr(settings, "IS_USING_DURATION_LOG", False)

    def process_request(self, request):
        if not self.is_enabled:
            return None
        setattr(request, self.req_start_time_key, timer())
        return None

    def process_response(self, request, response):
        if not self.is_enabled:
            return response
        try:
            self.log(request, response)
            logger.info("[InfluxDB Logging Success]")
        except Exception as err:
            msg = traceback.format_exc()
            logger.error("[InfluxDB Logging Failed] %s\n%s", str(err), msg)
        return response

    def log(self, request, response):
        req_end_time = timer()
        req_start_time = getattr(request, self.req_start_time_key, req_end_time)
        duration = int((req_end_time - req_start_time) * 1000)
        log_detail = {
            "tags": {
                "operator": getattr(request.user, "pk", ""),
                "path": request.path,
                "method": request.method,
                "ip": get_ip(request),
                "code": response.status_code,
                **self.build_extras(request, response),
            },
            "fields": {
                "duration": duration,
            },
        }
        self.save(log_detail)

    def save(self, detail):
        custom_save_func_string = getattr(settings, "DURATION_LOG_ASYNC_SAVE_FUNC", None)
        if custom_save_func_string:
            try:
                custom_save_func = import_string(custom_save_func_string)
                custom_save_func.delay(detail)
            except Exception as err:
                msg = traceback.format_exc()
                logger.error(
                    "[Custom Log Save Func Error] %s\t%s\n%s",
                    custom_save_func_string,
                    err,
                    msg,
                )
                SaveLogHandler().save_log(detail)
        else:
            SaveLogHandler().save_log(detail)

    def build_extras(self, request, response):
        extra_func = getattr(settings, "DURATION_LOG_EXTRA_FUNC", {})
        extras = {}
        for key, func_string in extra_func.items():
            try:
                func = import_string(func_string)
                extras[key] = func(request, response)()
            except ImportError:
                logger.error("[Extra Log Func Not Exists] %s", func_string)
            except Exception as err:
                msg = traceback.format_exc()
                logger.error(
                    "[Extra Log Build Error] %s\t%s\n%s", func_string, err, msg
                )
        return extras
