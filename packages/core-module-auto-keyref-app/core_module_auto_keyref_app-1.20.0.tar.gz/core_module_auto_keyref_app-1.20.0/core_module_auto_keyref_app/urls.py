"""Url routing
"""

from django.urls import re_path

from core_module_auto_keyref_app.ajax import get_updated_keys
from core_module_auto_keyref_app.views import AutoKeyRefModule

urlpatterns = [
    re_path(
        r"module-auto-keyref", AutoKeyRefModule.as_view(), name="core_auto_keyref_view"
    ),
    re_path(
        r"get-updated-keys",
        get_updated_keys,
        name="core_module_auto_keyref_app_get_updated_keys",
    ),
]
