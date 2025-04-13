from django.urls import path, include
from django.conf import settings

API_VERSION = getattr(settings, 'API_VERSION', 1)

path_string = f"api/v{API_VERSION}/"
folder_string = f"shared.urls.v{API_VERSION}"

urlpatterns = [
    path(path_string, include(folder_string)),
]
