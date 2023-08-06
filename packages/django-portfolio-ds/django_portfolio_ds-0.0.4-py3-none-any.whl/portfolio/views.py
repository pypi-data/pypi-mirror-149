import os
from django.shortcuts import render, get_object_or_404
from .models import Portfolio
from django.conf import settings

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def details(request, theme: str, color: str, id: int):
    context = {
            'theme': theme,
            'color': color,
            'obj': get_object_or_404(Portfolio, pk=id),
        }
    logger.debug(context)
    return render(request, f"portfolio_details/details.html", context)
