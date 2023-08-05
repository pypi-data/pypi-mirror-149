from django.template import Library, loader

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
def make_contact(context):
    logger.info(context)
    t = loader.get_template(f"contact/{context['theme']}.html")
    context.update({
        'theme': context['theme'],
        'contact': context['contact'],
    })
    return t.render(context.flatten())
