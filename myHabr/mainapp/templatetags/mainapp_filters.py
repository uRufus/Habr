import re
from django.template import Library
from django.utils.safestring import mark_safe


register = Library()
@register.filter(is_safe=True)
def mark_tags(value):
    return mark_safe(re.sub(r'(@\w+\b)',
                            r'<i style="color:green">\1</i><br>', value))
