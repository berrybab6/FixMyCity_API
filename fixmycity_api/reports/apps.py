from django.apps import AppConfig
import os
from django.conf import settings
import joblib 


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    # MODEL_FILE = os.path.join(settings.MODELS, "imageidentification.joblib")
    # model = joblib.load(MODEL_FILE)
