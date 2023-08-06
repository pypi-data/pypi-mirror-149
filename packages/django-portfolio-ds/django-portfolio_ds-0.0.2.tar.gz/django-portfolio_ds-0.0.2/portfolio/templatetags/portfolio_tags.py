from django.template import Library, loader
from ..models import Portfolio, Category

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def make_portfolio(context):
    t = loader.get_template(f"portfolio/{context['theme']}.html")
    context.update({
        'categories': Category.objects,
        'items': Portfolio.objects
    })
    logger.info(context)
    return t.render(context.flatten())
