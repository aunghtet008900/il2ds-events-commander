# -*- coding: utf-8 -*-

import logging

from django.conf import settings as app_settings


LOG = logging.getLogger(__name__)


def settings(request):
    """
    Inject application settings to template context.
    """
    return {'settings': app_settings}


def project_name(request):
    return {'PROJECT_NAME': unicode(app_settings.PROJECT_NAME)}