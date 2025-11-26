from django.apps import AppConfig


class ConfessionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'confession'

    def ready(self):
        # 导入信号处理器
        import confession.signals