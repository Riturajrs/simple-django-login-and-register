import os

from django.core.wsgi import get_wsgi_application
from aws_lambda_wsgi import WSGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_wsgi_application()

def lambda_handler(event, context):
    return WSGIHandler(application).handle(event, context)
