from django import template

register = template.Library()

# Для пагинации, чтобы сохранять состояние запроса в фильтрах при переходе между страницами
@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    request = context['request']
    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()