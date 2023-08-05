from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_duration_log"
    verbose_name = _("Django请求耗时日志")
