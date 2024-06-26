BROKER_URL = "redis://redis:6379/1"
CELERY_RESULT_BACKEND = "redis://redis:6379/1"

# json serializer is more secure than the default pickle
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"

# Use UTC instead of localtime
CELERY_ENABLE_UTC = True

# Maximum retries per task
CELERY_TASK_ANNOTATIONS = {"*": {"max_retries": 3}}

# A custom property used in tasks.py:run()
CUSTOM_RETRY_DELAY = 10
